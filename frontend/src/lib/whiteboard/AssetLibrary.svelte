<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { v4 as uuidv4 } from 'uuid';
  import type { WhiteboardAsset } from '../types';

  export let assets: WhiteboardAsset[] = [];

  const dispatch = createEventDispatcher<{ add: { asset: WhiteboardAsset } }>();
  let label = '';
  let url = '';

  const addAsset = () => {
    if (!label.trim() || !url.trim()) return;
    dispatch('add', { asset: { id: uuidv4(), name: label.trim(), url: url.trim() } });
    label = '';
    url = '';
  };
</script>

<div class="assets">
  <header>
    <h3>Asset library</h3>
    <div class="add">
      <input placeholder="Name" bind:value={label} />
      <input placeholder="Image URL or data URI" bind:value={url} />
      <button on:click={addAsset}>Add</button>
    </div>
  </header>
  <div class="grid">
    {#each assets as asset (asset.id)}
      <figure>
        <img alt={asset.name} src={asset.url} />
        <figcaption>{asset.name}</figcaption>
      </figure>
    {/each}
  </div>
</div>

<style>
  .assets {
    background: #0f1c2e;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  header {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  h3 {
    margin: 0;
    color: #d8e6ff;
  }
  .add {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 8px;
  }
  input {
    padding: 8px;
    background: #0f253b;
    color: #e8f0ff;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
  }
  button {
    padding: 8px 10px;
    border-radius: 6px;
    background: #1e88e5;
    color: white;
    border: none;
  }
  .grid {
    display: grid;
    gap: 10px;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }
  figure {
    margin: 0;
    background: #0c1a2a;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    align-items: center;
  }
  img {
    max-width: 100%;
    max-height: 120px;
    object-fit: contain;
    border-radius: 6px;
  }
  figcaption {
    color: #c7d9ff;
    font-size: 0.9rem;
    text-align: center;
  }
</style>
