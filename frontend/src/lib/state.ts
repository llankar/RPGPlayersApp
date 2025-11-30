import { derived, writable } from 'svelte/store';
import { createDiagram, createNote, createSocket, deleteNote, fetchState, setDisplay, updateNote } from './api';
import type { AppState, Diagram, DisplayContent, Note, WsEventMap } from './types';

const initialState: AppState = { notes: [], diagrams: [], display: null };
const state = writable<AppState>(initialState);

fetchState().then((data) => state.set(data)).catch((error) => console.error(error));

// Wire up websocket updates
createSocket((data: unknown) => {
  const event = data as WsEventMap;
  state.update((current) => {
    switch (event.event) {
      case 'note_added':
        return {
          ...current,
          notes: [...current.notes.filter((n) => n.id !== (event.note as Note).id), event.note as Note]
        };
      case 'note_updated': {
        const updated = event.note as Note | undefined;
        if (!updated) {
          return { ...current, notes: current.notes.filter((n) => n.id !== (event.note_id as string)) };
        }
        return { ...current, notes: current.notes.map((n) => (n.id === updated.id ? updated : n)) };
      }
      case 'diagram_changed': {
        const diag = event.diagram as Diagram;
        return { ...current, diagrams: [...current.diagrams.filter((d) => d.id !== diag.id), diag] };
      }
      case 'display_changed':
        return { ...current, display: event.display as DisplayContent };
      default:
        return current;
    }
  });
});

export const notes = derived(state, ($s) => $s.notes);
export const diagrams = derived(state, ($s) => $s.diagrams);
export const display = derived(state, ($s) => $s.display);

export async function submitNote(payload: Omit<Note, 'id'>): Promise<void> {
  const created = await createNote(payload);
  state.update((current) => ({ ...current, notes: [...current.notes, created] }));
}

export async function patchNote(note: Note): Promise<void> {
  const updated = await updateNote(note);
  state.update((current) => ({
    ...current,
    notes: current.notes.map((n) => (n.id === updated.id ? updated : n))
  }));
}

export async function removeNote(id: string): Promise<void> {
  await deleteNote(id);
  state.update((current) => ({ ...current, notes: current.notes.filter((n) => n.id !== id) }));
}

export async function submitDiagram(diagram: Omit<Diagram, 'id'>): Promise<void> {
  const created = await createDiagram(diagram);
  state.update((current) => ({ ...current, diagrams: [...current.diagrams, created] }));
}

export async function updateDisplay(displayContent: DisplayContent): Promise<void> {
  const result = await setDisplay(displayContent);
  state.update((current) => ({ ...current, display: result }));
}
