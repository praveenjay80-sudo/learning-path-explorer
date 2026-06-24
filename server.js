const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;

const ROUTES = {
  '/':                           'index.html',
  '/learning-path-explorer':     'index.html',
  '/learning-path-explorer.html':'index.html',
  '/research-explorer':          'research-explorer.html',
  '/research-explorer.html':     'research-explorer.html',
  '/concept-atlas':              'concept-atlas.html',
  '/concept-atlas.html':         'concept-atlas.html',
};

const server = http.createServer((req, res) => {
  const file = ROUTES[req.url.split('?')[0]];
  if (file) {
    fs.readFile(path.join(__dirname, file), (err, data) => {
      if (err) {
        res.writeHead(500, {'Content-Type': 'text/plain'});
        res.end('Error loading ' + file);
        return;
      }
      res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
      res.end(data);
    });
  } else {
    res.writeHead(302, {'Location': '/'});
    res.end();
  }
});

server.listen(PORT, () => {
  console.log(`Learning Path Explorer running on port ${PORT}`);
  console.log(`  /                    → index.html (Learning Path Explorer)`);
  console.log(`  /research-explorer   → research-explorer.html`);
  console.log(`  /concept-atlas       → concept-atlas.html`);
});
