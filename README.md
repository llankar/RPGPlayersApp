# TableApp

TableApp is a lightweight FastAPI + Svelte utility for tabletop role‑playing sessions. Players can create notes and diagrams from their own devices while a shared Fire TV display mirrors the selected content in real time via WebSockets.

## Prerequisites
- Python 3.11+
- Node.js 18+

## Installation
```bash
pip install -r requirements.txt
cd frontend
npm install
```

## Running in development
Start the FastAPI server with hot reload:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Run the Svelte dev server in another terminal:
```bash
cd frontend
npm run dev -- --host --port 5173
```

Visit `http://localhost:5173/player` for the player UI and `http://localhost:5173/display` for the TV view. The front‑end uses the current host to reach the API, so devices on the LAN can connect using the machine's IP.

## Building the front‑end
The Vite build is configured to emit static assets directly into the FastAPI static directory so the backend can serve them:
```bash
cd frontend
npm run build
```
After building, the FastAPI server will serve the UI from `/` on port 8000.

## Project structure
- `backend/main.py` – FastAPI app, REST/WebSocket endpoints, and static file serving.
- `backend/models.py` – Pydantic models shared across endpoints (notes, diagrams, shared display content).
- `backend/storage.py` – JSON persistence utilities (`data/state.json`).
- `frontend/src/routes/player.svelte` – Responsive player UI with note creation, diagram builder, and share toggles.
- `frontend/src/routes/display.svelte` – Minimal TV view that shows the currently shared note or diagram.
- `frontend/src/lib/DiagramCanvas.svelte` – Konva-based canvas for building and viewing diagrams.
- `frontend/src/lib/components/MarkdownEditor.svelte` – Simple Markdown editor with a live preview used by the note form.
- `frontend/src/lib/state.ts` – Svelte store layer that wraps the REST API and WebSocket events.
- `frontend/package.json` – Front‑end dependencies and scripts.
- `requirements.txt` – Python dependencies.

## Features
- Create Markdown notes with live preview, keeping them private until you flip the share toggle.
- Build node-and-edge diagrams on a Konva canvas, save them, and share them to the TV in read-only mode.
- Share any note or diagram from the player UI; the backend broadcasts the selected item to all connected displays via WebSocket.
- Fully static front-end build lives in `backend/static` so the FastAPI server can serve everything in one process.

## Extending the app
The code is organized into small, commented modules to keep it readable. Consider adding authentication, richer diagram editing, or note search by extending the corresponding files under `backend/` and `frontend/src/`. Because the Fire TV screen is just another route, you can experiment with custom layouts or transitions in `frontend/src/routes/display.svelte`.
