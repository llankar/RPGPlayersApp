"""Pydantic models for TableApp backend."""

from __future__ import annotations

from typing import List, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Note(BaseModel):
    """Represents a markdown note created by a player."""

    id: UUID = Field(default_factory=uuid4)
    title: str
    body_md: str
    author: str
    shared: bool = False


class DiagramNode(BaseModel):
    """A node in a simple graph diagram."""

    id: UUID = Field(default_factory=uuid4)
    label: str
    x: float
    y: float


class DiagramEdge(BaseModel):
    """A directional connection between two nodes."""

    source_id: UUID
    target_id: UUID


class Diagram(BaseModel):
    """Diagram composed of nodes and edges."""

    id: UUID = Field(default_factory=uuid4)
    nodes: List[DiagramNode] = Field(default_factory=list)
    edges: List[DiagramEdge] = Field(default_factory=list)


class DisplayContent(BaseModel):
    """Current shared content shown on the Fire TV screen."""

    type: Literal["note", "diagram"]
    id: UUID

    @classmethod
    def note(cls, note_id: UUID) -> "DisplayContent":
        return cls(type="note", id=note_id)

    @classmethod
    def diagram(cls, diagram_id: UUID) -> "DisplayContent":
        return cls(type="diagram", id=diagram_id)


class AppState(BaseModel):
    """Aggregate state stored in memory and persisted to disk."""

    notes: List[Note] = Field(default_factory=list)
    diagrams: List[Diagram] = Field(default_factory=list)
    display: DisplayContent | None = None
