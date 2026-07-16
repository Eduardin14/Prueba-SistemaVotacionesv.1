"""Schemas Pydantic para Votante (Voter)."""

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class VoterCreate(BaseModel):
    """Datos requeridos para registrar un votante."""

    name: str = Field(..., min_length=1, description="Nombre del votante")
    email: EmailStr = Field(..., description="Correo electronico unico")


class VoterResponse(BaseModel):
    """Datos devueltos de un votante."""

    id: UUID
    name: str
    email: EmailStr
    has_voted: bool

    model_config = {"from_attributes": True}
