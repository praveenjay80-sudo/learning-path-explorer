# Reading Map Generator — Design

## Summary

A new single-file static HTML app, `reading-map.html`, in the same family as `research-explorer.html` and `concept-atlas.html`. Given any topic typed in free text, it generates an immensely complete, staged reading map covering both books and papers, dynamically via a user-supplied OpenRouter API key.

## Goals

- Free-text topic input — not limited to a fixed list, reusable for any subject.
- "Immensely complete": breadth (all major subtopics covered) and depth (staged progression from orientation to frontier) in one generation.
- Every entry explicitly tagged as a **book** or a **paper**, with a working outbound link.
- Same architectural family as the existing two apps: no build step, vanilla JS, IndexedDB cache, SSE streaming.

## Non-goals

- No fixed taxonomy/dropdown menu (that pattern already exists in `reading-list-generator.html`).
- No support for additional work types beyond book/paper (no courses, videos, lecture notes).
- No backend changes — this is a static file; `server.js` routing is out of scope unless the user later asks to wire up a route.

## Architecture

- Single static file, vanilla HTML/CSS/JS, no framework, no build step.
- API: OpenRouter (`https://openrouter.ai/api/v1/chat/completions`), model `anthropic/claude-sonnet-4-6` — same call pattern as `reading-list-generator.html`.
- API key entered by user, persisted to `localStorage`.
- IndexedDB cache keyed by normalized topic string (lowercased, trimmed) — repeat topics load instantly without re-calling the API.
- Streaming via `fetch` + `ReadableStream`, consistent with the other two apps.

## Generation flow (two passes, both streamed)

**Pass 1 — Breadth (subtopic map)**
- Prompt: given the topic, enumerate the full set of subtopics/subfields a genuinely complete treatment must cover.
- Returns JSON: `{ "subtopics": [{ "name": string, "description": string }] }`
- Rendered immediately as a chip row so the user sees coverage scope before depth generation starts.
- Saved to IndexedDB as soon as it completes (cache resilience: if pass 2 is interrupted, reopening the topic re-runs only pass 2).

**Pass 2 — Depth (staged reading sequence)**
- Prompt: given the topic AND the pass-1 subtopic list, build the staged reading map. Must explicitly cover every subtopic from pass 1 somewhere in the sequence. No artificial caps — include as many works as the topic genuinely warrants.
- Stage vocabulary (adapt per topic, not all stages required): Orientation & Landscape, Core Foundations, Seminal Works, Breakthroughs & Advances, Modern Synthesis, Contemporary Frontiers. Optional: Methodological Foundations, Historical & Philosophical Context, Interdisciplinary Bridges, Open Problems & Future Directions, Application Domains.
- Returns JSON: `{ "stages": [{ "label": string, "summary": string, "works": [{ "title": string, "author": string, "year": string|number, "type": "book"|"paper", "description": string, "role": string }] }] }`
- `role` is a short functional label (e.g. "seminal paper", "standard textbook", "key breakthrough", "definitive survey") — free text, same convention as the existing generator.
- Client-side (not model-generated) link construction per work: papers → Google Scholar search URL from title+author; books → Google Books search URL from title+author. Avoids hallucinated URLs.
- Full result (subtopics + stages) saved to IndexedDB once pass 2 completes.

## UI

- Top: topic text input, Generate button, OpenRouter API key input (password field, persisted).
- Subtopic-coverage strip: chips showing pass-1 output, rendered as soon as available.
- Staged reading map: each stage rendered as a colored section (stage header with number + label + summary, reusing `reading-list-generator.html`'s visual language), each work shown with title/author/year, a BOOK/PAPER badge, role badge, description, and a link icon/button.
- Stats bar: total stages · total works · book count vs paper count.
- Filter toggle: All / Books only / Papers only.
- Dark/light theme via `prefers-color-scheme`, matching the existing apps.

## Error handling

- Missing/invalid API key: inline status message; Generate stays disabled until a key is present.
- Stream/fetch failure on either pass: caught per-pass, shown as an error state with a "regenerate this pass" button that retries only the failed pass (does not re-run a pass that already succeeded).
- Malformed JSON from the model: caught, shown as an error state with a regenerate option rather than crashing the render.

## Testing / verification

No test framework in this repo (consistent with the other single-file apps). Verification is manual:
1. Open `reading-map.html` directly in a browser.
2. Enter a real OpenRouter key.
3. Generate a map for one of: microeconomics, game theory, psychology, persuasion, ethics, mathematics, computers.
4. Confirm both passes stream and render correctly, in order.
5. Reload the page, re-enter the same topic, confirm it loads instantly from IndexedDB cache.
6. Confirm book/paper badges are correctly assigned and links resolve to sensible Google Scholar / Google Books searches.
7. Confirm the books-only / papers-only filter toggle works.
