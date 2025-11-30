export type UUID = string;

export interface Note {
  id: UUID;
  title: string;
  body_md: string;
  author: string;
  shared: boolean;
}

export interface DiagramNode {
  id: UUID;
  label: string;
  x: number;
  y: number;
}

export interface DiagramEdge {
  source_id: UUID;
  target_id: UUID;
}

export interface Diagram {
  id: UUID;
  nodes: DiagramNode[];
  edges: DiagramEdge[];
  shared: boolean;
}

export interface DisplayContent {
  type: 'note' | 'diagram';
  id: UUID;
}

export interface AppState {
  notes: Note[];
  diagrams: Diagram[];
  display?: DisplayContent | null;
}

export interface WsEventMap {
  event: 'note_added' | 'note_updated' | 'diagram_changed' | 'display_changed';
  [key: string]: unknown;
}
