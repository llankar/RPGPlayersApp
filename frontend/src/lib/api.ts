import type { AppState, Diagram, DisplayContent, Note } from './types';

const { protocol, hostname, port } = window.location;
const apiPort = port === '5173' ? '8000' : port;
const baseUrl = apiPort ? `${protocol}//${hostname}:${apiPort}` : `${protocol}//${hostname}`;

async function jsonRequest<T>(url: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    }
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  return (await response.json()) as T;
}

export async function fetchState(): Promise<AppState> {
  return jsonRequest<AppState>(`${baseUrl}/state`);
}

export async function createNote(note: Omit<Note, 'id'>): Promise<Note> {
  return jsonRequest<Note>(`${baseUrl}/notes`, {
    method: 'POST',
    body: JSON.stringify(note)
  });
}

export async function updateNote(note: Note): Promise<Note> {
  return jsonRequest<Note>(`${baseUrl}/notes/${note.id}`, {
    method: 'PATCH',
    body: JSON.stringify(note)
  });
}

export async function deleteNote(id: string): Promise<void> {
  await jsonRequest<void>(`${baseUrl}/notes/${id}`, { method: 'DELETE' });
}

export async function createDiagram(diagram: Omit<Diagram, 'id'>): Promise<Diagram> {
  return jsonRequest<Diagram>(`${baseUrl}/diagrams`, {
    method: 'POST',
    body: JSON.stringify(diagram)
  });
}

export async function setDisplay(display: DisplayContent): Promise<DisplayContent> {
  return jsonRequest<DisplayContent>(`${baseUrl}/display`, {
    method: 'PUT',
    body: JSON.stringify(display)
  });
}

export function createSocket(onMessage: (data: unknown) => void): WebSocket {
  const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const wsHost = apiPort ? `${window.location.hostname}:${apiPort}` : window.location.hostname;
  const ws = new WebSocket(`${wsProtocol}://${wsHost}/ws`);
  ws.onmessage = (event) => onMessage(JSON.parse(event.data));
  return ws;
}
