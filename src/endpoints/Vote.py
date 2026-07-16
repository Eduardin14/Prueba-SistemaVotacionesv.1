"""Router de endpoints para Voto (Vote)."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.responses import success_response
from src.crud import Vote_crud
from src.database.config import get_db
from src.schemas.Vote_schema import VoteCreate, VoteResponse, VotingStatistics

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("", status_code=201)
def cast_vote(vote_data: VoteCreate, db: Session = Depends(get_db)):
    """Emite un voto (registra voter_id y candidate_id)."""
    vote = Vote_crud.cast_vote(db, vote_data)
    return success_response(
        data=VoteResponse.model_validate(vote).model_dump(mode="json"),
        message="Voto emitido exitosamente",
    )


@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    """
    Obtiene estadisticas de la votacion:
    total de votos por candidato, porcentaje por candidato y total de votantes que votaron.
    """
    stats: VotingStatistics = Vote_crud.get_statistics(db)
    return success_response(data=stats.model_dump(mode="json"))


@router.get("")
def list_votes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Obtiene todos los votos emitidos, con paginacion."""
    votes = Vote_crud.get_votes(db, skip=skip, limit=limit)
    return success_response(
        data=[VoteResponse.model_validate(v).model_dump(mode="json") for v in votes]
    )
