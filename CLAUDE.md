# Concept Atlas

A single-file static HTML app that takes any academic topic and produces a concept graph + canonical works + staged reading order.

## File

- **`concept-atlas.html`** — the entire app (~1400 lines, single file, no build step, no backend)

## What it does

Enter any academic topic (e.g. "Machine Learning") → get:

1. **Concept graph** (left pane) — prerequisites, core concepts, and next-level successors. Each concept links to OpenAlex. Load-bearing concepts only, no padding.
2. **Canonical works per concept** (center pane) — 3-5 genuinely canonical works per concept, categorized as seminal / breakthrough / pedagogical, with Google Scholar links. Claude curates the canon directly (not OpenAlex — OpenAlex's title.search was too literal and missed canonical textbooks).
3. **Staged reading order** (right pane) — works arranged into stages. Items within a stage can be read in parallel; stages are strictly sequential. Each item has a forward-facing bridge sentence.

## Architecture

- **Single static HTML file** — vanilla HTML/CSS/JS, no framework, no build step
- **Anthropic Claude API** — user-supplied key, called browser-side via `anthropic-dangerous-direct-browser-access` header
- **OpenAlex API** — optional, user-supplied key, used only for concept tag enrichment (not for works)
- **IndexedDB** — topic-keyed cache so repeat queries load instantly
- **Streaming** — Anthropic SSE for Stages 1 and 3 (concept graph and reading sequence)

## Generation flow

1. **Stage 1**: Claude generates concept graph (predecessors / core / successors) — streamed
2. **Stage 1b**: OpenAlex concept tags fetched per concept (parallel, if key present)
3. **Stage 2**: Claude generates canonical works per concept (parallel, 3-5 works each)
4. **Stage 3**: Claude sequences all works into staged reading order — streamed

## Key design choices

- **No OpenAlex for works** — Claude curates the canon directly. OpenAlex's title.search missed canonical textbooks whose titles don't contain the exact concept name (e.g. Strang's "Introduction to Linear Algebra" doesn't title-match "Linear Algebra").
- **No numerical caps** — prompts say "include ONLY genuinely canonical/load-bearing items. No numerical cap. Do not pad." The count is whatever the quality bar produces.
- **Google Scholar links on every work** — no API key needed, just `scholar.google.com/scholar?q=<title>`
- **Concept names hyperlink to OpenAlex** — `openalex.org/concepts?search=<name>` (no key needed)
- **Corrections UI** — users can add missing works, mark wrong edges, add missing concepts. All corrections persist in IndexedDB.

## API keys needed

- **Anthropic API key** (required) — for Claude calls
- **OpenAlex API key** (optional) — only for concept tag enrichment

Both are entered in the header and persisted to localStorage.

## How to run

Open `concept-atlas.html` directly in a browser, or serve the folder locally. No build step.

## How to deploy

The app is a single static HTML file. For Railway deployment, a minimal Node.js server (`server.js`) serves the file. See `server.js` and `package.json`.

## Tech stack

- Vanilla HTML/CSS/JS (no framework, no build step)
- Anthropic Messages API (Claude)
- OpenAlex API (concepts endpoint, optional)
- IndexedDB for persistence
- SSE streaming via fetch + ReadableStream
