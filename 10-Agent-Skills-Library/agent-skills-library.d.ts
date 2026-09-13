export interface SkillInput { name: string; required: boolean; description: string }
export interface SkillSource {
  repo: string | null; url: string | null; commit: string | null; path: string;
  license: string; sha256: string | null; included_path: string | null;
}
export interface SkillRecord {
  id: string; title: string; kind: 'agent' | 'skill' | 'workflow'; origin: string;
  category: string; roles: string[]; summary: string; description: string;
  when_to_use: string[]; inputs: SkillInput[]; steps: string[]; outputs: string[];
  examples: string[]; checks: string[]; limits: string[]; tool_requirements: string[];
  jurisdiction: string; readiness: string; source: SkillSource;
  files: Array<{ label: string; path?: string; url?: string }>;
  instructions: string | null; instructions_sha256: string | null; instruction_path: string | null;
  platform?: { areas: string[]; target_origin: string; deployed_verified: false; [key: string]: unknown };
  input_schema?: Record<string, unknown>; output_schema?: Record<string, unknown>;
  tool_bindings?: unknown; evaluation_cases?: unknown; legacy_ids?: string[];
  related_ids: string[]; source_prompt?: string | null; source_prompt_note?: string;
  profile_kind?: 'specialist' | 'orchestrator' | 'profile_only';
  editorial_notes?: string | string[]; strengths?: string[]; practice_areas?: string[];
  runtime_installed: false; legal_accuracy_evaluated: false;
  [key: string]: unknown;
}
export interface SkillCatalog { schema_version: string; title: string; records: SkillRecord[]; [key: string]: unknown }
export interface LibraryHandle { destroy(): void; select(id: string): boolean; getSelection(): SkillRecord[] }
export interface LibraryOptions {
  catalog: SkillCatalog; libraryBase?: string; assetBase?: string;
  hashRouting?: boolean; persistKey?: string;
}
declare global {
  var AgentSkillsLibrary: { mount(root: HTMLElement, options: LibraryOptions): LibraryHandle };
}
