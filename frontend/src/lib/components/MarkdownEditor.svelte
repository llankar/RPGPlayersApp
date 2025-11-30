<script lang="ts">
  import MarkdownView from '$lib/MarkdownView.svelte';

  /**
   * Small helper component that wraps a textarea with a live Markdown preview.
   * The parent component owns the value through bind:value to keep things simple.
   */
  export let label: string = 'Body';
  export let placeholder: string = 'Write using Markdown...';
  export let value: string = '';
</script>

<div class="markdown-editor">
  <label>
    <span>{label}</span>
    <textarea rows="8" bind:value placeholder={placeholder}></textarea>
  </label>
  <div class="preview">
    <p class="hint">Live preview</p>
    <MarkdownView markdown={value || '_Start typing to see formatted text..._'} />
  </div>
</div>

<style>
  .markdown-editor {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 12px;
  }
  label {
    display: flex;
    flex-direction: column;
    gap: 8px;
    color: #b3c6e0;
  }
  textarea {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #1e3a5f;
    background: #0f253b;
    color: #e8f0ff;
    min-height: 200px;
  }
  .preview {
    background: #0f1c2e;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 10px;
  }
  .hint {
    margin: 0 0 6px 0;
    color: #7fa4ce;
    font-size: 0.9rem;
  }
</style>
