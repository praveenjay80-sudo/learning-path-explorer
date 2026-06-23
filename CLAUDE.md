# Academic Research Tools

Two single-file static HTML apps powered by the Anthropic Claude API. No build step, no backend dependencies — vanilla HTML/CSS/JS served by a minimal Node.js server for Railway deployment.

---

## Apps

### 1. Research Explorer — `research-explorer.html`

Enter any research question → get a full concept map, staged reading list, and a synthesized answer — all anchored to the specific question.

**Three tabs:**

1. **Question Generator** — enter an academic field (+ optional sub-topic) → tiered question bank from Foundational through Research level. Each question includes an explanation of what a complete answer covers, prerequisite concepts, and a difficulty rating.

2. **Research Explorer** — enter a research question → two panes:
   - *Left*: all load-bearing concepts with plain-language explanation + how each concept addresses the question
   - *Right*: reading list organized into sequential stages (works within a stage are parallel); each work has a plain-language summary, "how it answers your question" paragraph, prerequisite chips, and a Google Scholar link

3. **Answer** — synthesized 3–5 paragraph answer to the research question, with inline clickable links to concepts (purple) and works (blue) that jump to the Research Explorer tab

**Generation flow (3 stages, all streamed):**
1. Claude generates concept list — saved to IndexedDB immediately
2. Claude generates staged reading list — saved to IndexedDB immediately
3. Claude writes synthesized answer — full state saved to IndexedDB

**Cache resilience:** if generation is interrupted at any stage, the next run resumes from where it left off (no repeated API calls for already-completed stages).

---

### 2. Concept Atlas — `concept-atlas.html`

Enter any academic topic → concept graph + canonical works + staged reading order.

**Three panes:**
1. *Left*: concept graph — prerequisites, core concepts, successors. Each concept links to OpenAlex.
2. *Center*: canonical works per concept — seminal / breakthrough / pedagogical, with Google Scholar links
3. *Right*: staged reading sequence — parallel within stage, sequential between stages, with bridge sentences

**Generation flow (3 stages, streamed):**
1. Claude generates concept graph — streamed
2. OpenAlex concept tags fetched per concept (parallel, optional)
3. Claude generates canonical works per concept (parallel)
4. Claude sequences all works into staged reading order — streamed

---

## Architecture (both apps)

- **Single static HTML files** — vanilla HTML/CSS/JS, no framework, no build step
- **Anthropic Claude API** — user-supplied key, called browser-side via `anthropic-dangerous-direct-browser-access` header
- **IndexedDB** — query-keyed cache so repeat queries load instantly
- **Streaming** — Anthropic SSE via fetch + ReadableStream

## API keys

- **Anthropic API key** (required) — for all Claude calls; entered in header, persisted to localStorage
- **OpenAlex API key** (optional, Concept Atlas only) — for concept tag enrichment

## Routes (server.js)

- `/` → `research-explorer.html` (main app)
- `/research-explorer` → `research-explorer.html`
- `/concept-atlas` → `concept-atlas.html`

## How to run locally

Open either HTML file directly in a browser. No build step needed.

## How to deploy

Push to GitHub — Railway auto-deploys via `node server.js`. See `railway.json`.

## Tech stack

- Vanilla HTML/CSS/JS (no framework, no build step)
- Anthropic Messages API (claude-sonnet-4-6 default)
- OpenAlex API (Concept Atlas only, optional)
- IndexedDB for persistence
- SSE streaming via fetch + ReadableStream
- Node.js (server.js, Railway only)
