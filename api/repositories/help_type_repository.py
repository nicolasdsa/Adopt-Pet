from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.help_type import HelpType


class HelpTypeRepository:
    """Consultas relacionadas aos tipos de ajuda."""

    def list_all(self, db: Session) -> list[HelpType]:
        stmt = select(HelpType).order_by(HelpType.id)
        return list(db.execute(stmt).scalars())

    def get_by_keys(self, db: Session, keys: Iterable[str]) -> list[HelpType]:
        keys = list(keys)
        if not keys:
            return []

        stmt = select(HelpType).where(HelpType.key.in_(keys))
        return list(db.execute(stmt).scalars())
