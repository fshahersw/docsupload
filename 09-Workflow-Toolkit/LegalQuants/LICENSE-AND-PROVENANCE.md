# License and provenance boundaries

The packet preserves original Git blob bytes. `REUSE-MANIFEST.json` gives source commit, Git blob SHA-1, SHA-256, byte count and license path for every file. No upstream file in the packet was edited. New review documents and workflow design contracts are separate from those originals.

## First-party lq-ai material

The root [LICENSE](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/LICENSE) grants Apache-2.0 rights for the covered code. The packet retains that license and [NOTICES.md](https://github.com/LegalQuants/lq-ai/blob/2cc3149238defbbb171ec845cd0d3a43a34054f2/NOTICES.md). The separately licensed web application is outside this packet.

For redistribution or modification, preserve required copyright/attribution notices and the license copy; mark subsequent modifications. This review does not grant trademark rights or rights in separate dependencies, source documents, private databases, models, credentials or hosted services.

The five YAML playbooks are explicitly described by their authors as unvetted starters. Their positions must not become firm-approved legal standards automatically.

| Playbook | Packet treatment | Provenance detail |
|---|---|---|
| NDA — Mutual | Copied unchanged | Authored starter under root license; no additional embedded third-party-source notice observed |
| NDA — Unilateral | Copied unchanged | Authored starter under root license; no additional embedded third-party-source notice observed |
| MSA — SaaS | Catalog only | Its header names Common Paper Cloud Service Agreement and Bonterms Software License terms under CC BY 4.0; exact derived versions/line mapping are not stated |
| MSA — Commercial Purchase | Catalog only | Header names a Common Paper “Master Subscription Agreement”; the exact referenced source/version was not established in this review |
| DPA — GDPR | Catalog only | Header names European Commission SCCs and EDPB guidelines; original source reuse terms and incorporated passages have not been mapped |

The source publishers confirm that [Common Paper standards](https://commonpaper.com/standards) and [Bonterms Software License Terms v1.0](https://bonterms.com/forms/software-license-terms-v1) use CC BY 4.0. That supports the attribution requirement; it does not establish which exact version or text the lq-ai authors adapted. Do not relabel incorporated CC BY content as solely Apache. See the [CC BY 4.0 terms](https://creativecommons.org/licenses/by/4.0/) when a verified adaptation is later added.

## Community gitlink

The parent submodule points to `a293659770c6d9094e3f9893a0de6e59475e95b6`. It was cloned separately and checked out at that exact commit. The community [README license section](https://github.com/LegalQuants/lq-skills/blob/a293659770c6d9094e3f9893a0de6e59475e95b6/README.md#license) states that folder licenses override the project Apache-2.0 default; folders without an override inherit that default. Each inventory entry records the nearest actual LICENSE file and credited authorship.

Among selected community folders:

- `adversarial-qc`: MIT; copyright Alexios van der Slikke-Kirillov.
- `coquill` and its three internal folders: MIT; copyright Ang Hou Fu. All four license files are retained.
- `legal-translation`: MIT; copyright Arjun Singh Chouhan.
- The selected AnonLQ litigation skills retain their local Apache-2.0 license files.
- Selected governance skills inherit the community root Apache-2.0 license.

MIT copyright and permission notices remain in the packet. No selected skill had an unresolved local license. Other community material is cataloged rather than copied when its relevance or implementation maturity is weak; that is not a finding that its license forbids reuse.

CoQuill's bundled Bonterms DOCX and all its example template directories are excluded. They are separate template/provenance inputs, not an approved firm form library. Its unchanged README still describes those upstream examples; the packet manifest is authoritative about what is actually included.

The `office-word-diff`, `superdoc-redlines`, `redlines`, `text-provenance`, `sgcite`, BART and Vibe Legal skill descriptions do not bring those external tools' implementations or licenses into this packet. Review the actual dependency repositories and exact versions before adopting them.

## Future changes

Keep the upstream snapshot immutable. Place adapted skills under a firm namespace with a new version, explicit original-source links, modification notice and evaluation record. Resolve duplicate names deliberately: in particular, community `nda-review` is a different author's unilateral workflow, while the parent variant supports mutual review. Never flatten the two repositories into one directory and let the last copied file win.
