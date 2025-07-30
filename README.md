# Talka Demo

This project is a small demonstration combining a Vue 3 frontend with a simple Python
backend using WebSockets. It visualises call data in a dashboard and allows
browsing of call history.

## Requirements

- **Node.js** (v14 or later)
- **Python** (3.8 or later)
- Python packages listed in `requirements.txt`

## Installation

Install frontend dependencies:

```bash
npm install
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Development

Start the Python backend first:

```bash
python app.py
```

In another terminal, start the Vue development server:

```bash
npm run serve
```

The frontend will be available at `http://localhost:8080` and connects to the
WebSocket server on port `8765`.

## Production build

Generate optimised static files:

```bash
npm run build
```

## Linting and tests

Run ESLint checks and basic Python syntax checks:

```bash
npm run lint
python -m py_compile app.py
```

## Project structure

- `app.py` – simple WebSocket and HTTP server used during development
- `src/` – Vue 3 application source
- `public/` – static assets served by Vue CLI

