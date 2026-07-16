"""Schemas Pydantic para Voto (Vote) y estadisticas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class VoteCreate(BaseModel):
    """Datos requeridos para emitir un voto."""

    voter_id: UUID = Field(..., description="ID del votante")
    candidate_id: UUID = Field(..., description="ID del candidato seleccionado")


class VoteResponse(BaseModel):
    """Datos devueltos de un voto."""

    id: UUID
    voter_id: UUID
    candidate_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class CandidateStatistics(BaseModel):
    """Estadisticas de un candidato en particular."""

    candidate_id: UUID
    name: str
    party: str | None
    votes: int
    percentage: float


class VotingStatistics(BaseModel):
    """Estadisticas globales de la votacion."""

    total_votes: int
    total_voters_voted: int
    candidates: list[CandidateStatistics]
