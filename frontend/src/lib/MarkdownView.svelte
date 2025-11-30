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
  .markdown h1,
  .markdown h2,
  .markdown h3 {
    color: #bbdefb;
  }
  .markdown a {
    color: #90caf9;
  }
</style>
