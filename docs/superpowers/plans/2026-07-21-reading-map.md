# Reading Map Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `reading-map.html` — a single-file static app that takes any free-text topic and generates an immensely complete, staged reading map covering both books and papers, via a user-supplied OpenRouter API key.

**Architecture:** Vanilla HTML/CSS/JS, no build step, no framework. Two-pass streamed generation (breadth subtopic map, then staged depth reading sequence) against OpenRouter's `anthropic/claude-sonnet-4-6`. IndexedDB caches results per normalized topic key. Client-side link builders (not model output) produce Google Scholar / Google Books search URLs per work.

**Tech Stack:** Vanilla JS (ES2020+), `fetch` + `ReadableStream` for SSE, `indexedDB` for caching. Node.js only used offline to unit-test pure helper functions (this repo has no test framework or package.json test runner — see Global Constraints).

## Global Constraints

- Single static HTML file, no framework, no build step (per spec Architecture section).
- API: OpenRouter `https://openrouter.ai/api/v1/chat/completions`, model `anthropic/claude-sonnet-4-6` (per spec).
- API key input is `type=password`, persisted to `localStorage` (per spec UI section).
- IndexedDB cache keyed by normalized topic string, lowercased and trimmed (per spec Architecture section).
- Work types are exactly `"book"` or `"paper"` — no other type values (per spec Non-goals).
- Links are built client-side from title+author, never taken from model output (per spec Pass 2, "avoid hallucinated URLs").
- No test framework exists in this repo. Pure logic functions (no DOM/network) are verified with standalone `node` scripts written to the scratchpad directory and run directly. DOM/network-dependent behavior is verified manually in a browser per spec's Testing section.
- Dark/light theme via `prefers-color-scheme`, matching `research-explorer.html` / `concept-atlas.html` / `reading-list-generator.html`.
- All model-generated text (subtopic names/descriptions, work titles/authors/descriptions/roles) MUST pass through an `escapeHtml(str)` helper before being concatenated into any `innerHTML` string. Model output is untrusted for HTML-injection purposes even though it isn't direct user input. Added in Task 5 fix (post-review), applies to Task 5's `renderSubtopics` and Task 6's `workRowHtml`/`renderStages`.

---

### Task 1: File scaffold — HTML shell, theme CSS, layout

**Files:**
- Create: `C:\Users\prave\reading-map.html`

**Interfaces:**
- Produces: DOM elements later tasks attach behavior to — `#topicInput`, `#apiKey`, `#genBtn`, `#status`, `#subtopics`, `#statsBar`, `#filterBar`, `#results`.

- [ ] **Step 1: Write the HTML shell with theme CSS and static layout**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Reading Map Generator</title>
<style>
:root{
  --bg:#f5f6f8; --surface:#fff; --surface2:#eef0f4; --text:#1a1d23; --muted:#6b7280;
  --border:#e2e5ea; --accent:#4f46e5; --accent2:#0891b2; --book:#0891b2; --paper:#c2410c;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#0d1117; --surface:#161b22; --surface2:#21262d; --text:#e6edf3; --muted:#8b949e;
    --border:#30363d; --accent:#6366f1; --accent2:#06b6d4; --book:#22d3ee; --paper:#fb923c;
  }
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}
header{background:var(--surface);border-bottom:1px solid var(--border);padding:0.8rem 1.5rem;position:sticky;top:0;z-index:10;}
header h1{font-size:1.25rem;font-weight:800;letter-spacing:-0.02em;background:linear-gradient(135deg,#4f46e5,#0891b2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
header .sub{font-size:0.78rem;color:var(--muted);margin-top:0.15rem;}
main{max-width:960px;margin:0 auto;padding:1.25rem;}
.controls{display:flex;flex-direction:column;gap:0.6rem;margin-bottom:1rem;}
.row{display:flex;gap:0.6rem;flex-wrap:wrap;align-items:center;}
.row input[type=text]{flex:1;min-width:220px;padding:0.55rem 0.8rem;border-radius:6px;border:1px solid var(--border);background:var(--surface);color:var(--text);font-size:0.95rem;}
.row input[type=password]{flex:1;min-width:200px;max-width:320px;padding:0.45rem 0.7rem;border-radius:6px;border:1px solid var(--border);background:var(--surface);color:var(--text);font-size:0.88rem;}
.row button{background:var(--accent);color:#fff;border:none;padding:0.55rem 1.2rem;border-radius:6px;font-size:0.9rem;font-weight:600;cursor:pointer;white-space:nowrap;transition:background .15s;}
.row button:hover:not(:disabled){background:#4338ca;}
.row button:disabled{opacity:0.5;cursor:not-allowed;}
#status{font-size:0.85rem;color:var(--muted);min-height:1.3em;padding:0.3rem 0;}
#status.error{color:#dc2626;}
#status.info{color:var(--accent);}
#subtopics{display:flex;flex-wrap:wrap;gap:0.4rem;margin:0.6rem 0;}
.chip{background:var(--surface2);border:1px solid var(--border);color:var(--text);font-size:0.78rem;padding:0.25rem 0.6rem;border-radius:999px;}
#statsBar{font-size:0.82rem;color:var(--muted);padding:0.4rem 0;display:none;}
#statsBar.show{display:block;}
#filterBar{display:none;gap:0.4rem;margin-bottom:0.6rem;}
#filterBar.show{display:flex;}
#filterBar button{background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:0.3rem 0.8rem;border-radius:6px;font-size:0.8rem;cursor:pointer;}
#filterBar button.active{background:var(--accent);color:#fff;border-color:var(--accent);}
#results{margin-top:0.5rem;}
.stage{margin-bottom:1.2rem;border-radius:8px;overflow:hidden;border:1px solid var(--border);}
.stage-header{padding:0.5rem 0.9rem;font-weight:700;font-size:0.9rem;display:flex;align-items:center;gap:0.5rem;background:var(--accent);color:#fff;}
.stage-num{display:inline-flex;align-items:center;justify-content:center;background:rgba(255,255,255,0.22);font-weight:800;font-size:0.8rem;min-width:1.8rem;height:1.8rem;border-radius:4px;}
.stage-summary{padding:0.4rem 0.9rem;background:var(--surface2);color:var(--muted);font-size:0.82rem;font-style:italic;border-bottom:1px solid var(--border);}
.stage-body{background:var(--surface);padding:0.8rem 0.9rem;}
.work{margin-bottom:0.7rem;padding-bottom:0.7rem;border-bottom:1px solid var(--border);}
.work:last-child{margin-bottom:0;border-bottom:none;padding-bottom:0;}
.work .title{font-weight:600;color:var(--text);}
.work .author{color:var(--muted);font-size:0.82rem;}
.work .desc{font-size:0.84rem;color:var(--muted);margin-top:0.2rem;line-height:1.4;}
.badge{display:inline-block;font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.02em;padding:0.1rem 0.4rem;border-radius:3px;margin-right:0.35rem;vertical-align:middle;}
.badge.book{background:var(--book);color:#04222b;}
.badge.paper{background:var(--paper);color:#2b1200;}
.badge.role{background:var(--surface2);color:var(--accent);border:1px solid var(--border);}
.work a.link{font-size:0.78rem;color:var(--accent2);text-decoration:none;margin-left:0.3rem;}
.work a.link:hover{text-decoration:underline;}
.loading{text-align:center;padding:2rem;color:var(--muted);}
.retry-btn{background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:0.3rem 0.8rem;border-radius:6px;font-size:0.8rem;cursor:pointer;margin-top:0.4rem;}
</style>
</head>
<body>
<header>
  <h1>Reading Map Generator</h1>
  <div class="sub">Enter any topic → complete staged reading map, books and papers, all levels</div>
</header>
<main>
  <div class="controls">
    <div class="row">
      <input type="text" id="topicInput" placeholder="e.g. game theory, persuasion, ethics..." />
      <button id="genBtn" disabled>Generate</button>
    </div>
    <div class="row">
      <input type="password" id="apiKey" placeholder="OpenRouter API Key (sk-or-...)" />
    </div>
    <div id="status"></div>
  </div>
  <div id="subtopics"></div>
  <div id="statsBar"></div>
  <div id="filterBar">
    <button data-filter="all" class="active">All</button>
    <button data-filter="book">Books only</button>
    <button data-filter="paper">Papers only</button>
  </div>
  <div id="results"></div>
</main>
<script>
</script>
</body>
</html>
```

- [ ] **Step 2: Manual verification — open in browser**

Open `C:\Users\prave\reading-map.html` directly in a browser (double-click or `start reading-map.html` from that directory).

Expected: header renders with gradient title, topic input + Generate button + API key row are visible, Generate button is disabled (no `onclick`/enable logic wired yet — that's expected at this stage), dark/light theme matches OS setting.

- [ ] **Step 3: Commit**

```bash
git add reading-map.html
git commit -m "Scaffold reading-map.html shell and theme CSS"
```

---

### Task 2: Pure helper functions — topic key, link builders

**Files:**
- Modify: `C:\Users\prave\reading-map.html` (inside the empty `<script>` tag from Task 1)
- Test (scratch, not committed): `C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\4e81d10c-2b14-4b96-ba05-4bfaaf9ae5c3\scratchpad\test-helpers.mjs`

**Interfaces:**
- Consumes: nothing (pure functions).
- Produces: `normalizeTopicKey(topic)`, `scholarLink(title, author)`, `booksLink(title, author)` — used by Task 3 (cache keys) and Task 6 (work links).

- [ ] **Step 1: Write the pure helper functions into the script tag**

```html
<script>
// ── Pure helpers ─────────────────────────────────────────
function normalizeTopicKey(topic) {
  return topic.trim().toLowerCase().replace(/\s+/g, ' ');
}

function scholarLink(title, author) {
  const q = encodeURIComponent([title, author].filter(Boolean).join(' '));
  return 'https://scholar.google.com/scholar?q=' + q;
}

function booksLink(title, author) {
  const q = encodeURIComponent([title, author].filter(Boolean).join(' '));
  return 'https://www.google.com/search?tbm=bks&q=' + q;
}
</script>
```

- [ ] **Step 2: Write a standalone node test for these functions**

Create `test-helpers.mjs` in the scratchpad directory:

```javascript
function normalizeTopicKey(topic) {
  return topic.trim().toLowerCase().replace(/\s+/g, ' ');
}
function scholarLink(title, author) {
  const q = encodeURIComponent([title, author].filter(Boolean).join(' '));
  return 'https://scholar.google.com/scholar?q=' + q;
}
function booksLink(title, author) {
  const q = encodeURIComponent([title, author].filter(Boolean).join(' '));
  return 'https://www.google.com/search?tbm=bks&q=' + q;
}

function assertEqual(actual, expected, label) {
  if (actual !== expected) {
    console.error('FAIL:', label, '\n  got:', actual, '\n  want:', expected);
    process.exitCode = 1;
  } else {
    console.log('PASS:', label);
  }
}

assertEqual(normalizeTopicKey('  Game Theory  '), 'game theory', 'normalizeTopicKey trims and lowercases');
assertEqual(normalizeTopicKey('Micro   Economics'), 'micro economics', 'normalizeTopicKey collapses whitespace');
assertEqual(
  scholarLink('Prospect Theory', 'Kahneman & Tversky'),
  'https://scholar.google.com/scholar?q=' + encodeURIComponent('Prospect Theory Kahneman & Tversky'),
  'scholarLink builds correct search URL'
);
assertEqual(
  booksLink('Influence', 'Cialdini'),
  'https://www.google.com/search?tbm=bks&q=' + encodeURIComponent('Influence Cialdini'),
  'booksLink builds correct search URL'
);
assertEqual(scholarLink('Solo Title', ''), 'https://scholar.google.com/scholar?q=' + encodeURIComponent('Solo Title'), 'scholarLink handles missing author');
```

- [ ] **Step 3: Run the test**

Run: `node "C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\4e81d10c-2b14-4b96-ba05-4bfaaf9ae5c3\scratchpad\test-helpers.mjs"`

Expected: five `PASS:` lines, exit code 0.

- [ ] **Step 4: Commit**

```bash
git add reading-map.html
git commit -m "Add pure helpers: topic key normalization and link builders"
```

---

### Task 3: IndexedDB cache helpers

**Files:**
- Modify: `C:\Users\prave\reading-map.html`

**Interfaces:**
- Consumes: `normalizeTopicKey` (Task 2).
- Produces: `getCached(topicKey)` returns `Promise<object|undefined>`; `putCached(topicKey, data)` returns `Promise<void>` — used by Task 7 (cache integration).

- [ ] **Step 1: Add IndexedDB helpers to the script tag**

```html
<script>
// ── IndexedDB cache ──────────────────────────────────────
const DB_NAME = 'reading-map-cache';
const STORE_NAME = 'topics';

function openCacheDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      req.result.createObjectStore(STORE_NAME, { keyPath: 'key' });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function getCached(topicKey) {
  const db = await openCacheDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readonly');
    const req = tx.objectStore(STORE_NAME).get(topicKey);
    req.onsuccess = () => resolve(req.result ? req.result.data : undefined);
    req.onerror = () => reject(req.error);
  });
}

async function putCached(topicKey, data) {
  const db = await openCacheDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    tx.objectStore(STORE_NAME).put({ key: topicKey, data });
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}
</script>
```

- [ ] **Step 2: Manual verification in browser devtools**

Open `reading-map.html` in a browser, open devtools console, run:

```javascript
await putCached('game theory', { subtopics: [{name: 'test', description: 'x'}] });
await getCached('game theory');
```

Expected: second call returns `{subtopics: [{name: 'test', description: 'x'}]}`. Then run `await getCached('nonexistent topic')` — expected: `undefined`.

- [ ] **Step 3: Commit**

```bash
git add reading-map.html
git commit -m "Add IndexedDB cache helpers (getCached/putCached)"
```

---

### Task 4: SSE line parser (pure) + streaming fetch helper

**Files:**
- Modify: `C:\Users\prave\reading-map.html`
- Test (scratch): `C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\4e81d10c-2b14-4b96-ba05-4bfaaf9ae5c3\scratchpad\test-sse.mjs`

**Interfaces:**
- Consumes: nothing new.
- Produces: `parseSSELine(line)` returns `string|null` (the delta text, or `null` if the line isn't a content delta or is `[DONE]`); `streamChatCompletion(apiKey, messages, onDelta)` returns `Promise<string>` (full accumulated text) and calls `onDelta(fullTextSoFar)` on every chunk — used by Task 5 and Task 6.

- [ ] **Step 1: Add the pure SSE line parser**

```html
<script>
// ── SSE parsing (pure) ───────────────────────────────────
function parseSSELine(line) {
  if (!line.startsWith('data: ')) return null;
  const payload = line.slice(6).trim();
  if (payload === '[DONE]') return null;
  try {
    const json = JSON.parse(payload);
    const delta = json.choices?.[0]?.delta?.content;
    return typeof delta === 'string' ? delta : null;
  } catch {
    return null;
  }
}
</script>
```

- [ ] **Step 2: Test the parser standalone**

Create `test-sse.mjs` in the scratchpad directory:

```javascript
function parseSSELine(line) {
  if (!line.startsWith('data: ')) return null;
  const payload = line.slice(6).trim();
  if (payload === '[DONE]') return null;
  try {
    const json = JSON.parse(payload);
    const delta = json.choices?.[0]?.delta?.content;
    return typeof delta === 'string' ? delta : null;
  } catch {
    return null;
  }
}

function assertEqual(actual, expected, label) {
  if (actual !== expected) {
    console.error('FAIL:', label, '\n  got:', actual, '\n  want:', expected);
    process.exitCode = 1;
  } else {
    console.log('PASS:', label);
  }
}

assertEqual(parseSSELine('data: {"choices":[{"delta":{"content":"hi"}}]}'), 'hi', 'parses content delta');
assertEqual(parseSSELine('data: [DONE]'), null, 'DONE returns null');
assertEqual(parseSSELine(': keep-alive'), null, 'non-data line returns null');
assertEqual(parseSSELine('data: not json'), null, 'malformed JSON returns null instead of throwing');
assertEqual(parseSSELine('data: {"choices":[{"delta":{}}]}'), null, 'missing content field returns null');
```

- [ ] **Step 3: Run the test**

Run: `node "C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\4e81d10c-2b14-4b96-ba05-4bfaaf9ae5c3\scratchpad\test-sse.mjs"`

Expected: five `PASS:` lines, exit code 0.

- [ ] **Step 4: Add the streaming fetch helper (network-dependent, manual verification only)**

```html
<script>
// ── Streaming OpenRouter call ────────────────────────────
async function streamChatCompletion(apiKey, messages, onDelta) {
  const resp = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + apiKey,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'anthropic/claude-sonnet-4-6',
      messages,
      stream: true
    })
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error('OpenRouter error ' + resp.status + ': ' + text);
  }
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let full = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop();
    for (const line of lines) {
      const delta = parseSSELine(line);
      if (delta) {
        full += delta;
        onDelta(full);
      }
    }
  }
  return full;
}
</script>
```

- [ ] **Step 5: Manual verification with a real API key**

In the browser console (on the open `reading-map.html` page), with a real OpenRouter key:

```javascript
await streamChatCompletion(
  'sk-or-...',
  [{ role: 'user', content: 'Say the word "test" and nothing else.' }],
  (text) => console.log('chunk so far:', text)
);
```

Expected: multiple `chunk so far:` logs with growing text, final resolved value contains "test".

- [ ] **Step 6: Commit**

```bash
git add reading-map.html
git commit -m "Add SSE parser and OpenRouter streaming helper"
```

---

### Task 5: Pass 1 — breadth prompt, generation, and chip rendering

**Files:**
- Modify: `C:\Users\prave\reading-map.html`

**Interfaces:**
- Consumes: `streamChatCompletion` (Task 4), `#subtopics` div (Task 1).
- Produces: `buildBreadthPrompt(topic)` returns `string`; `runPass1(topic, apiKey)` returns `Promise<Array<{name:string, description:string}>>` and renders chips as it streams — used by Task 6 and Task 7.

- [ ] **Step 1: Add the breadth prompt builder and pass-1 runner**

```html
<script>
// ── Pass 1: breadth ──────────────────────────────────────
function buildBreadthPrompt(topic) {
  return `You are an expert academic librarian mapping the full breadth of "${topic}".

List every major subtopic, subfield, or branch a genuinely complete treatment of "${topic}" must cover. Think broadly: core theory, methodology, historical development, major schools of thought, applied domains, and adjacent areas that serious students are expected to know.

Return ONLY a JSON object with exactly one key "subtopics": an array of objects, each with:
  - "name" (2-6 words)
  - "description" (1 sentence: what this subtopic covers)

No artificial caps — include every subtopic that genuinely belongs. Return ONLY valid JSON, no markdown fences, no commentary.`;
}

function renderSubtopics(subtopics) {
  const el = document.getElementById('subtopics');
  el.innerHTML = subtopics.map(s => '<span class="chip" title="' +
    escapeHtml(s.description) + '">' + escapeHtml(s.name) + '</span>').join('');
}

async function runPass1(topic, apiKey) {
  const raw = await streamChatCompletion(
    apiKey,
    [{ role: 'user', content: buildBreadthPrompt(topic) }],
    () => {} // pass 1 renders only once parsed (JSON isn't safely partial-parseable mid-stream)
  );
  const parsed = JSON.parse(raw);
  renderSubtopics(parsed.subtopics);
  return parsed.subtopics;
}
</script>
```

- [ ] **Step 2: Manual verification**

In the browser console with a real key:

```javascript
await runPass1('game theory', 'sk-or-...');
```

Expected: the `#subtopics` div in the page fills with chips like "Zero-Sum Games", "Cooperative Game Theory", "Mechanism Design", etc., and the function resolves to that same array.

- [ ] **Step 3: Commit**

```bash
git add reading-map.html
git commit -m "Add pass 1 breadth generation and subtopic chip rendering"
```

---

### Task 6: Pass 2 — staged depth prompt, generation, and stage rendering

**Files:**
- Modify: `C:\Users\prave\reading-map.html`

**Interfaces:**
- Consumes: `streamChatCompletion` (Task 4), `scholarLink`/`booksLink` (Task 2), `escapeHtml` (added in Task 5's post-review fix — read the current file to confirm it exists before using it), `#results` div (Task 1).
- Produces: `buildDepthPrompt(topic, subtopics)` returns `string`; `runPass2(topic, subtopics, apiKey)` returns `Promise<Array<Stage>>` where `Stage = {label, summary, works: [{title, author, year, type, description, role}]}` and renders stage sections — used by Task 7 (cache) and Task 8 (stats/filter).

- [ ] **Step 1: Add the depth prompt builder, work-row renderer, and pass-2 runner**

```html
<script>
// ── Pass 2: depth ────────────────────────────────────────
function buildDepthPrompt(topic, subtopics) {
  const subtopicList = subtopics.map(s => '- ' + s.name + ': ' + s.description).join('\n');
  return `You are an expert academic librarian building a complete staged reading map for "${topic}".

The reading map must cover EVERY one of these subtopics somewhere in its sequence:
${subtopicList}

Follow natural pedagogical progression — from accessible entry points through foundational texts to cutting-edge frontiers. Each stage builds on prior stages; works within a stage can be read in parallel.

Stage vocabulary (adapt per topic, not all required): "Orientation & Landscape", "Core Foundations", "Seminal Works", "Breakthroughs & Advances", "Modern Synthesis", "Contemporary Frontiers". Optional: "Methodological Foundations", "Historical & Philosophical Context", "Interdisciplinary Bridges", "Open Problems & Future Directions", "Application Domains".

For each work include exactly:
  - "title" (string)
  - "author" (string)
  - "year" (string or number)
  - "type" (exactly "book" or "paper" — no other value)
  - "description" (1-2 sentences: what it is and why it matters at this stage)
  - "role" (short functional label, e.g. "seminal paper", "standard textbook", "key breakthrough", "definitive survey")

Each stage object has "label" (2-6 words), "summary" (1 sentence), "works" (array).

Aim for genuine completeness — when in doubt, include. Include both books AND papers throughout; do not favor one type. No artificial caps.

Return ONLY a JSON object with exactly one key "stages" (array). No markdown fences, no commentary.`;
}

function workRowHtml(w) {
  const link = w.type === 'paper' ? scholarLink(w.title, w.author) : booksLink(w.title, w.author);
  const safeType = escapeHtml(w.type);
  return '<div class="work" data-type="' + safeType + '">' +
    '<span class="badge ' + safeType + '">' + safeType + '</span>' +
    '<span class="badge role">' + escapeHtml(w.role) + '</span>' +
    '<div class="title">' + escapeHtml(w.title) + ' <span class="author">— ' + escapeHtml(w.author) + ', ' + escapeHtml(String(w.year)) + '</span></div>' +
    '<div class="desc">' + escapeHtml(w.description) + '</div>' +
    '<a class="link" href="' + link + '" target="_blank" rel="noopener">View →</a>' +
    '</div>';
}

function renderStages(stages) {
  const el = document.getElementById('results');
  el.innerHTML = stages.map((s, i) => {
    const num = String(i + 1).padStart(2, '0');
    return '<div class="stage">' +
      '<div class="stage-header"><span class="stage-num">' + num + '</span>' + escapeHtml(s.label) + '</div>' +
      (s.summary ? '<div class="stage-summary">' + escapeHtml(s.summary) + '</div>' : '') +
      '<div class="stage-body">' + s.works.map(workRowHtml).join('') + '</div>' +
      '</div>';
  }).join('');
}

async function runPass2(topic, subtopics, apiKey) {
  const raw = await streamChatCompletion(
    apiKey,
    [{ role: 'user', content: buildDepthPrompt(topic, subtopics) }],
    () => {}
  );
  const parsed = JSON.parse(raw);
  renderStages(parsed.stages);
  return parsed.stages;
}
</script>
```

- [ ] **Step 2: Manual verification**

In the browser console, after running pass 1 for a topic (Task 5's verification), run:

```javascript
const subtopics = await runPass1('persuasion', 'sk-or-...');
await runPass2('persuasion', subtopics, 'sk-or-...');
```

Expected: `#results` fills with numbered stage sections, each work row shows a BOOK or PAPER badge, a role badge, title/author/year, description, and a working "View →" link that opens a Google Scholar or Google Books search in a new tab.

- [ ] **Step 3: Commit**

```bash
git add reading-map.html
git commit -m "Add pass 2 staged depth generation and stage/work rendering"
```

---

### Task 7: Main generate flow with cache integration and API key persistence

**Files:**
- Modify: `C:\Users\prave\reading-map.html`

**Interfaces:**
- Consumes: `getCached`/`putCached` (Task 3), `runPass1`/`runPass2` (Tasks 5-6), `normalizeTopicKey` (Task 2), `renderSubtopics`/`renderStages` (Tasks 5-6), `#topicInput`/`#apiKey`/`#genBtn`/`#status` (Task 1).
- Produces: wired `genBtn.onclick` handler; `localStorage` persistence for the API key — used by Task 9 (error handling wraps this same handler).

- [ ] **Step 1: Wire up input enabling, key persistence, and the main generate handler**

```html
<script>
// ── Main flow ────────────────────────────────────────────
const topicInput = document.getElementById('topicInput');
const apiKeyInput = document.getElementById('apiKey');
const genBtn = document.getElementById('genBtn');
const statusEl = document.getElementById('status');

apiKeyInput.value = localStorage.getItem('reading-map-api-key') || '';

function setStatus(msg, cls) {
  statusEl.textContent = msg;
  statusEl.className = cls || '';
}

function updateGenBtn() {
  genBtn.disabled = !(topicInput.value.trim() && apiKeyInput.value.trim());
}
topicInput.oninput = updateGenBtn;
apiKeyInput.oninput = updateGenBtn;
updateGenBtn();

genBtn.onclick = async function () {
  const topic = topicInput.value.trim();
  const apiKey = apiKeyInput.value.trim();
  if (!topic || !apiKey) return;
  localStorage.setItem('reading-map-api-key', apiKey);

  const topicKey = normalizeTopicKey(topic);
  genBtn.disabled = true;
  document.getElementById('subtopics').innerHTML = '';
  document.getElementById('results').innerHTML = '<div class="loading">Checking cache...</div>';

  try {
    const cached = await getCached(topicKey);

    let subtopics = cached?.subtopics;
    if (subtopics) {
      renderSubtopics(subtopics);
    } else {
      setStatus('Generating subtopic map (pass 1/2)...', 'info');
      subtopics = await runPass1(topic, apiKey);
      await putCached(topicKey, { subtopics });
    }

    let stages = cached?.stages;
    if (stages) {
      renderStages(stages);
    } else {
      setStatus('Generating staged reading map (pass 2/2)...', 'info');
      stages = await runPass2(topic, subtopics, apiKey);
      await putCached(topicKey, { subtopics, stages });
    }

    setStatus('Done.', '');
  } catch (err) {
    setStatus('Error: ' + err.message, 'error');
    document.getElementById('results').innerHTML = '';
  } finally {
    genBtn.disabled = false;
  }
};
</script>
```

- [ ] **Step 2: Manual verification — full generate flow**

Open `reading-map.html` fresh in a browser, enter a real API key, type "ethics" in the topic field, click Generate.

Expected: status shows "Generating subtopic map...", chips appear, status updates to "Generating staged reading map...", stage sections appear with work rows, status shows "Done.".

- [ ] **Step 3: Manual verification — cache resumption**

Reload the page, re-enter the same API key (or confirm it persisted), type "ethics" again, click Generate.

Expected: no network requests fire (check browser devtools Network tab — no `openrouter.ai` requests), chips and stages render instantly from cache.

- [ ] **Step 4: Commit**

```bash
git add reading-map.html
git commit -m "Wire main generate flow with IndexedDB cache resumption"
```

---

### Task 8: Stats bar and book/paper filter toggle

**Files:**
- Modify: `C:\Users\prave\reading-map.html`
- Test (scratch): `C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\4e81d10c-2b14-4b96-ba05-4bfaaf9ae5c3\scratchpad\test-stats.mjs`

**Interfaces:**
- Consumes: `stages` array (produced by Task 7's flow), `#statsBar`/`#filterBar`/`#results` (Task 1).
- Produces: `computeStats(stages)` returns `{stageCount, workCount, bookCount, paperCount}`; filter button wiring.

- [ ] **Step 1: Add the pure stats function**

```html
<script>
// ── Stats ────────────────────────────────────────────────
function computeStats(stages) {
  let workCount = 0, bookCount = 0, paperCount = 0;
  for (const s of stages) {
    for (const w of s.works) {
      workCount++;
      if (w.type === 'book') bookCount++;
      else if (w.type === 'paper') paperCount++;
    }
  }
  return { stageCount: stages.length, workCount, bookCount, paperCount };
}
</script>
```

- [ ] **Step 2: Test it standalone**

Create `test-stats.mjs` in the scratchpad directory:

```javascript
function computeStats(stages) {
  let workCount = 0, bookCount = 0, paperCount = 0;
  for (const s of stages) {
    for (const w of s.works) {
      workCount++;
      if (w.type === 'book') bookCount++;
      else if (w.type === 'paper') paperCount++;
    }
  }
  return { stageCount: stages.length, workCount, bookCount, paperCount };
}

function assertDeepEqual(actual, expected, label) {
  const a = JSON.stringify(actual), e = JSON.stringify(expected);
  if (a !== e) {
    console.error('FAIL:', label, '\n  got:', a, '\n  want:', e);
    process.exitCode = 1;
  } else {
    console.log('PASS:', label);
  }
}

const sample = [
  { works: [{ type: 'book' }, { type: 'paper' }] },
  { works: [{ type: 'paper' }] }
];
assertDeepEqual(computeStats(sample), { stageCount: 2, workCount: 3, bookCount: 1, paperCount: 2 }, 'computeStats counts correctly');
assertDeepEqual(computeStats([]), { stageCount: 0, workCount: 0, bookCount: 0, paperCount: 0 }, 'computeStats handles empty stages');
```

- [ ] **Step 3: Run the test**

Run: `node "C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\4e81d10c-2b14-4b96-ba05-4bfaaf9ae5c3\scratchpad\test-stats.mjs"`

Expected: two `PASS:` lines, exit code 0.

- [ ] **Step 4: Add stats rendering and filter wiring, call from the main flow**

```html
<script>
// ── Stats/filter rendering ───────────────────────────────
function renderStatsBar(stats) {
  const el = document.getElementById('statsBar');
  el.textContent = stats.stageCount + ' stages · ' + stats.workCount + ' works (' +
    stats.bookCount + ' books, ' + stats.paperCount + ' papers)';
  el.classList.add('show');
}

function applyFilter(type) {
  document.querySelectorAll('.work').forEach(w => {
    w.style.display = (type === 'all' || w.dataset.type === type) ? '' : 'none';
  });
}

document.getElementById('filterBar').addEventListener('click', (e) => {
  const btn = e.target.closest('button[data-filter]');
  if (!btn) return;
  document.querySelectorAll('#filterBar button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  applyFilter(btn.dataset.filter);
});
</script>
```

- [ ] **Step 5: Call `renderStatsBar` and show the filter bar from the main flow**

Modify the `genBtn.onclick` handler from Task 7 — after the `stages` block resolves (both the cached branch and the freshly-generated branch), add:

```javascript
    const stats = computeStats(stages);
    renderStatsBar(stats);
    document.getElementById('filterBar').classList.add('show');
    applyFilter('all');
```

placed immediately before `setStatus('Done.', '');` inside the `try` block.

- [ ] **Step 6: Manual verification**

Generate a reading map for any topic. Expected: a stats line appears above the results (e.g. "6 stages · 42 works (18 books, 24 papers)"), and the All/Books only/Papers only buttons are visible. Click "Books only" — expected: only rows with the BOOK badge remain visible, others are hidden. Click "All" — expected: all rows reappear.

- [ ] **Step 7: Commit**

```bash
git add reading-map.html
git commit -m "Add stats bar and book/paper filter toggle"
```

---

### Task 9: Error handling — invalid key, per-pass retry, malformed JSON

**Files:**
- Modify: `C:\Users\prave\reading-map.html`

**Interfaces:**
- Consumes: `runPass1`/`runPass2` (Tasks 5-6), the `genBtn.onclick` handler (Task 7).
- Produces: retry buttons that re-invoke only the failed pass without repeating a succeeded one.

- [ ] **Step 1: Refactor the generate handler to isolate each pass with its own retry**

Replace the `genBtn.onclick` body from Task 7 (with the Task 8 Step 5 addition already applied) with this version, which adds a `renderRetry` helper and per-pass catch blocks:

```html
<script>
function renderRetry(label, onRetry) {
  const el = document.getElementById('results');
  const div = document.createElement('div');
  div.className = 'loading';
  div.innerHTML = label + '<br><button class="retry-btn">Retry</button>';
  div.querySelector('button').onclick = onRetry;
  el.appendChild(div);
}

genBtn.onclick = async function () {
  const topic = topicInput.value.trim();
  const apiKey = apiKeyInput.value.trim();
  if (!topic || !apiKey) {
    setStatus('Enter a topic and your OpenRouter API key.', 'error');
    return;
  }
  localStorage.setItem('reading-map-api-key', apiKey);

  const topicKey = normalizeTopicKey(topic);
  genBtn.disabled = true;
  document.getElementById('subtopics').innerHTML = '';
  document.getElementById('statsBar').classList.remove('show');
  document.getElementById('filterBar').classList.remove('show');
  document.getElementById('results').innerHTML = '<div class="loading">Checking cache...</div>';

  const cached = await getCached(topicKey).catch(() => undefined);

  let subtopics = cached?.subtopics;
  if (!subtopics) {
    setStatus('Generating subtopic map (pass 1/2)...', 'info');
    try {
      subtopics = await runPass1(topic, apiKey);
      await putCached(topicKey, { subtopics });
    } catch (err) {
      setStatus('Pass 1 failed: ' + err.message, 'error');
      renderRetry('Subtopic generation failed.', () => genBtn.onclick());
      genBtn.disabled = false;
      return;
    }
  } else {
    renderSubtopics(subtopics);
  }

  let stages = cached?.stages;
  if (!stages) {
    setStatus('Generating staged reading map (pass 2/2)...', 'info');
    document.getElementById('results').innerHTML = '<div class="loading">Generating staged reading map...</div>';
    try {
      stages = await runPass2(topic, subtopics, apiKey);
      await putCached(topicKey, { subtopics, stages });
    } catch (err) {
      setStatus('Pass 2 failed: ' + err.message, 'error');
      document.getElementById('results').innerHTML = '';
      renderRetry('Staged reading map generation failed.', async () => {
        genBtn.disabled = true;
        setStatus('Retrying pass 2/2...', 'info');
        try {
          stages = await runPass2(topic, subtopics, apiKey);
          await putCached(topicKey, { subtopics, stages });
          const stats = computeStats(stages);
          renderStatsBar(stats);
          document.getElementById('filterBar').classList.add('show');
          applyFilter('all');
          setStatus('Done.', '');
        } catch (err2) {
          setStatus('Pass 2 failed again: ' + err2.message, 'error');
          renderRetry('Staged reading map generation failed.', () => genBtn.onclick());
        }
        genBtn.disabled = false;
      });
      genBtn.disabled = false;
      return;
    }
  } else {
    renderStages(stages);
  }

  const stats = computeStats(stages);
  renderStatsBar(stats);
  document.getElementById('filterBar').classList.add('show');
  applyFilter('all');
  setStatus('Done.', '');
  genBtn.disabled = false;
};
</script>
```

Remove the earlier `genBtn.onclick` block written in Task 7 / Task 8 Step 5 — this replaces it entirely (same handler, now with error isolation).

- [ ] **Step 2: Manual verification — invalid key**

Enter an obviously invalid API key (e.g. `sk-or-invalid`) and a topic, click Generate.

Expected: status shows "Pass 1 failed: OpenRouter error 401: ..." (or similar), a "Retry" button appears under the loading area.

- [ ] **Step 3: Manual verification — malformed JSON resilience**

In the browser console, temporarily test the catch path directly:

```javascript
try { JSON.parse('not json'); } catch (e) { console.log('caught as expected:', e.message); }
```

Expected: confirms `JSON.parse` throws are catchable (this is what `runPass1`/`runPass2` rely on — a malformed model response surfaces as a caught error rather than an uncaught exception, per the try/catch structure added in Step 1).

- [ ] **Step 4: Manual verification — pass-2-only retry**

With a valid key, generate a topic successfully once (so it's cached). In devtools, manually delete just the `stages` key from a cached entry to simulate a pass-2 interruption:

```javascript
const db = await openCacheDB();
const tx = db.transaction('topics', 'readwrite');
const rec = await new Promise(r => { const req = tx.objectStore('topics').get('ethics'); req.onsuccess = () => r(req.result); });
delete rec.data.stages;
tx.objectStore('topics').put(rec);
```

Reload the page, generate "ethics" again. Expected: subtopic chips render instantly from cache (no pass-1 network call), status shows "Generating staged reading map (pass 2/2)..." and only pass 2 runs.

- [ ] **Step 5: Commit**

```bash
git add reading-map.html
git commit -m "Add per-pass error handling and retry for reading-map.html"
```

---

### Task 10: Final end-to-end verification pass

**Files:**
- None (verification only).

- [ ] **Step 1: Full walkthrough per spec's Testing section**

With `reading-map.html` open in a browser and a real OpenRouter key entered:

1. Generate a map for "game theory" (one of the user's original 7 topics). Confirm both passes stream and render in order (chips first, then stages).
2. Reload the page, generate "game theory" again. Confirm it loads instantly from IndexedDB with no new `openrouter.ai` network requests (check devtools Network tab).
3. Confirm every work row has exactly one BOOK or PAPER badge and a working "View →" link that opens a plausible Google Scholar (papers) or Google Books (books) search.
4. Click "Books only" and "Papers only" in the filter bar; confirm the row set changes correctly each time, and "All" restores everything.
5. Confirm the stats bar numbers match a manual count of rendered work rows for at least one stage.
6. Repeat step 1 for one more of the 7 topics (e.g. "persuasion") to confirm the app isn't hardcoded to a single topic.

- [ ] **Step 2: Fix any issues found during the walkthrough**

If any check in Step 1 fails, fix the relevant code in `reading-map.html` directly and re-run the failed check before proceeding.

- [ ] **Step 3: Final commit**

```bash
git add reading-map.html
git commit -m "Complete reading-map.html end-to-end verification"
```

---

### Task 11: Live raw-text streaming preview

**Why:** Real end-to-end testing (Task 10) showed that for broad topics, a single pass can run for many minutes with the UI stuck on a static "Generating..." spinner and zero feedback. `runPass1`/`runPass2` currently pass `() => {}` as `onDelta` because JSON isn't safely partial-parseable mid-stream — but the user still needs to see *something* moving. This task adds a live raw-text preview box that shows the growing streamed text as it arrives, without attempting to parse it until the stream completes.

**Files:**
- Modify: `C:\Users\prave\reading-map.html`

**Interfaces:**
- Consumes: `runPass1`/`runPass2` (Tasks 5-6, current file has them at lines ~255 and ~317 — read the file first since line numbers may have shifted from prior fixes).
- Produces: `#streamPreview` DOM element; modifies the `onDelta` callback passed to `streamChatCompletion` inside both `runPass1` and `runPass2`.

- [ ] **Step 1: Add the `#streamPreview` element and its CSS**

In the `<style>` block, add (near the existing `.loading{...}` rule):

```css
#streamPreview{display:none;background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:0.6rem 0.8rem;font-family:ui-monospace,Consolas,monospace;font-size:0.72rem;white-space:pre-wrap;word-break:break-word;max-height:220px;overflow-y:auto;color:var(--muted);margin:0.6rem 0;}
#streamPreview.show{display:block;}
```

In the HTML body, add the element immediately after `<div id="status"></div>` and before `<div id="subtopics"></div>`:

```html
<div id="streamPreview"></div>
```

- [ ] **Step 2: Update `runPass1` to stream into the preview**

Read the current file to find the exact current text of `runPass1` (it should closely match this), then replace it with:

```javascript
async function runPass1(topic, apiKey) {
  const previewEl = document.getElementById('streamPreview');
  previewEl.textContent = '';
  previewEl.classList.add('show');
  const raw = await streamChatCompletion(
    apiKey,
    [{ role: 'user', content: buildBreadthPrompt(topic) }],
    (text) => { previewEl.textContent = text; previewEl.scrollTop = previewEl.scrollHeight; }
  );
  previewEl.classList.remove('show');
  const parsed = JSON.parse(raw);
  renderSubtopics(parsed.subtopics);
  return parsed.subtopics;
}
```

- [ ] **Step 3: Update `runPass2` the same way**

```javascript
async function runPass2(topic, subtopics, apiKey) {
  const previewEl = document.getElementById('streamPreview');
  previewEl.textContent = '';
  previewEl.classList.add('show');
  const raw = await streamChatCompletion(
    apiKey,
    [{ role: 'user', content: buildDepthPrompt(topic, subtopics) }],
    (text) => { previewEl.textContent = text; previewEl.scrollTop = previewEl.scrollHeight; }
  );
  previewEl.classList.remove('show');
  const parsed = JSON.parse(raw);
  renderStages(parsed.stages);
  return parsed.stages;
}
```

Note: both functions share one `#streamPreview` element — this is correct since only one pass runs at a time in the normal flow. The retry closures added in Task 9 call `runPass2` directly, so they automatically get the same live-preview behavior with no further changes needed there.

- [ ] **Step 4: Manual verification**

Open `reading-map.html`, enter a real key, generate any topic. Expected: immediately after clicking Generate, a scrollable monospace box appears below the status line showing raw JSON text growing in real time during pass 1; it clears and hides once pass 1 finishes and chips render; the same box reappears and fills during pass 2; it hides once stages render.

- [ ] **Step 5: Commit**

```bash
git add reading-map.html
git commit -m "Add live raw-text streaming preview for both passes"
```

---

### Task 12: Chunked parallel pass 2 for large subtopic counts

**Why:** Real E2E testing showed "game theory" returned 776 subtopics from pass 1, producing a 110KB pass-2 prompt that ran for 10+ minutes without completing. The user chose to keep pass 1 uncapped but wants pass 2 to be faster. This task splits pass 2 into chunks of subtopics, generates each chunk's staged reading map with its own (much smaller, much faster) API call, runs a bounded number of these concurrently, and merges the per-chunk stage results into one final staged reading map, ordered by a canonical stage sequence.

**Files:**
- Modify: `C:\Users\prave\reading-map.html`

**Interfaces:**
- Consumes: `buildDepthPrompt`, `streamChatCompletion`, `renderStages`, `#streamPreview` (Task 11).
- Produces: `chunkArray(arr, size)`, `runWithConcurrencyLimit(items, limit, fn)`, `mergeStageBatches(batches)`, replaces `runPass2` — used by Task 7/9's generate flow (same call signature `runPass2(topic, subtopics, apiKey)` and same return shape `Promise<Array<Stage>>`, so no changes needed to the calling code).

- [ ] **Step 1: Add `chunkArray` and `runWithConcurrencyLimit` (pure/generic helpers)**

```javascript
// ── Chunking + bounded concurrency ───────────────────────
function chunkArray(arr, size) {
  const chunks = [];
  for (let i = 0; i < arr.length; i += size) chunks.push(arr.slice(i, i + size));
  return chunks;
}

async function runWithConcurrencyLimit(items, limit, fn) {
  const results = new Array(items.length);
  let next = 0;
  async function worker() {
    while (next < items.length) {
      const i = next++;
      results[i] = await fn(items[i], i);
    }
  }
  const workers = Array.from({ length: Math.min(limit, items.length) }, worker);
  await Promise.all(workers);
  return results;
}
```

- [ ] **Step 2: Test both standalone with node**

Create a scratch test file `C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\4e81d10c-2b14-4b96-ba05-4bfaaf9ae5c3\scratchpad\test-chunking.mjs`:

```javascript
function chunkArray(arr, size) {
  const chunks = [];
  for (let i = 0; i < arr.length; i += size) chunks.push(arr.slice(i, i + size));
  return chunks;
}

async function runWithConcurrencyLimit(items, limit, fn) {
  const results = new Array(items.length);
  let next = 0;
  async function worker() {
    while (next < items.length) {
      const i = next++;
      results[i] = await fn(items[i], i);
    }
  }
  const workers = Array.from({ length: Math.min(limit, items.length) }, worker);
  await Promise.all(workers);
  return results;
}

function assertDeepEqual(actual, expected, label) {
  const a = JSON.stringify(actual), e = JSON.stringify(expected);
  if (a !== e) { console.error('FAIL:', label, '\n  got:', a, '\n  want:', e); process.exitCode = 1; }
  else console.log('PASS:', label);
}

assertDeepEqual(chunkArray([1,2,3,4,5], 2), [[1,2],[3,4],[5]], 'chunkArray splits into correct groups');
assertDeepEqual(chunkArray([1,2], 5), [[1,2]], 'chunkArray handles array smaller than size');
assertDeepEqual(chunkArray([], 5), [], 'chunkArray handles empty array');

(async () => {
  const active = [];
  let maxConcurrent = 0;
  const items = [1,2,3,4,5,6,7,8];
  const results = await runWithConcurrencyLimit(items, 3, async (n) => {
    active.push(n);
    maxConcurrent = Math.max(maxConcurrent, active.length);
    await new Promise(r => setTimeout(r, 10));
    active.splice(active.indexOf(n), 1);
    return n * 2;
  });
  assertDeepEqual(results, [2,4,6,8,10,12,14,16], 'runWithConcurrencyLimit preserves order and computes correctly');
  if (maxConcurrent > 3) { console.error('FAIL: exceeded concurrency limit, max was', maxConcurrent); process.exitCode = 1; }
  else console.log('PASS: never exceeded concurrency limit of 3 (max observed: ' + maxConcurrent + ')');
})();
```

Run: `node "C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\4e81d10c-2b14-4b96-ba05-4bfaaf9ae5c3\scratchpad\test-chunking.mjs"`

Expected: 5 PASS lines, exit code 0.

- [ ] **Step 3: Add `mergeStageBatches`**

```javascript
const STAGE_ORDER = [
  'Orientation & Landscape',
  'Methodological Foundations',
  'Historical & Philosophical Context',
  'Core Foundations',
  'Seminal Works',
  'Breakthroughs & Advances',
  'Interdisciplinary Bridges',
  'Modern Synthesis',
  'Contemporary Frontiers',
  'Open Problems & Future Directions',
  'Application Domains'
];

function mergeStageBatches(batches) {
  const byLabel = new Map();
  for (const batch of batches) {
    for (const s of batch.stages) {
      const key = s.label.trim().toLowerCase();
      if (!byLabel.has(key)) {
        byLabel.set(key, { label: s.label, summary: s.summary, works: [] });
      }
      byLabel.get(key).works.push(...s.works);
    }
  }
  const merged = Array.from(byLabel.values());
  merged.sort((a, b) => {
    const ia = STAGE_ORDER.findIndex(x => x.toLowerCase() === a.label.trim().toLowerCase());
    const ib = STAGE_ORDER.findIndex(x => x.toLowerCase() === b.label.trim().toLowerCase());
    const oa = ia === -1 ? STAGE_ORDER.length : ia;
    const ob = ib === -1 ? STAGE_ORDER.length : ib;
    return oa - ob;
  });
  return merged;
}
```

- [ ] **Step 4: Test `mergeStageBatches` standalone with node**

Create `C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\4e81d10c-2b14-4b96-ba05-4bfaaf9ae5c3\scratchpad\test-merge.mjs` with the same `STAGE_ORDER`/`mergeStageBatches` code above, plus:

```javascript
function assertDeepEqual(actual, expected, label) {
  const a = JSON.stringify(actual), e = JSON.stringify(expected);
  if (a !== e) { console.error('FAIL:', label, '\n  got:', a, '\n  want:', e); process.exitCode = 1; }
  else console.log('PASS:', label);
}

const batches = [
  { stages: [
    { label: 'Seminal Works', summary: 'S1', works: [{title:'A'}] },
    { label: 'Orientation & Landscape', summary: 'O1', works: [{title:'B'}] }
  ]},
  { stages: [
    { label: 'seminal works', summary: 'S2 (dup label, different case)', works: [{title:'C'}] },
    { label: 'Contemporary Frontiers', summary: 'F1', works: [{title:'D'}] }
  ]}
];
const merged = mergeStageBatches(batches);
assertDeepEqual(merged.map(s => s.label), ['Orientation & Landscape', 'Seminal Works', 'Contemporary Frontiers'], 'merged stages are ordered by STAGE_ORDER regardless of input order');
assertDeepEqual(merged.find(s => s.label === 'Seminal Works').works.map(w => w.title), ['A', 'C'], 'works from same-label chunks (case-insensitive) are combined into one stage, in arrival order');
assertDeepEqual(mergeStageBatches([{stages:[{label:'Some Unknown Stage', summary:'x', works:[]}]}]).map(s=>s.label), ['Some Unknown Stage'], 'a label not in STAGE_ORDER still appears (sorted last)');
```

Run: `node "C:\Users\prave\AppData\Local\Temp\claude\C--Users-prave\4e81d10c-2b14-4b96-ba05-4bfaaf9ae5c3\scratchpad\test-merge.mjs"`

Expected: 3 PASS lines, exit code 0.

- [ ] **Step 5: Replace `runPass2` with the chunked version**

Read the current file first to find `runPass2`'s exact current text (it was last modified in Task 11 to add the streaming preview) and replace the whole function with:

```javascript
const DEPTH_CHUNK_SIZE = 50;
const DEPTH_CONCURRENCY = 5;

async function runPass2(topic, subtopics, apiKey) {
  const previewEl = document.getElementById('streamPreview');
  const chunks = chunkArray(subtopics, DEPTH_CHUNK_SIZE);
  previewEl.textContent = '';
  previewEl.classList.add('show');

  const progress = chunks.map(() => 0);
  function renderProgress() {
    previewEl.textContent = chunks.length === 1
      ? previewEl.textContent
      : progress.map((n, i) => 'Batch ' + (i + 1) + '/' + chunks.length + ': ' + n + ' chars').join('\n');
    previewEl.scrollTop = previewEl.scrollHeight;
  }

  const batches = await runWithConcurrencyLimit(chunks, DEPTH_CONCURRENCY, async (chunk, i) => {
    const raw = await streamChatCompletion(
      apiKey,
      [{ role: 'user', content: buildDepthPrompt(topic, chunk) }],
      (text) => {
        if (chunks.length === 1) { previewEl.textContent = text; previewEl.scrollTop = previewEl.scrollHeight; }
        else { progress[i] = text.length; renderProgress(); }
      }
    );
    return JSON.parse(raw);
  });

  previewEl.classList.remove('show');
  const stages = chunks.length === 1 ? batches[0].stages : mergeStageBatches(batches);
  renderStages(stages);
  return stages;
}
```

Note: for topics with `subtopics.length <= DEPTH_CHUNK_SIZE` (50), this produces exactly one chunk — behavior is functionally identical to before (one call, direct raw-text streaming, no merge needed). Broad topics get split into multiple chunks processed with at most `DEPTH_CONCURRENCY` (5) requests in flight at once, each with a much smaller prompt (at most 50 subtopics' worth of context instead of hundreds), so both per-request latency and total wall-clock time drop substantially versus one giant sequential call.

- [ ] **Step 6: Manual verification**

Open `reading-map.html`, enter a real key, and generate a topic known to produce many subtopics (e.g. "game theory", which returned 776 subtopics in earlier testing). Expected: pass 2's preview box shows multiple "Batch N/M: ... chars" lines updating concurrently (proving parallelism), pass 2 completes in a small fraction of the time observed before this task (minutes, not 10+ minutes), and the final rendered stages still follow the canonical stage order (Orientation & Landscape first, Contemporary Frontiers near the end, etc.) with no duplicate stage sections for the same stage label.

- [ ] **Step 7: Commit**

```bash
git add reading-map.html
git commit -m "Chunk pass 2 into parallel batches for large subtopic counts"
```
