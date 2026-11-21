// Vercel serverless function: proxies Fermi's concept listings (Fermi sends no CORS headers)
// and returns a compact list [fieldKey, branch, topic, title, path] for the page to diff
// against its bundled snapshot.
const FIELDS = ['physics-new','hs-physics-new','ndli-cbse','ndli-icse','mathematics-new','chemistry','biology','cs-ai','frontier'];
module.exports = async (req, res) => {
  try {
    const [lib, hs] = await Promise.all([
      fetch('https://fermi.ai/api/library-topics').then(r => { if (!r.ok) throw new Error('library ' + r.status); return r.json(); }),
      fetch('https://fermi.ai/api/wiki/hs-topics').then(r => { if (!r.ok) throw new Error('hs ' + r.status); return r.json(); }),
    ]);
    const items = [];
    for (const t of lib.topics || []) {
      if (!FIELDS.includes(t.key)) continue;
      for (const l of t.lessons || []) items.push([t.key, l.branch || '', l.topic || '', l.title, '/wiki/' + (l.wiki_slug || l.slug)]);
    }
    for (const t of hs.topics || []) {
      if (t.key === 'hs-physics') continue; // site's "High School Physics" is hs-physics-new
      for (const l of t.lessons || []) items.push([t.key, l.branch || '', l.subarea || '', l.title, l.url]);
    }
    res.setHeader('Cache-Control', 's-maxage=1800, stale-while-revalidate=86400');
    res.status(200).json({ fetchedAt: new Date().toISOString(), items });
  } catch (e) {
    res.status(502).json({ error: String(e.message || e) });
  }
};
