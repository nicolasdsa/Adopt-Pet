from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from controllers.animal_controller import create_animal, list_species
from core.dependencies import get_current_organization
from db.session import get_db
from models.organization import Organization
from schemas.animal import AnimalCreate, AnimalRead, AnimalSpeciesRead

router = APIRouter(prefix="/animals", tags=["Animais"])


@router.get(
    "/species",
    response_model=list[AnimalSpeciesRead],
    summary="Listar espécies de animais disponíveis",
)
def list_animal_species(db: Session = Depends(get_db)) -> list[AnimalSpeciesRead]:
    """Retorna as espécies cadastradas para seleção."""
    return list_species(db)


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
