"""Logica de acceso a datos para Candidato (Candidate)."""

from uuid import UUID

from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, NotFoundError
from src.entities.Candidate import Candidate
from src.entities.Voter import Voter
from src.schemas.Candidate_schema import CandidateCreate


def create_candidate(db: Session, candidate_data: CandidateCreate) -> Candidate:
    """Registra un nuevo candidato, validando nombre unico y que no sea votante."""
    name = candidate_data.name.strip()

    existing_candidate = db.query(Candidate).filter(Candidate.name.ilike(name)).first()
    if existing_candidate:
        raise ConflictError(f"Ya existe un candidato registrado con el nombre '{name}'")

    is_voter = db.query(Voter).filter(Voter.name.ilike(name)).first()
    if is_voter:
        raise ConflictError(
            f"'{candidate_data.name}' ya esta registrado como votante y no puede ser candidato"
        )

    candidate = Candidate(name=name, party=candidate_data.party)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate


def get_candidate(db: Session, candidate_id: UUID) -> Candidate:
    """Obtiene un candidato por ID o lanza NotFoundError."""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise NotFoundError(f"Candidato con id '{candidate_id}' no encontrado")
    return candidate


def get_candidates(
    db: Session, skip: int = 0, limit: int = 10, name: str | None = None
) -> list[Candidate]:
    """Lista candidatos con paginacion y filtro opcional por nombre."""
    query = db.query(Candidate)
    if name:
        query = query.filter(Candidate.name.ilike(f"%{name}%"))
    return query.offset(skip).limit(limit).all()
