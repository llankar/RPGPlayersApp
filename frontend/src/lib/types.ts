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
  type: 'note' | 'diagram' | 'whiteboard';
  id: UUID;
}

export interface AppState {
  notes: Note[];
  diagrams: Diagram[];
  whiteboards: Whiteboard[];
  display?: DisplayContent | null;
}

export interface WsEventMap {
  event: 'note_added' | 'note_updated' | 'diagram_changed' | 'whiteboard_changed' | 'display_changed';
  [key: string]: unknown;
}

export interface StrokePoint {
  x: number;
  y: number;
}

export interface WhiteboardStroke {
  id: UUID;
  points: StrokePoint[];
  color: string;
  width: number;
  layer_id: UUID;
}

export type WhiteboardShapeKind = 'rectangle' | 'ellipse' | 'diamond' | 'arrow';

export interface WhiteboardShape {
  id: UUID;
  kind: WhiteboardShapeKind;
  x: number;
  y: number;
  width: number;
  height: number;
  stroke: string;
  fill: string;
  layer_id: UUID;
}

export interface WhiteboardTextBox {
  id: UUID;
  text: string;
  x: number;
  y: number;
  color: string;
  font_size: number;
  layer_id: UUID;
}

export interface WhiteboardStickyNote {
  id: UUID;
  text: string;
  x: number;
  y: number;
  color: string;
  layer_id: UUID;
}

export interface WhiteboardAsset {
  id: UUID;
  name: string;
  url: string;
}

export interface WhiteboardImage {
  id: UUID;
  asset_id: UUID;
  x: number;
  y: number;
  width: number;
  height: number;
  layer_id: UUID;
}

export interface WhiteboardConnector {
  id: UUID;
  from_id: UUID;
  to_id: UUID;
  label?: string | null;
  layer_id: UUID;
}

export interface WhiteboardLayer {
  id: UUID;
  name: string;
  visible: boolean;
  order: number;
}

export interface Whiteboard {
  id: UUID;
  title: string;
  layers: WhiteboardLayer[];
  strokes: WhiteboardStroke[];
  shapes: WhiteboardShape[];
  text_items: WhiteboardTextBox[];
  sticky_notes: WhiteboardStickyNote[];
  connectors: WhiteboardConnector[];
  images: WhiteboardImage[];
  assets: WhiteboardAsset[];
  shared: boolean;
}

export type WhiteboardTool = 'pen' | 'text' | 'sticky' | 'shape' | 'image' | 'connector';
