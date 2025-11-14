from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Mapping
from uuid import UUID

from jose import JWTError, jwt
import bcrypt

from core.config import get_settings

class InvalidTokenError(Exception):
    """Raised when a JWT token cannot be validated."""


def get_password_hash(password: str) -> str:
    """Generate a password hash using bcrypt."""
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check whether the provided password matches the stored hash."""
    if isinstance(hashed_password, str):
        hashed_bytes = hashed_password.encode("utf-8")
    else:
        hashed_bytes = hashed_password

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_bytes,
    )


def create_access_token(
    *,
    subject: str | UUID,
    expires_delta: timedelta | None = None,
    additional_claims: Mapping[str, Any] | None = None,
) -> str:
    """Create a signed JWT token with optional extra claims."""
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))

    payload: Dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    if additional_claims:
        payload.update(additional_claims)

    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token, returning its payload."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as exc:
        raise InvalidTokenError("Token inválido ou expirado.") from exc
    return payload
