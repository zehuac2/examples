import { createServer, get } from 'http';
import { readFileSync } from 'fs';

const template = readFileSync('index.html').toString();

const server = createServer((request, response) => {
  console.log(`new request: ${request.url}`);

  switch (request.url) {
    case '/':
      response.write(template);
      response.end();
      break;
  }

  if (request.url.startsWith('/static')) {
    get(`http://localhost:3000${request.url}`, (viteResponse) => {
      viteResponse.on('data', (chunk) => {
        response.write(chunk);
        response.end();
      });
    });
  }
});

server.listen(4000, () => {
  console.log('server running on http://localhost:4000');
});
