from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from controllers.animal_controller import create_animal
from core.dependencies import get_current_organization
from db.session import get_db
from models.organization import Organization
from schemas.animal import AnimalCreate, AnimalRead

router = APIRouter(prefix="/animals", tags=["Animais"])


@router.post(
    "",
    response_model=AnimalRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo animal",
)
def register_animal(
    payload: AnimalCreate,
    db: Session = Depends(get_db),
    organization: Organization = Depends(get_current_organization),
) -> AnimalRead:
    """Registra um animal vinculado a uma ONG."""
    return create_animal(payload, organization=organization, db=db)
