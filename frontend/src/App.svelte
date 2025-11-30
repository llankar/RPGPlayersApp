<script lang="ts">
  import Router from 'svelte-spa-router';
  import Player from './routes/player.svelte';
  import Display from './routes/display.svelte';

  const routes = {
    '/': Player,
    '/player': Player,
    '/display': Display
  };
</script>

<main>
  <Router {routes} />
</main>
