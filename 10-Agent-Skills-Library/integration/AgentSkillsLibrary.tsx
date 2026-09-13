import { useEffect, useRef } from 'react';
import type { SkillCatalog } from '../agent-skills-library';
import '../agent-skills-library.js';
import '../agent-skills-library.css';

interface Props {
  catalog: SkillCatalog;
  libraryBase: string;
  assetBase: string;
  selectionStorageKey: string;
}

/** Host adapter only. Runtime execution and authorization belong to the host. */
export function AgentSkillsLibrary({ catalog, libraryBase, assetBase, selectionStorageKey }: Props) {
  const container = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!container.current) return;
    const library = globalThis.AgentSkillsLibrary.mount(container.current, {
      catalog, libraryBase, assetBase, hashRouting: false,
      persistKey: selectionStorageKey,
    });
    return () => library.destroy();
  }, [catalog, libraryBase, assetBase, selectionStorageKey]);
  return <div ref={container} />;
}
