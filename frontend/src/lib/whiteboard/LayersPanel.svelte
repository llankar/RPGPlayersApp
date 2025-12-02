<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { WhiteboardLayer } from '../types';

  export let layers: WhiteboardLayer[] = [];

  const dispatch = createEventDispatcher<{
    toggle: { id: string };
    add: { name: string };
  }>();

  let newLayerName = '';

  const addLayer = () => {
    if (!newLayerName.trim()) return;
    dispatch('add', { name: newLayerName.trim() });
    newLayerName = '';
  };
</script>

<div class="layers">
  <header>
    <h3>Layers</h3>
    <div class="add">
      <input placeholder="Name" bind:value={newLayerName} />
      <button on:click={addLayer}>Add</button>
    </div>
  </header>
  <ul>
    {#each layers.sort((a, b) => a.order - b.order) as layer (layer.id)}
      <li>
        <label>
          <input type="checkbox" checked={layer.visible} on:change={() => dispatch('toggle', { id: layer.id })} />
          <span>{layer.name}</span>
        </label>
      </li>
    {/each}
  </ul>
</div>

<style>
  .layers {
    background: #0f1c2e;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 12px;
  }
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 10px;
  }
  h3 {
    margin: 0;
    color: #d8e6ff;
  }
  .add {
    display: flex;
    gap: 6px;
  }
  input {
    padding: 6px 8px;
    background: #0f253b;
    color: #e8f0ff;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
  }
  button {
    padding: 6px 10px;
    border-radius: 6px;
    background: #1e88e5;
    color: white;
    border: none;
  }
  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  label {
    color: #c7d9ff;
    display: flex;
    align-items: center;
    gap: 8px;
  }
</style>
