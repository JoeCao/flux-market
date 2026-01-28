# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Stock market K-line visualization system supporting US and China A-share markets. Frontend-backend separation architecture with Vue 3 + TypeScript frontend and Python FastAPI backend.

## Development Commands

```bash
# One-click start (recommended)
./start.sh

# Or start separately:
# Backend (port 8000)
cd backend && source ../venv/bin/activate && python run.py

# Frontend (port 5173)
cd frontend && npm run dev

# Build frontend for production
cd frontend && npm run build

# Initialize stock database
python backend/init_db.py
```

## Architecture

**Backend** (`backend/`)
- FastAPI app entry: `app/main.py` (includes CORS config)
- API routes: `app/api/stock.py` - 4 endpoints (kline, search, validate, info)
- Business logic: `app/services/stock_service.py` - akshare wrapper with retry logic
- Data models: `app/models/stock.py` - Pydantic schemas
- Stock database: `stocks.db` (SQLite) - code/name lookup

**Frontend** (`frontend/`)
- Entry: `src/main.ts`
- Core components:
  - `src/components/KLineChart.vue` - ECharts candlestick with MA lines and volume
  - `src/components/StockSelector.vue` - Stock search and date/adjust selection
- API layer: `src/api/`
- Types: `src/types/`

## Key Implementation Details

- **Dual market support**: US stocks (e.g., AAPL) and A-shares (e.g., 000001, 600000)
- **Data source**: akshare library with Sina data source for stability
- **Adjust types**: qfq (forward), hfq (backward), or none
- **Technical indicators**: Auto-calculated MA5/MA10/MA20
- **A-share retry**: 3 retries with delay for flaky data fetches

## API Reference

- `GET /api/stock/kline?symbol=AAPL&start_date=&end_date=&adjust=qfq`
- `GET /api/stock/search?keyword=apple`
- `GET /api/stock/validate/{symbol}`
- Swagger docs: http://localhost:8000/docs

## Environment

- Python 3.11+ with venv at project root
- Node.js 16+
- No test framework configured yet
