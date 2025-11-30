<script lang="ts">
  import DiagramCanvas from '$lib/DiagramCanvas.svelte';
  import MarkdownView from '$lib/MarkdownView.svelte';
  import { diagrams, notes, patchNote, submitDiagram, submitNote, updateDisplay } from '$lib/state';
  import type { DiagramEdge, DiagramNode, Note } from '$lib/types';
  import { v4 as uuidv4 } from 'uuid';

  let title = '';
  let author = '';
  let body = '';
  let error: string | null = null;

  let diagramNodes: DiagramNode[] = [];
  let diagramEdges: DiagramEdge[] = [];
  let edgeSource = '';
  let edgeTarget = '';

  const addNode = () => {
    const count = diagramNodes.length + 1;
    diagramNodes = [
      ...diagramNodes,
      { id: uuidv4(), label: `Node ${count}`, x: 80 + count * 40, y: 80 + count * 20 }
    ];
  };

  const addEdge = () => {
    if (!edgeSource || !edgeTarget || edgeSource === edgeTarget) return;
    diagramEdges = [...diagramEdges, { source_id: edgeSource, target_id: edgeTarget }];
    edgeSource = '';
    edgeTarget = '';
  };

  const submitNoteForm = async () => {
    error = null;
    try {
      await submitNote({ title, author, body_md: body, shared: false });
      title = '';
      author = '';
      body = '';
    } catch (e) {
      error = (e as Error).message;
    }
  };

  const saveDiagram = async () => {
    if (!diagramNodes.length) {
      error = 'Add at least one node before saving the diagram.';
      return;
    }
    error = null;
    try {
      await submitDiagram({ nodes: diagramNodes, edges: diagramEdges });
      diagramNodes = [];
      diagramEdges = [];
    } catch (e) {
      error = (e as Error).message;
    }
  };

  const toggleShare = async (note: Note) => {
    const updated = { ...note, shared: !note.shared };
    await patchNote(updated);
    if (updated.shared) {
      await updateDisplay({ type: 'note', id: updated.id });
    }
  };

  const shareDiagram = async (id: string) => {
    await updateDisplay({ type: 'diagram', id });
  };

  const moveNode = (id: string, x: number, y: number) => {
    diagramNodes = diagramNodes.map((n) => (n.id === id ? { ...n, x, y } : n));
  };
</script>

<section class="page">
  <header>
    <div>
      <h1>TableApp Player</h1>
      <p>Create notes and diagrams, then share them to the table display.</p>
    </div>
  </header>

  {#if error}
    <div class="banner">{error}</div>
  {/if}

  <div class="grid">
    <div class="panel">
      <h2>New note</h2>
      <label>
        Title
        <input bind:value={title} placeholder="Short title" />
      </label>
      <label>
        Author
        <input bind:value={author} placeholder="Your name" />
      </label>
      <label>
        Body (Markdown)
        <textarea rows="6" bind:value={body} placeholder="Write your note in Markdown"></textarea>
      </label>
      <button on:click|preventDefault={submitNoteForm}>Save note</button>
    </div>

    <div class="panel">
      <h2>Live preview</h2>
      <MarkdownView markdown={body || '*Start typing to see the preview*'} />
    </div>
  </div>

  <div class="panel">
    <h2>Notes</h2>
    <div class="note-list">
      {#each $notes as note (note.id)}
        <article>
          <div class="note-head">
            <div>
              <h3>{note.title}</h3>
              <small>By {note.author}</small>
            </div>
            <label class="toggle">
              <input type="checkbox" checked={note.shared} on:change={() => toggleShare(note)} />
              <span>Share</span>
            </label>
          </div>
          <MarkdownView markdown={note.body_md} />
        </article>
      {/each}
    </div>
  </div>

  <div class="panel">
    <h2>Diagram builder</h2>
    <div class="diagram-grid">
      <div>
        <button on:click={addNode}>Add node</button>
        <div class="edge-form">
          <select bind:value={edgeSource}>
            <option value="">Source</option>
            {#each diagramNodes as node}
              <option value={node.id}>{node.label}</option>
            {/each}
          </select>
          <select bind:value={edgeTarget}>
            <option value="">Target</option>
            {#each diagramNodes as node}
              <option value={node.id}>{node.label}</option>
            {/each}
          </select>
          <button on:click={addEdge}>Add edge</button>
        </div>
        <p class="hint">Drag nodes to reposition them before saving.</p>
        <DiagramCanvas nodes={diagramNodes} edges={diagramEdges} onNodeMove={moveNode} />
        <button class="primary" on:click={saveDiagram}>Save diagram</button>
      </div>
      <div>
        <h3>Existing diagrams</h3>
        <div class="diagram-list">
          {#each $diagrams as diagram (diagram.id)}
            <div class="diagram-item">
              <p><strong>ID:</strong> {diagram.id}</p>
              <button on:click={() => shareDiagram(diagram.id)}>Share to display</button>
              <DiagramCanvas nodes={diagram.nodes} edges={diagram.edges} readonly />
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .page {
    padding: 24px;
    color: #e8f0ff;
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  header h1 {
    margin: 0;
  }
  header p {
    margin: 4px 0 0;
    color: #b3c6e0;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 16px;
  }
  .panel {
    background: #0f1c2e;
    border: 1px solid #1e3a5f;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
  label {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 12px;
    color: #b3c6e0;
  }
  input,
  textarea,
  select {
    padding: 8px;
    border-radius: 6px;
    border: 1px solid #1e3a5f;
    background: #0f253b;
    color: #e8f0ff;
  }
  button {
    padding: 10px 14px;
    border-radius: 6px;
    border: none;
    background: #1e88e5;
    color: white;
    font-weight: 600;
  }
  button.primary {
    margin-top: 8px;
    width: 100%;
  }
  .note-list {
    display: grid;
    gap: 12px;
  }
  article {
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 12px;
    background: #0f253b;
  }
  .note-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
  .toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
  }
  .diagram-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 16px;
  }
  .diagram-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .diagram-item {
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 12px;
    background: #0f253b;
  }
  .edge-form {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin: 8px 0;
  }
  .hint {
    color: #b3c6e0;
    font-size: 0.9rem;
  }
  .banner {
    background: #ffcdd2;
    color: #b71c1c;
    padding: 10px;
    border-radius: 8px;
  }
  @media (max-width: 600px) {
    .note-head {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>
