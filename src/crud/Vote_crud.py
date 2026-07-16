"""Logica de acceso a datos para Voto (Vote)."""

from sqlalchemy.orm import Session

from src.core.exceptions import BadRequestError, NotFoundError
from src.entities.Candidate import Candidate
from src.entities.Vote import Vote
from src.entities.Voter import Voter
from src.schemas.Vote_schema import CandidateStatistics, VoteCreate, VotingStatistics


def cast_vote(db: Session, vote_data: VoteCreate) -> Vote:
    """
    Emite un voto validando:
    - Que el votante exista y no haya votado antes.
    - Que el candidato exista.
    Actualiza has_voted del votante e incrementa el contador del candidato.
    """
    voter = db.query(Voter).filter(Voter.id == vote_data.voter_id).first()
    if not voter:
        raise NotFoundError(f"Votante con id '{vote_data.voter_id}' no encontrado")

    if voter.has_voted:
        raise BadRequestError("El votante ya ha emitido su voto")

    candidate = db.query(Candidate).filter(Candidate.id == vote_data.candidate_id).first()
    if not candidate:
        raise NotFoundError(f"Candidato con id '{vote_data.candidate_id}' no encontrado")

    vote = Vote(voter_id=voter.id, candidate_id=candidate.id)
    voter.has_voted = True
    candidate.votes += 1

    db.add(vote)
    db.add(voter)
    db.add(candidate)
    db.commit()
    db.refresh(vote)
    return vote


def get_votes(db: Session, skip: int = 0, limit: int = 10) -> list[Vote]:
    """Lista todos los votos emitidos con paginacion."""
    return db.query(Vote).offset(skip).limit(limit).all()


def get_statistics(db: Session) -> VotingStatistics:
    """Calcula estadisticas: votos totales por candidato, porcentaje y votantes que votaron."""
    candidates = db.query(Candidate).all()
    total_votes = sum(c.votes for c in candidates)
    total_voters_voted = db.query(Voter).filter(Voter.has_voted.is_(True)).count()

    candidate_stats = [
        CandidateStatistics(
            candidate_id=c.id,
            name=c.name,
            party=c.party,
            votes=c.votes,
            percentage=round((c.votes / total_votes * 100), 2) if total_votes > 0 else 0.0,
        )
        for c in candidates
    ]

    return VotingStatistics(
        total_votes=total_votes,
        total_voters_voted=total_voters_voted,
        candidates=candidate_stats,
    )
