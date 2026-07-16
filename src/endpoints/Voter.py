"""Router de endpoints para Votante (Voter)."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.responses import success_response
from src.crud import Voter_crud
from src.database.config import get_db
from src.schemas.Voter_schema import VoterCreate, VoterResponse

router = APIRouter(prefix="/voters", tags=["Voters"])


@router.post("", status_code=201)
def register_voter(voter_data: VoterCreate, db: Session = Depends(get_db)):
    """Registra un nuevo votante."""
    voter = Voter_crud.create_voter(db, voter_data)
    return success_response(
        data=VoterResponse.model_validate(voter).model_dump(mode="json"),
        message="Votante registrado exitosamente",
    )


@router.get("")
def list_voters(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = Query(None, description="Filtrar por nombre"),
    db: Session = Depends(get_db),
):
    """Lista votantes con paginacion y filtro opcional por nombre."""
    voters = Voter_crud.get_voters(db, skip=skip, limit=limit, name=name)
    return success_response(
        data=[VoterResponse.model_validate(v).model_dump(mode="json") for v in voters]
    )


@router.delete("/{voter_id}")
def delete_voter(voter_id: UUID, db: Session = Depends(get_db)):
    """Elimina un votante por ID."""
    Voter_crud.delete_voter(db, voter_id)
    return success_response(data=None, message="Votante eliminado exitosamente")
