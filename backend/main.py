"""FastAPI entrypoint for the TableApp backend."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketState

# Ensure the repository root is on the import path so the app can be run as a script.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.models import AppState, Diagram, DisplayContent, Note
from backend.storage import load_state, save_state

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
# Ensure the static directory exists so FastAPI can mount it even before builds run.
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="TableApp")

# Allow connecting from the same host over HTTP/WebSocket.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# In-memory state initialized from disk at startup.
STATE: AppState = load_state()


class WebSocketManager:
    """Tracks active websocket clients and handles broadcasting."""

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict) -> None:
        """Send the message to all connected clients, pruning closed sockets."""
        serialized = json.dumps(message)
        for connection in list(self.active_connections):
            if connection.application_state == WebSocketState.DISCONNECTED:
                self.disconnect(connection)
                continue
            try:
                await connection.send_text(serialized)
            except Exception:
                self.disconnect(connection)


manager = WebSocketManager()


# Helper functions ---------------------------------------------------------

def _find_note(note_id: UUID) -> Note | None:
    return next((n for n in STATE.notes if str(n.id) == str(note_id)), None)


def _persist_state() -> None:
    """Persist the current state to disk."""
    save_state(STATE)


# REST endpoints -----------------------------------------------------------

@app.get("/notes", response_model=List[Note])
async def list_notes() -> List[Note]:
    return STATE.notes


@app.post("/notes", response_model=Note, status_code=201)
async def create_note(note: Note) -> Note:
    STATE.notes.append(note)
    _persist_state()
    await manager.broadcast({"event": "note_added", "note": note.dict()})
    return note


@app.patch("/notes/{note_id}", response_model=Note)
async def update_note(note_id: UUID, note_update: Note) -> Note:
    existing = _find_note(note_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Note not found")
    # Replace the existing note with new data while keeping the id.
    updated_note = note_update.copy(update={"id": existing.id})
    STATE.notes = [updated_note if str(n.id) == str(note_id) else n for n in STATE.notes]
    _persist_state()
    await manager.broadcast({"event": "note_updated", "note": updated_note.dict()})
    return updated_note


@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: UUID) -> None:
    STATE.notes = [n for n in STATE.notes if str(n.id) != str(note_id)]
    _persist_state()
    await manager.broadcast({"event": "note_updated", "note_id": str(note_id)})


@app.get("/diagrams", response_model=List[Diagram])
async def list_diagrams() -> List[Diagram]:
    return STATE.diagrams


@app.post("/diagrams", response_model=Diagram, status_code=201)
async def create_diagram(diagram: Diagram) -> Diagram:
    STATE.diagrams.append(diagram)
    _persist_state()
    await manager.broadcast({"event": "diagram_changed", "diagram": diagram.dict()})
    return diagram


@app.put("/display", response_model=DisplayContent)
async def set_display(display: DisplayContent) -> DisplayContent:
    STATE.display = display
    _persist_state()
    await manager.broadcast({"event": "display_changed", "display": display.dict()})
    return display


@app.get("/state", response_model=AppState)
async def get_state() -> AppState:
    return STATE


# WebSocket ----------------------------------------------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Static files -------------------------------------------------------------

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
