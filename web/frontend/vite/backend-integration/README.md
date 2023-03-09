# Backend Integrations

- The [client](src/index.js) will attempt to load an image at
  `/static/src/mug.png` by `import mug from "./mug.png";`
- Vite server is hosted at `localhost:3000`, the [backend server](server.js) is
  hosted at `localhost:4000`.
- The backend is configured to redirect `/static` requests to `localhost:3000`
