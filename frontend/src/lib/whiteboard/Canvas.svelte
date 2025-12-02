<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { v4 as uuidv4 } from 'uuid';
  import type {
    StrokePoint,
    Whiteboard,
    WhiteboardConnector,
    WhiteboardShape,
    WhiteboardTool
  } from '../types';

  const CONNECTOR_OFFSET = 12;

  export let whiteboard: Whiteboard;
  export let activeTool: WhiteboardTool = 'pen';
  export let strokeColor = '#1e88e5';
  export let strokeWidth = 3;
  export let selectedLayerId: string | null = null;
  export let readonly = false;

  const dispatch = createEventDispatcher<{
    strokeCreated: { stroke: Whiteboard['strokes'][number] };
  }>();

  let drawing = false;
  let draftPoints: StrokePoint[] = [];

  $: activeLayerId = selectedLayerId ?? whiteboard.layers[0]?.id ?? null;
  $: visibleLayers = new Set(whiteboard.layers.filter((l) => l.visible).map((l) => l.id));

  const pointerToSvg = (event: PointerEvent): StrokePoint => {
    const svg = event.currentTarget as SVGSVGElement;
    const rect = svg.getBoundingClientRect();
    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };
  };

  const onPointerDown = (event: PointerEvent) => {
    if (readonly || activeTool !== 'pen' || !activeLayerId) return;
    drawing = true;
    draftPoints = [pointerToSvg(event)];
  };

  const onPointerMove = (event: PointerEvent) => {
    if (!drawing || readonly || activeTool !== 'pen') return;
    draftPoints = [...draftPoints, pointerToSvg(event)];
  };

  const onPointerUp = () => {
    if (!drawing || readonly || activeTool !== 'pen' || !activeLayerId) return;
    drawing = false;
    if (draftPoints.length < 2) {
      draftPoints = [];
      return;
    }
    dispatch('strokeCreated', {
      stroke: {
        id: uuidv4(),
        points: draftPoints,
        color: strokeColor,
        width: strokeWidth,
        layer_id: activeLayerId
      }
    });
    draftPoints = [];
  };

  const shapePath = (shape: WhiteboardShape) => {
    switch (shape.kind) {
      case 'ellipse':
        return null;
      case 'diamond': {
        const cx = shape.x + shape.width / 2;
        const cy = shape.y + shape.height / 2;
        return `${cx},${shape.y} ${shape.x + shape.width},${cy} ${cx},${shape.y + shape.height} ${shape.x},${cy}`;
      }
      case 'arrow': {
        const head = 14;
        const tailY = shape.y + shape.height / 2;
        const headPoint = `${shape.x + shape.width},${tailY}`;
        const tailLeft = `${shape.x},${tailY}`;
        const headTop = `${shape.x + shape.width - head},${shape.y}`;
        const headBottom = `${shape.x + shape.width - head},${shape.y + shape.height}`;
        return `${tailLeft} ${headTop} ${headPoint} ${headBottom}`;
      }
      default:
        return null;
    }
  };

  const connectorCoords = (connector: WhiteboardConnector) => {
    const start = findAnchor(connector.from_id);
    const end = findAnchor(connector.to_id);
    return start && end
      ? {
          x1: start.x,
          y1: start.y,
          x2: end.x,
          y2: end.y
        }
      : null;
  };

  const findAnchor = (id: string) => {
    const shape = whiteboard.shapes.find((s) => s.id === id);
    if (shape) return { x: shape.x + shape.width / 2, y: shape.y + shape.height / 2 };

    const sticky = whiteboard.sticky_notes.find((s) => s.id === id);
    if (sticky) return { x: sticky.x, y: sticky.y };

    const text = whiteboard.text_items.find((t) => t.id === id);
    if (text) return { x: text.x, y: text.y };

    const image = whiteboard.images.find((i) => i.id === id);
    if (image) return { x: image.x + image.width / 2, y: image.y + image.height / 2 };

    return null;
  };
</script>

<svg
  class="whiteboard-surface"
  on:pointerdown={onPointerDown}
  on:pointermove={onPointerMove}
  on:pointerup={onPointerUp}
  on:pointerleave={onPointerUp}
  role="presentation"
>
  {#each whiteboard.strokes as stroke (stroke.id)}
    {#if visibleLayers.has(stroke.layer_id)}
      <polyline
        fill="none"
        stroke={stroke.color}
        stroke-width={stroke.width}
        stroke-linejoin="round"
        stroke-linecap="round"
        points={stroke.points.map((p) => `${p.x},${p.y}`).join(' ')}
      />
    {/if}
  {/each}

  {#each whiteboard.shapes as shape (shape.id)}
    {#if visibleLayers.has(shape.layer_id)}
      {#if shape.kind === 'rectangle'}
        <rect
          x={shape.x}
          y={shape.y}
          width={shape.width}
          height={shape.height}
          stroke={shape.stroke}
          fill={shape.fill}
          rx="8"
          ry="8"
        />
      {:else if shape.kind === 'ellipse'}
        <ellipse
          cx={shape.x + shape.width / 2}
          cy={shape.y + shape.height / 2}
          rx={shape.width / 2}
          ry={shape.height / 2}
          stroke={shape.stroke}
          fill={shape.fill}
        />
      {:else}
        <polygon points={shapePath(shape)} stroke={shape.stroke} fill={shape.fill} />
      {/if}
    {/if}
  {/each}

  {#each whiteboard.text_items as text (text.id)}
    {#if visibleLayers.has(text.layer_id)}
      <text x={text.x} y={text.y} fill={text.color} font-size={text.font_size} dominant-baseline="hanging">
        {text.text}
      </text>
    {/if}
  {/each}

  {#each whiteboard.sticky_notes as sticky (sticky.id)}
    {#if visibleLayers.has(sticky.layer_id)}
      <g>
        <rect x={sticky.x - 80} y={sticky.y - 40} width="160" height="80" rx="10" ry="10" fill={sticky.color} />
        <text x={sticky.x - 70} y={sticky.y - 20} fill="#1b1b1b" font-size="14" font-weight="600">
          {sticky.text}
        </text>
      </g>
    {/if}
  {/each}

  {#each whiteboard.images as image (image.id)}
    {#if visibleLayers.has(image.layer_id)}
      {#if whiteboard.assets.find((asset) => asset.id === image.asset_id) as asset}
        <image
          href={asset.url}
          x={image.x}
          y={image.y}
          width={image.width}
          height={image.height}
          preserveAspectRatio="xMidYMid meet"
        />
      {/if}
    {/if}
  {/each}

  {#each whiteboard.connectors as connector (connector.id)}
    {#if visibleLayers.has(connector.layer_id)}
      {#if connectorCoords(connector) as coords}
        <g class="connector">
          <line x1={coords.x1} y1={coords.y1} x2={coords.x2} y2={coords.y2} />
          <circle cx={coords.x1} cy={coords.y1} r={CONNECTOR_OFFSET / 3} />
          <circle cx={coords.x2} cy={coords.y2} r={CONNECTOR_OFFSET / 3} />
          {#if connector.label}
            <text
              x={(coords.x1 + coords.x2) / 2}
              y={(coords.y1 + coords.y2) / 2 - CONNECTOR_OFFSET}
              text-anchor="middle"
              fill="#c7d9ff"
              font-size="12"
            >
              {connector.label}
            </text>
          {/if}
        </g>
      {/if}
    {/if}
  {/each}

  {#if drawing && draftPoints.length}
    <polyline
      fill="none"
      stroke={strokeColor}
      stroke-width={strokeWidth}
      stroke-linejoin="round"
      stroke-linecap="round"
      points={draftPoints.map((p) => `${p.x},${p.y}`).join(' ')}
    />
  {/if}
</svg>

<style>
  .whiteboard-surface {
    width: 100%;
    height: 520px;
    background: #0c1a2a;
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.04);
  }
  rect,
  ellipse,
  polygon,
  line {
    stroke-width: 2;
  }
  .connector line {
    stroke: #8bd5ff;
    stroke-dasharray: 6 4;
  }
  .connector circle {
    fill: #8bd5ff;
  }
</style>
