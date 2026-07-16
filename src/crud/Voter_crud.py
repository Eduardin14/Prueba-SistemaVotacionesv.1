"""Logica de acceso a datos para Votante (Voter)."""

from uuid import UUID

from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, NotFoundError
from src.entities.Candidate import Candidate
from src.entities.Voter import Voter
from src.schemas.Voter_schema import VoterCreate


def create_voter(db: Session, voter_data: VoterCreate) -> Voter:
    """Registra un nuevo votante, validando email unico y que no sea candidato."""
    existing = db.query(Voter).filter(Voter.email == voter_data.email).first()
    if existing:
        raise ConflictError(f"Ya existe un votante con el email '{voter_data.email}'")

    is_candidate = (
        db.query(Candidate)
        .filter(Candidate.name.ilike(voter_data.name.strip()))
        .first()
    )
    if is_candidate:
        raise ConflictError(
            f"'{voter_data.name}' ya esta registrado como candidato y no puede ser votante"
        )

    voter = Voter(name=voter_data.name.strip(), email=voter_data.email)
    db.add(voter)
    db.commit()
    db.refresh(voter)
    return voter


def get_voter(db: Session, voter_id: UUID) -> Voter:
    """Obtiene un votante por ID o lanza NotFoundError."""
    voter = db.query(Voter).filter(Voter.id == voter_id).first()
    if not voter:
        raise NotFoundError(f"Votante con id '{voter_id}' no encontrado")
    return voter


def get_voters(db: Session, skip: int = 0, limit: int = 10, name: str | None = None) -> list[Voter]:
    """Lista votantes con paginacion y filtro opcional por nombre."""
    query = db.query(Voter)
    if name:
        query = query.filter(Voter.name.ilike(f"%{name}%"))
    return query.offset(skip).limit(limit).all()


def delete_voter(db: Session, voter_id: UUID) -> None:
    """Elimina un votante por ID."""
    voter = get_voter(db, voter_id)
    db.delete(voter)
    db.commit()
