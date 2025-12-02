<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { WhiteboardLayer, WhiteboardTool } from '../types';

  export let activeTool: WhiteboardTool = 'pen';
  export let strokeColor = '#1e88e5';
  export let strokeWidth = 3;
  export let layers: WhiteboardLayer[] = [];
  export let selectedLayerId: string | null = null;

  const dispatch = createEventDispatcher<{
    tool: { tool: WhiteboardTool };
    color: { color: string };
    width: { width: number };
    layer: { id: string | null };
  }>();

  const setTool = (tool: WhiteboardTool) => dispatch('tool', { tool });
  const setColor = (color: string) => dispatch('color', { color });
  const setWidth = (width: number) => dispatch('width', { width });
  const setLayer = (id: string) => dispatch('layer', { id });
</script>

<div class="tool-palette">
  <div class="tool-row">
    <label>Tools</label>
    <div class="tool-buttons">
      {#each ['pen', 'text', 'sticky', 'shape', 'image', 'connector'] as tool}
        <button class:active={activeTool === tool} on:click={() => setTool(tool as WhiteboardTool)}>
          {tool}
        </button>
      {/each}
    </div>
  </div>

  <div class="tool-row">
    <label>Stroke color</label>
    <input type="color" bind:value={strokeColor} on:input={(e) => setColor(e.currentTarget.value)} />
  </div>

  <div class="tool-row">
    <label>Stroke width</label>
    <input
      type="range"
      min="1"
      max="12"
      step="1"
      bind:value={strokeWidth}
      on:input={(e) => setWidth(parseInt(e.currentTarget.value, 10))}
    />
    <span class="value">{strokeWidth}px</span>
  </div>

  <div class="tool-row">
    <label>Layer</label>
    <select bind:value={selectedLayerId} on:change={(e) => setLayer(e.currentTarget.value)}>
      {#each layers as layer}
        <option value={layer.id}>{layer.name}</option>
      {/each}
    </select>
  </div>
</div>

<style>
  .tool-palette {
    display: flex;
    flex-direction: column;
    gap: 12px;
    background: #0f1c2e;
    border: 1px solid #1e3a5f;
    padding: 12px;
    border-radius: 10px;
  }
  .tool-row {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #c7d9ff;
    flex-wrap: wrap;
  }
  .tool-buttons {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }
  button {
    padding: 6px 10px;
    background: #133458;
    color: #d8e6ff;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    text-transform: capitalize;
  }
  button.active {
    background: #1e88e5;
    border-color: #42a5f5;
  }
  label {
    font-weight: 600;
  }
  input[type='color'] {
    border: none;
    width: 44px;
    height: 32px;
    padding: 0;
    background: transparent;
  }
  input[type='range'] {
    flex: 1;
  }
  select {
    padding: 6px;
    background: #0f253b;
    color: #e8f0ff;
    border-radius: 6px;
    border: 1px solid #1e3a5f;
  }
  .value {
    color: #9bb8db;
  }
</style>
