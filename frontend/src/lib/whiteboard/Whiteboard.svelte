<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { v4 as uuidv4 } from 'uuid';
  import type {
    Whiteboard,
    WhiteboardAsset,
    WhiteboardConnector,
    WhiteboardLayer,
    WhiteboardShapeKind,
    WhiteboardTool
  } from '../types';
  import AssetLibrary from './AssetLibrary.svelte';
  import Canvas from './Canvas.svelte';
  import LayersPanel from './LayersPanel.svelte';
  import ToolPalette from './ToolPalette.svelte';

  export let whiteboard: Whiteboard;
  export let readonly = false;

  const dispatch = createEventDispatcher<{ change: { board: Whiteboard } }>();

  let activeTool: WhiteboardTool = 'pen';
  let strokeColor = '#1e88e5';
  let strokeWidth = 3;
  let selectedLayerId: string | null = whiteboard.layers[0]?.id ?? null;
  let shapeKind: WhiteboardShapeKind = 'rectangle';
  let textValue = '';
  let stickyValue = '';
  let connectorFrom = '';
  let connectorTo = '';
  let connectorLabel = '';
  let imageAssetId = '';

  $: selectedLayerId = selectedLayerId ?? whiteboard.layers[0]?.id ?? null;
  $: if (selectedLayerId && !whiteboard.layers.find((l) => l.id === selectedLayerId)) {
    selectedLayerId = whiteboard.layers[0]?.id ?? null;
  }

  const updateBoard = (updater: (current: Whiteboard) => Whiteboard) => {
    if (readonly) return;
    const updated = updater(structuredClone(whiteboard));
    dispatch('change', { board: updated });
  };

  const addLayer = (name: string) => {
    updateBoard((current) => {
      const nextLayer: WhiteboardLayer = { id: uuidv4(), name, visible: true, order: current.layers.length };
      current.layers = [...current.layers, nextLayer];
      if (!selectedLayerId) {
        selectedLayerId = nextLayer.id;
      }
      return current;
    });
  };

  const toggleLayer = (id: string) => {
    updateBoard((current) => {
      current.layers = current.layers.map((layer) =>
        layer.id === id ? { ...layer, visible: !layer.visible } : layer
      );
      return current;
    });
  };

  const onStrokeCreated = (event: CustomEvent<{ stroke: Whiteboard['strokes'][number] }>) => {
    updateBoard((current) => {
      current.strokes = [...current.strokes, event.detail.stroke];
      return current;
    });
  };

  const addShape = () => {
    if (!selectedLayerId) return;
    updateBoard((current) => {
      current.shapes = [
        ...current.shapes,
        {
          id: uuidv4(),
          kind: shapeKind,
          x: 120,
          y: 120 + current.shapes.length * 14,
          width: 160,
          height: 90,
          stroke: strokeColor,
          fill: '#17345c',
          layer_id: selectedLayerId
        }
      ];
      return current;
    });
  };

  const addText = () => {
    if (!textValue.trim() || !selectedLayerId) return;
    updateBoard((current) => {
      current.text_items = [
        ...current.text_items,
        {
          id: uuidv4(),
          text: textValue.trim(),
          x: 140,
          y: 120 + current.text_items.length * 24,
          color: '#e8f0ff',
          font_size: 18,
          layer_id: selectedLayerId
        }
      ];
      return current;
    });
    textValue = '';
  };

  const addSticky = () => {
    if (!stickyValue.trim() || !selectedLayerId) return;
    updateBoard((current) => {
      current.sticky_notes = [
        ...current.sticky_notes,
        { id: uuidv4(), text: stickyValue.trim(), x: 180, y: 180, color: '#ffc857', layer_id: selectedLayerId }
      ];
      return current;
    });
    stickyValue = '';
  };

  const addConnector = () => {
    if (!connectorFrom || !connectorTo || !selectedLayerId) return;
    const connector: WhiteboardConnector = {
      id: uuidv4(),
      from_id: connectorFrom,
      to_id: connectorTo,
      label: connectorLabel || null,
      layer_id: selectedLayerId
    };
    updateBoard((current) => {
      current.connectors = [...current.connectors, connector];
      return current;
    });
    connectorFrom = '';
    connectorTo = '';
    connectorLabel = '';
  };

  const addImage = () => {
    if (!imageAssetId || !selectedLayerId) return;
    updateBoard((current) => {
      current.images = [
        ...current.images,
        { id: uuidv4(), asset_id: imageAssetId, x: 200, y: 220, width: 200, height: 140, layer_id: selectedLayerId }
      ];
      return current;
    });
    imageAssetId = '';
  };

  const addAsset = (asset: WhiteboardAsset) => {
    updateBoard((current) => {
      current.assets = [...current.assets, asset];
      return current;
    });
  };

  const connectableIds = () => [
    ...whiteboard.shapes.map((s) => ({ id: s.id, label: `Shape ${s.kind}` })),
    ...whiteboard.text_items.map((t) => ({ id: t.id, label: `Text: ${t.text.slice(0, 16)}` })),
    ...whiteboard.sticky_notes.map((s) => ({ id: s.id, label: `Sticky: ${s.text.slice(0, 16)}` })),
    ...whiteboard.images.map((i) => ({ id: i.id, label: 'Image' }))
  ];
</script>

<div class="whiteboard-shell">
  <div class="controls">
    <ToolPalette
      {activeTool}
      {strokeColor}
      {strokeWidth}
      layers={whiteboard.layers}
      {selectedLayerId}
      on:tool={(e) => (activeTool = e.detail.tool)}
      on:color={(e) => (strokeColor = e.detail.color)}
      on:width={(e) => (strokeWidth = e.detail.width)}
      on:layer={(e) => (selectedLayerId = e.detail.id)}
    />

    <div class="stacked">
      <LayersPanel
        layers={whiteboard.layers}
        on:add={(e) => addLayer(e.detail.name)}
        on:toggle={(e) => toggleLayer(e.detail.id)}
      />

      <AssetLibrary assets={whiteboard.assets} on:add={(e) => addAsset(e.detail.asset)} />
    </div>
  </div>

  <div class="workspace">
    <Canvas
      {whiteboard}
      {activeTool}
      {strokeColor}
      {strokeWidth}
      {selectedLayerId}
      {readonly}
      on:strokeCreated={onStrokeCreated}
    />

    {#if !readonly}
      <div class="actions">
        {#if activeTool === 'shape'}
          <div class="action-card">
            <label>Shape</label>
            <select bind:value={shapeKind}>
              <option value="rectangle">Rectangle</option>
              <option value="ellipse">Ellipse</option>
              <option value="diamond">Diamond</option>
              <option value="arrow">Arrow</option>
            </select>
            <button on:click={addShape}>Add shape</button>
          </div>
        {:else if activeTool === 'text'}
          <div class="action-card">
            <label>Text</label>
            <input placeholder="Add text" bind:value={textValue} />
            <button on:click={addText}>Add text box</button>
          </div>
        {:else if activeTool === 'sticky'}
          <div class="action-card">
            <label>Sticky note</label>
            <input placeholder="Note body" bind:value={stickyValue} />
            <button on:click={addSticky}>Add sticky</button>
          </div>
        {:else if activeTool === 'connector'}
          <div class="action-card">
            <label>Connector</label>
            <div class="row">
              <select bind:value={connectorFrom}>
                <option value="">From</option>
                {#each connectableIds() as item}
                  <option value={item.id}>{item.label}</option>
                {/each}
              </select>
              <select bind:value={connectorTo}>
                <option value="">To</option>
                {#each connectableIds() as item}
                  <option value={item.id}>{item.label}</option>
                {/each}
              </select>
            </div>
            <input placeholder="Label (optional)" bind:value={connectorLabel} />
            <button on:click={addConnector}>Add connector</button>
          </div>
        {:else if activeTool === 'image'}
          <div class="action-card">
            <label>Image</label>
            <select bind:value={imageAssetId}>
              <option value="">Pick asset</option>
              {#each whiteboard.assets as asset}
                <option value={asset.id}>{asset.name}</option>
              {/each}
            </select>
            <button on:click={addImage}>Place image</button>
          </div>
        {:else}
          <div class="action-card hint">Use the canvas to draw freehand strokes.</div>
        {/if}
      </div>
    {/if}
  </div>
</div>

<style>
  .whiteboard-shell {
    display: grid;
    grid-template-columns: 340px 1fr;
    gap: 16px;
    color: #e8f0ff;
  }
  .controls {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .workspace {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .actions {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 10px;
  }
  .action-card {
    background: #0f1c2e;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .action-card.hint {
    color: #9bb8db;
  }
  label {
    font-weight: 600;
  }
  input,
  select {
    padding: 8px;
    background: #0f253b;
    color: #e8f0ff;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
  }
  button {
    padding: 8px 12px;
    background: #1e88e5;
    color: white;
    border: none;
    border-radius: 6px;
  }
  .row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 8px;
  }
  .stacked {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  @media (max-width: 920px) {
    .whiteboard-shell {
      grid-template-columns: 1fr;
    }
  }
</style>
