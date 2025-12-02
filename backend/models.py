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
    shared: bool = False


class DisplayContent(BaseModel):
    """Current shared content shown on the Fire TV screen."""

    type: Literal["note", "diagram", "whiteboard"]
    id: UUID

    @classmethod
    def note(cls, note_id: UUID) -> "DisplayContent":
        return cls(type="note", id=note_id)

    @classmethod
    def diagram(cls, diagram_id: UUID) -> "DisplayContent":
        return cls(type="diagram", id=diagram_id)

    @classmethod
    def whiteboard(cls, whiteboard_id: UUID) -> "DisplayContent":
        return cls(type="whiteboard", id=whiteboard_id)


class StrokePoint(BaseModel):
    """Point belonging to a drawn stroke."""

    x: float
    y: float


class WhiteboardStroke(BaseModel):
    """Freehand stroke captured from the canvas."""

    id: UUID = Field(default_factory=uuid4)
    points: List[StrokePoint] = Field(default_factory=list)
    color: str = "#1e88e5"
    width: float = 2.0
    layer_id: UUID


class WhiteboardShape(BaseModel):
    """Basic geometric shape."""

    id: UUID = Field(default_factory=uuid4)
    kind: Literal["rectangle", "ellipse", "diamond", "arrow"]
    x: float
    y: float
    width: float
    height: float
    stroke: str = "#e8f0ff"
    fill: str = "#1e3a5f"
    layer_id: UUID


class WhiteboardTextBox(BaseModel):
    """Rich text box."""

    id: UUID = Field(default_factory=uuid4)
    text: str
    x: float
    y: float
    color: str = "#e8f0ff"
    font_size: float = 16.0
    layer_id: UUID


class WhiteboardStickyNote(BaseModel):
    """Sticky note item with quick text."""

    id: UUID = Field(default_factory=uuid4)
    text: str
    x: float
    y: float
    color: str = "#ffc857"
    layer_id: UUID


class WhiteboardAsset(BaseModel):
    """Asset reference for images uploaded to the board."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    url: str


class WhiteboardImage(BaseModel):
    """Placed image on the canvas."""

    id: UUID = Field(default_factory=uuid4)
    asset_id: UUID
    x: float
    y: float
    width: float
    height: float
    layer_id: UUID


class WhiteboardConnector(BaseModel):
    """Connector line linking two items."""

    id: UUID = Field(default_factory=uuid4)
    from_id: UUID
    to_id: UUID
    label: str | None = None
    layer_id: UUID


class WhiteboardLayer(BaseModel):
    """Layer used to organize items on the board."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    visible: bool = True
    order: int = 0


class Whiteboard(BaseModel):
    """Interactive whiteboard supporting drawing, shapes, and assets."""

    id: UUID = Field(default_factory=uuid4)
    title: str = "Untitled board"
    layers: List[WhiteboardLayer] = Field(default_factory=list)
    strokes: List[WhiteboardStroke] = Field(default_factory=list)
    shapes: List[WhiteboardShape] = Field(default_factory=list)
    text_items: List[WhiteboardTextBox] = Field(default_factory=list)
    sticky_notes: List[WhiteboardStickyNote] = Field(default_factory=list)
    connectors: List[WhiteboardConnector] = Field(default_factory=list)
    images: List[WhiteboardImage] = Field(default_factory=list)
    assets: List[WhiteboardAsset] = Field(default_factory=list)
    shared: bool = False

    @classmethod
    def create_default(cls, title: str = "Untitled board") -> "Whiteboard":
        base_layer = WhiteboardLayer(name="Base", order=0)
        return cls(title=title, layers=[base_layer])


class AppState(BaseModel):
    """Aggregate state stored in memory and persisted to disk."""

    notes: List[Note] = Field(default_factory=list)
    diagrams: List[Diagram] = Field(default_factory=list)
    whiteboards: List[Whiteboard] = Field(default_factory=list)
    display: DisplayContent | None = None
