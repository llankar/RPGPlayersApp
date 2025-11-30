"""Persistence helpers for saving and loading application state."""

from __future__ import annotations

import json
from pathlib import Path

from backend.models import AppState

# Store data relative to the repository root so uvicorn can be started anywhere.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "state.json"


def ensure_data_dir() -> None:
    """Create the parent directory for the data file if missing."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_state() -> AppState:
    """Load the application state from disk, returning defaults when absent."""
    ensure_data_dir()
    if DATA_PATH.exists():
        content = DATA_PATH.read_text(encoding="utf-8")
        try:
            data = json.loads(content)
            return AppState(**data)
        except json.JSONDecodeError:
            # Fall back to empty state when the file is corrupted.
            return AppState()
    return AppState()


def save_state(state: AppState) -> None:
    """Persist the application state as JSON on disk."""
    ensure_data_dir()
    DATA_PATH.write_text(state.json(indent=2), encoding="utf-8")
