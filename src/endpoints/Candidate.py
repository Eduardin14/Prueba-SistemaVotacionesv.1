"""Router de endpoints para Candidato (Candidate)."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.responses import success_response
from src.crud import Candidate_crud
from src.database.config import get_db
from src.schemas.Candidate_schema import CandidateCreate, CandidateResponse

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.post("", status_code=201)
def register_candidate(candidate_data: CandidateCreate, db: Session = Depends(get_db)):
    """Registra un nuevo candidato."""
    candidate = Candidate_crud.create_candidate(db, candidate_data)
    return success_response(
        data=CandidateResponse.model_validate(candidate).model_dump(mode="json"),
        message="Candidato registrado exitosamente",
    )


@router.get("")
def list_candidates(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = Query(None, description="Filtrar por nombre"),
    db: Session = Depends(get_db),
):
    """Obtiene la lista de candidatos, con paginacion y filtro opcional por nombre."""
    candidates = Candidate_crud.get_candidates(db, skip=skip, limit=limit, name=name)
    return success_response(
        data=[
            CandidateResponse.model_validate(c).model_dump(mode="json") for c in candidates
        ]
    )
