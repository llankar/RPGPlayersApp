<script lang="ts">
  import WhiteboardSurface from '$lib/whiteboard/Whiteboard.svelte';
  import { patchWhiteboard, submitWhiteboard, updateDisplay, whiteboards } from '$lib/state';
  import type { Whiteboard } from '$lib/types';
  import { v4 as uuidv4 } from 'uuid';

  const createBoard = (): Whiteboard => ({
    id: uuidv4(),
    title: 'New whiteboard',
    layers: [
      {
        id: uuidv4(),
        name: 'Base',
        visible: true,
        order: 0
      }
    ],
    strokes: [],
    shapes: [],
    text_items: [],
    sticky_notes: [],
    connectors: [],
    images: [],
    assets: [],
    shared: false
  });

  let workingBoard: Whiteboard = createBoard();
  let selectedBoardId: string | null = null;
  let status = '';
  let error: string | null = null;

  $: if (selectedBoardId) {
    const found = $whiteboards.find((w) => w.id === selectedBoardId);
    if (found) {
      workingBoard = structuredClone(found);
    }
  }

  const resetFeedback = () => {
    status = '';
    error = null;
  };

  const startNewBoard = () => {
    resetFeedback();
    selectedBoardId = null;
    workingBoard = createBoard();
  };

  const handleChange = (event: CustomEvent<{ board: Whiteboard }>) => {
    resetFeedback();
    workingBoard = event.detail.board;
  };

  const saveBoard = async () => {
    resetFeedback();
    const existing = $whiteboards.find((b) => b.id === workingBoard.id);
    try {
      const saved = existing ? await patchWhiteboard(workingBoard) : await submitWhiteboard(workingBoard);
      workingBoard = structuredClone(saved);
      status = 'Whiteboard saved';
      selectedBoardId = saved.id;
    } catch (e) {
      error = (e as Error).message;
    }
  };

  const toggleShare = async (board: Whiteboard) => {
    resetFeedback();
    try {
      const updated = await patchWhiteboard({ ...board, shared: !board.shared });
      workingBoard = structuredClone(updated.id === workingBoard.id ? updated : workingBoard);
      if (updated.shared) {
        await updateDisplay({ type: 'whiteboard', id: updated.id });
        status = 'Shared to display';
      }
    } catch (e) {
      error = (e as Error).message;
    }
  };

  const sendToDisplay = async (board: Whiteboard) => {
    resetFeedback();
    await updateDisplay({ type: 'whiteboard', id: board.id });
    status = 'Sent to display';
  };
</script>

<section class="page">
  <header>
    <div>
      <p class="eyebrow">RPG Table Toolkit</p>
      <h1>Collaborative whiteboard</h1>
      <p class="subtitle">
        Draw, drop sticky notes, wire connectors, and share the canvas live with your table display.
      </p>
    </div>
    <button class="ghost" on:click={startNewBoard}>Start fresh</button>
  </header>

  <div class="columns">
    <div class="panel">
      <div class="panel-head">
        <div>
          <p class="eyebrow">Board</p>
          <h2>{workingBoard.title}</h2>
        </div>
        <button class="primary" on:click={saveBoard}>Save whiteboard</button>
      </div>

      {#if error}
        <div class="banner error">{error}</div>
      {/if}
      {#if status}
        <div class="banner success">{status}</div>
      {/if}

      <WhiteboardSurface whiteboard={workingBoard} on:change={handleChange} />
    </div>

    <div class="panel side">
      <h3>Saved whiteboards</h3>
      <p class="helper">Load an existing board, share it, or jump back into editing.</p>
      <div class="board-list">
        {#each $whiteboards as board (board.id)}
          <article class:selected={board.id === workingBoard.id}>
            <div>
              <h4>{board.title}</h4>
              <p class="meta">{board.layers.length} layer(s) • {board.sticky_notes.length} sticky notes</p>
            </div>
            <div class="actions">
              <button on:click={() => (selectedBoardId = board.id)}>Open</button>
              <button class:active={board.shared} on:click={() => toggleShare(board)}>
                {board.shared ? 'Shared' : 'Share'}
              </button>
              <button on:click={() => sendToDisplay(board)}>Send to display</button>
            </div>
          </article>
        {/each}
        {#if !$whiteboards.length}
          <p class="helper">No boards yet—draw something and save it.</p>
        {/if}
      </div>
    </div>
  </div>
</section>

<style>
  .page {
    padding: 24px;
    color: #e8f0ff;
    max-width: 1200px;
    margin: 0 auto 42px auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
  h1 {
    margin: 4px 0;
  }
  .subtitle {
    margin: 0;
    color: #9bb8db;
  }
  .eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.8rem;
    color: #7ba6e0;
    margin: 0;
  }
  .columns {
    display: grid;
    grid-template-columns: 1.8fr 1fr;
    gap: 16px;
    align-items: start;
  }
  .panel {
    background: #0f1c2e;
    border: 1px solid #1e3a5f;
    padding: 16px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .panel-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .side h3 {
    margin: 0;
  }
  .side .helper {
    color: #9bb8db;
    margin: 0;
  }
  button {
    padding: 10px 14px;
    border-radius: 8px;
    border: 1px solid #1e3a5f;
    background: #17345c;
    color: white;
    font-weight: 600;
  }
  button.primary {
    background: #1e88e5;
    border-color: #42a5f5;
  }
  button.ghost {
    background: transparent;
  }
  button.active {
    background: #00c853;
    border-color: #5efc82;
  }
  .banner {
    padding: 10px 12px;
    border-radius: 8px;
  }
  .banner.error {
    background: #ffebee;
    color: #b71c1c;
  }
  .banner.success {
    background: #e2f3ff;
    color: #0d47a1;
  }
  .board-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  article {
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 10px;
    background: #0c1a2a;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  article.selected {
    border-color: #42a5f5;
  }
  .meta {
    margin: 0;
    color: #9bb8db;
  }
  .actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }
  @media (max-width: 960px) {
    .columns {
      grid-template-columns: 1fr;
    }
    header {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>
