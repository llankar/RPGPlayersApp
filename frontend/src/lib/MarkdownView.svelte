<script lang="ts">
  import { marked } from 'marked';
  export let markdown: string = '';
</script>

<div class="markdown">{@html marked.parse(markdown)}</div>

<style>
  .markdown {
    background: #0f253b;
    padding: 12px;
    border-radius: 8px;
    color: #e8f0ff;
    line-height: 1.6;
  }
  :global(.markdown h1),
  :global(.markdown h2),
  :global(.markdown h3) {
    color: #bbdefb;
  }
  :global(.markdown a) {
    color: #90caf9;
  }
</style>
