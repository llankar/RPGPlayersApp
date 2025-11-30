<script lang="ts">
  import Konva from 'konva';
  import { onDestroy, onMount } from 'svelte';
  import type { DiagramEdge, DiagramNode } from './types';

  export let nodes: DiagramNode[] = [];
  export let edges: DiagramEdge[] = [];
  export let readonly: boolean = false;
  export let onNodeMove: (id: string, x: number, y: number) => void = () => {};

  let container: HTMLDivElement;
  let stage: Konva.Stage;
  let layer: Konva.Layer;

  const draw = () => {
    if (!stage || !layer) return;
    layer.destroyChildren();

    // Draw edges first so nodes appear on top.
    edges.forEach((edge) => {
      const source = nodes.find((n) => n.id === edge.source_id);
      const target = nodes.find((n) => n.id === edge.target_id);
      if (!source || !target) return;
      const line = new Konva.Arrow({
        points: [source.x, source.y, target.x, target.y],
        pointerLength: 10,
        pointerWidth: 10,
        stroke: '#90caf9',
        fill: '#90caf9',
        strokeWidth: 2
      });
      layer.add(line);
    });

    // Draw nodes as draggable circles with labels.
    nodes.forEach((node) => {
      const circle = new Konva.Circle({
        x: node.x,
        y: node.y,
        radius: 24,
        fill: '#1e3a5f',
        stroke: '#90caf9',
        strokeWidth: 2,
        draggable: !readonly
      });
      const label = new Konva.Text({
        x: node.x - 20,
        y: node.y - 8,
        width: 40,
        align: 'center',
        text: node.label,
        fill: '#e8f0ff',
        fontSize: 12
      });

      if (!readonly) {
        circle.on('dragend', (e) => {
          const pos = e.target.position();
          onNodeMove(node.id, pos.x, pos.y);
        });
      }

      layer.add(circle);
      layer.add(label);
    });

    layer.draw();
  };

  const resizeStage = () => {
    if (!stage || !container) return;
    stage.width(container.clientWidth);
    stage.height(400);
    draw();
  };

  onMount(() => {
    stage = new Konva.Stage({
      container,
      width: container.clientWidth || 600,
      height: 400
    });
    layer = new Konva.Layer();
    stage.add(layer);
    draw();
    window.addEventListener('resize', resizeStage);
  });

  onDestroy(() => {
    window.removeEventListener('resize', resizeStage);
    stage?.destroy();
  });

  $: {
    // Redraw whenever the diagram inputs or readonly flag change.
    nodes;
    edges;
    readonly;
    if (stage && layer) {
      draw();
    }
  }
</script>

<div class="diagram-frame" bind:this={container}></div>

<style>
  .diagram-frame {
    width: 100%;
    border: 1px solid #1e3a5f;
    background: #0f253b;
    border-radius: 8px;
    overflow: hidden;
  }
</style>
