# EvoMap GEP Platform

AI Self-Evolution Infrastructure based on GEP (Genome Evolution Protocol).

## Quick Start

```bash
# Clone the repository
git clone https://github.com/jyf2100/evomap.git
cd evomap

# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | React Web UI |
| Backend | 8000 | FastAPI REST API |
| PostgreSQL | 5432 | Database |

## API Endpoints

- `GET /health` - Health check
- `GET /api/v1/genes` - List genes
- `POST /api/v1/genes` - Create gene
- `GET /api/v1/capsules` - List capsules
- `GET /api/v1/events` - List events

## Development

### Backend

```bash
cd backend
uv sync --dev
uv run pytest tests/ -v
uv run uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## GEP Protocol

The platform implements the GEP (Genome Evolution Protocol) loop:

1. **Scan** - Monitor logs for errors and patterns
2. **Signal** - Generate evolution signals
3. **Intent** - Classify evolution intent
4. **Mutate** - Generate code/prompt mutations
5. **Validate** - Sandbox validation
6. **Solidify** - Create validated genes

## License

MIT
