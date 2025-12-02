<script lang="ts">
import DiagramCanvas from '$lib/DiagramCanvas.svelte';
import MarkdownView from '$lib/MarkdownView.svelte';
import { diagrams, display, notes, whiteboards } from '$lib/state';
import WhiteboardViewer from '$lib/whiteboard/WhiteboardViewer.svelte';

  $: activeDisplay = $display;
  $: currentNote = activeDisplay?.type === 'note' ? $notes.find((n) => n.id === activeDisplay.id) : null;
  $: currentDiagram =
    activeDisplay?.type === 'diagram' ? $diagrams.find((d) => d.id === activeDisplay.id) : null;
  $: currentWhiteboard =
    activeDisplay?.type === 'whiteboard'
      ? $whiteboards.find((w) => w.id === activeDisplay.id)
      : null;
</script>

<section class="display">
  {#if !activeDisplay}
    <h1>No shared content yet</h1>
    <p class="subtitle">Ask the Game Master or a player to share a note or diagram.</p>
  {:else if activeDisplay.type === 'note' && currentNote}
    <h1>{currentNote.title}</h1>
    <p class="subtitle">Shared by {currentNote.author}</p>
    <MarkdownView markdown={currentNote.body_md} />
  {:else if activeDisplay.type === 'diagram' && currentDiagram}
    <h1>Shared diagram</h1>
    <DiagramCanvas nodes={currentDiagram.nodes} edges={currentDiagram.edges} readonly />
  {:else if activeDisplay.type === 'whiteboard' && currentWhiteboard}
    <WhiteboardViewer whiteboard={currentWhiteboard} />
  {:else}
    <h1>Content not found</h1>
    <p class="subtitle">The shared item was removed.</p>
  {/if}
</section>

<style>
  .display {
    min-height: 100vh;
    background: #0b1321;
    color: #e8f0ff;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    align-items: center;
    text-align: center;
  }
  h1 {
    font-size: 2.4rem;
    margin: 0;
  }
  .subtitle {
    color: #b3c6e0;
    margin: 0 0 12px 0;
  }
  :global(.markdown) {
    max-width: 900px;
    font-size: 1.3rem;
  }
  :global(.diagram-frame) {
    max-width: 1000px;
  }
</style>
