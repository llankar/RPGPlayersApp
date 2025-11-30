# Copilot Instructions for TableApp

## Project Overview
TableApp is a real-time collaborative tabletop RPG tool with a FastAPI backend and Svelte frontend. Players create notes/diagrams on their devices; a shared Fire TV display mirrors selected content via WebSocket broadcasts.

## Architecture

### Backend (Python/FastAPI)
- **Single process, in-memory state** persisted to `data/state.json` at startup/shutdown
- **Data model** (`backend/models.py`): Pydantic BaseModels for `Note`, `Diagram`, `DisplayContent`, and `AppState`
- **Endpoints** (`backend/main.py`):
  - REST: `/notes` (CRUD), `/diagrams` (CR), `/display` (PUT), `/state` (GET)
  - WebSocket: `/ws` broadcasts state changes to all connected clients
- **WebSocketManager**: Tracks active connections, prunes disconnected sockets, serializes messages to JSON

### Frontend (Svelte/TypeScript)
- **Reactive stores** (`frontend/src/lib/state.ts`): Svelte writable stores for `notes`, `diagrams`, `display` derived from app state
- **WebSocket listener**: Automatically updates stores on `note_added`, `note_updated`, `diagram_changed`, `display_changed` events
- **API layer** (`frontend/src/lib/api.ts`): 
  - Detects API port: if dev server on 5173, routes to backend on 8000; otherwise uses same port
  - All requests include `Content-Type: application/json` header
- **Routes**: `/player` (create/edit), `/display` (read-only TV view)
- **Canvas library**: Konva.js for diagram rendering (see `DiagramCanvas.svelte`)

## Key Workflows

### Adding a Feature
1. **Backend model change**: Add field to Pydantic class in `backend/models.py`
2. **Persistence**: Storage auto-handles new fields (append-only JSON)
3. **REST endpoint**: Add/modify in `backend/main.py`, wrap with `_persist_state()` and `manager.broadcast()`
4. **Frontend type**: Mirror model in `frontend/src/lib/types.ts`
5. **Frontend action**: Create API call in `frontend/src/lib/api.ts`, update store in `frontend/src/lib/state.ts`

### Build & Deploy
- **Development**: 
  ```
  uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
  cd frontend && npm run dev -- --host --port 5173
  ```
- **Production**: `npm run build` emits static files to `backend/static/`; FastAPI serves on port 8000

## Critical Patterns

### State Management
- **Single source of truth**: `AppState` in memory, synced to disk after mutations
- **Optimistic updates**: Frontend updates stores before server confirmation
- **WebSocket broadcasts**: All mutations trigger broadcasts; clients listen for events matching their operation type
- **UUID usage**: All entities use UUID fields; string comparisons on frontend (`str(n.id) == str(note_id)`)

### Error Handling
- **Backend**: HTTPException(404) when entity not found; WebSocket silently prunes broken connections
- **Frontend**: `jsonRequest()` throws on non-ok status; consumers should handle with try/catch
- **Graceful fallbacks**: Storage loads empty state if JSON corrupted; WebSocket reconnect isn't implemented (manual page reload)

### API Design
- Use Pydantic `.dict()` and `.json()` for serialization
- PATCH only for updates; DELETE returns 204 no-content
- DisplayContent uses type discriminator: `type: Literal["note", "diagram"]` with class methods `DisplayContent.note(id)` / `.diagram(id)`

## File Reference
- `backend/main.py` – All HTTP/WebSocket handlers and manager; **start here for endpoint behavior**
- `backend/models.py` – Data contracts; **mirror TypeScript types here**
- `backend/storage.py` – Persistence; **resilient to corruption, data-relative paths**
- `frontend/src/lib/state.ts` – Store sync logic; **every event type handled here**
- `frontend/src/lib/api.ts` – Port detection & HTTP setup; **changes affect all frontend requests**
- `frontend/src/routes/player.svelte` & `display.svelte` – UI entry points

## Common Tasks
- **Fix WebSocket typo**: Check `event` name in both `main.py` broadcast and `state.ts` switch statement
- **Add note field**: Update `Note` model → add REST tests → update frontend types → add UI field
- **Persist new data**: Auto-saved if in `AppState`; verify `storage.py` loads it
- **Debug API port**: Frontend uses smart detection; hardcode in `api.ts` if needed for LAN testing
