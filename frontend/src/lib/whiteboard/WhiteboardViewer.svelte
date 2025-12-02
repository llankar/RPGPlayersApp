<script lang="ts">
  import type { Whiteboard } from '../types';
  import Canvas from './Canvas.svelte';

  export let whiteboard: Whiteboard;
</script>

<div class="viewer">
  <header>
    <h2>{whiteboard.title}</h2>
    <p>Read-only shared view</p>
  </header>
  <Canvas {whiteboard} readonly activeTool="pen" />
</div>

<style>
  .viewer {
    display: flex;
    flex-direction: column;
    gap: 8px;
    color: #e8f0ff;
  }
  header {
    text-align: center;
  }
  h2 {
    margin: 0;
  }
  p {
    margin: 0;
    color: #9bb8db;
  }
</style>
