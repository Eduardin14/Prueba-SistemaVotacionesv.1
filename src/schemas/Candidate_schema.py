"""Schemas Pydantic para Candidato (Candidate)."""

from uuid import UUID

from pydantic import BaseModel, Field


class CandidateCreate(BaseModel):
    """Datos requeridos para registrar un candidato."""

    name: str = Field(..., min_length=1, description="Nombre del candidato")
    party: str | None = Field(None, description="Partido politico (opcional)")


class CandidateResponse(BaseModel):
    """Datos devueltos de un candidato."""

    id: UUID
    name: str
    party: str | None
    votes: int

    model_config = {"from_attributes": True}
