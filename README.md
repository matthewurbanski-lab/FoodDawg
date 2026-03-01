# FoodDawg (beta)

A lightweight, open-source MVP inspired by classic food service management suites: purchasing, inventory control, production outputs, and reporting.

## Current MVP features
- **Inventory ledger** (perpetual): receipts, issues, waste, transfers (as ledger entries)
- **Inventory balances** with computed average cost
- **PO Sync**: pull purchase orders from a *PO system* and post receipts into inventory
  - `csv` source included for beta testing
  - `rest` source skeleton included to map to your real PO API
- **Purchases summary report** (top purchases by cost)

## Quickstart (local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open: http://127.0.0.1:8000/docs

### Sync purchase orders into inventory (CSV demo)
```bash
curl -X POST "http://127.0.0.1:8000/purchasing/sync-pos"
curl "http://127.0.0.1:8000/inventory/balances"
curl "http://127.0.0.1:8000/reports/purchases-summary"
```

## Docker
```bash
docker compose up --build
```

## PO system integration
Set env vars:
- `FOODDAWG_PO_SOURCE=csv` or `rest`
- `FOODDAWG_PO_CSV_PATH=...`
- `FOODDAWG_PO_REST_BASE_URL=...`
- `FOODDAWG_PO_REST_TOKEN=...`

Implement your PO mapping in `app/services/integrations/po_rest.py` to match your PO system’s fields.

## Roadmap (next modules)
- Menu planning + recipe BOM (bill of materials) to drive purchasing/par levels
- Production docs: pick sheets, prep sheets, transfer sheets
- Inventory counts/shrink reporting vs planned use
- Catered event planning and pre-costing
- Forecasting stub → patron history + acceptability → portions

## License
MIT (edit as needed).
