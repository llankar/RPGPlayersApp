import { readable } from 'svelte/store';
import { whiteboards } from '../state';
import type { Whiteboard } from '../types';

/**
 * Simple collaboration hook that mirrors the shared whiteboard store and emits
 * the most recent version to subscribers whenever a remote update arrives.
 */
export function useCollaborationChannel(boardId: string) {
  return readable<Whiteboard | undefined>(undefined, (set) => {
    const unsubscribe = whiteboards.subscribe((list) => {
      set(list.find((board) => board.id === boardId));
    });
    return unsubscribe;
  });
}
