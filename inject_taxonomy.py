import re, sys

with open("C:/Users/prave/taxonomy.js", encoding="utf-8") as f:
    taxonomy_js = f.read()

with open("C:/Users/prave/index.html", encoding="utf-8") as f:
    html = f.read()

# ── 1. Replace the old constants + legacy blob ────────────────────────────────
# Replace from SHEET_CSV_URL line through end of _TOPIC_LIB_LEGACY array ("];")
old_block_start = "  const SHEET_CSV_URL ="
old_block_end   = "  ];\n\n  let _sheetDomains = null;"

i_start = html.index(old_block_start)
i_end   = html.index(old_block_end) + len(old_block_end)

indented_taxonomy = "\n".join("  " + line for line in taxonomy_js.splitlines())
new_block = f"{indented_taxonomy}\n\n  let _sheetDomains = null;"

html = html[:i_start] + new_block + html[i_end:]
print(f"Replaced legacy constants block ({i_end - i_start} chars -> {len(new_block)} chars)")

# ── 2. Replace fetchSheetData() ───────────────────────────────────────────────
old_fetch = """  async function fetchSheetData() {
    if (_sheetDomains) return _sheetDomains;
    if (_sheetLoading) return null;
    _sheetLoading = true;
    try {
      const resp = await fetch(SHEET_CSV_URL);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const text = await resp.text();
      const rows = parseCSV(text);
      _sheetDomains = buildSheetData(rows);
      // update the button label with real count
      const topicCount = rows.slice(1).filter(r => r.length > 1 && r[1] && r[1].trim()).length;
      const el = document.getElementById('libTopicCount');
      if(el) el.textContent = `${topicCount.toLocaleString()} curated topics · All academic domains`;
      return _sheetDomains;
    } catch(e) {
      console.error('Sheet fetch failed:', e);
      return null;
    } finally {
      _sheetLoading = false;
    }
  }"""

new_fetch = """  async function fetchSheetData() {
    if (_sheetDomains) return _sheetDomains;
    _sheetDomains = ACADEMIC_TAXONOMY;
    const topicCount = ACADEMIC_TAXONOMY.reduce((s,d) => s + d.fields.reduce((s2,f) => s2 + f.subfields.reduce((s3,sf) => s3 + sf.topics.length, 0), 0), 0);
    const el = document.getElementById('libTopicCount');
    if(el) el.textContent = `${topicCount.toLocaleString()} curated topics · All academic domains`;
    return _sheetDomains;
  }"""

if old_fetch not in html:
    print("ERROR: could not find fetchSheetData to replace. Aborting.", file=sys.stderr)
    sys.exit(1)

html = html.replace(old_fetch, new_fetch, 1)
print("Replaced fetchSheetData()")

# ── 3. Write output ───────────────────────────────────────────────────────────
with open("C:/Users/prave/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Written C:/Users/prave/index.html")
print(f"Final HTML size: {len(html):,} bytes")
