const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 8080;

const ROUTES = {
  '/': 'research-explorer.html',
  '/research-explorer': 'research-explorer.html',
  '/research-explorer.html': 'research-explorer.html',
  '/concept-atlas': 'concept-atlas.html',
  '/concept-atlas.html': 'concept-atlas.html',
  '/reading-list': 'reading-list-generator.html',
  '/reading-list-generator': 'reading-list-generator.html',
  '/knowledge-app': 'knowledge-app.html',
  '/knowledge-app.html': 'knowledge-app.html',
  '/taxonomy-agent': 'taxonomy-agent.html',
  '/taxonomy-agent.html': 'taxonomy-agent.html',
  '/exhaustive-reading-list': 'exhaustive-reading-list.html',
  '/exhaustive-reading-list.html': 'exhaustive-reading-list.html',
  '/fermi-app-concepts': 'fermi-app-concepts.html',
  '/fermi-app-concepts.html': 'fermi-app-concepts.html',
  '/fermi-concepts-data.js': 'fermi-concepts-data.js',
};

const server = http.createServer((req, res) => {
  const file = ROUTES[req.url.split('?')[0]];
  if (file) {
    fs.readFile(path.join(__dirname, file), (err, data) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Error loading ' + file);
        return;
      }
      res.writeHead(200, { 'Content-Type': file.endsWith('.js') ? 'text/javascript; charset=utf-8' : 'text/html; charset=utf-8' });
      res.end(data);
    });
  } else {
    res.writeHead(302, { 'Location': '/' });
    res.end();
  }
});

server.listen(PORT, () => {
  console.log(`Academic Research Tools running on port ${PORT}`);
  console.log(`  /                → research-explorer.html`);
  console.log(`  /concept-atlas   → concept-atlas.html`);
});
