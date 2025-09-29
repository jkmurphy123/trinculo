# trinculo
Autogen driven AI agent to sell your junk

A minimal, pragmatic starter to learn **AutoGen** multi-agent coordination and **MCP**-style tool separation for listing used books on marketplaces.

## What you get
- **FastAPI** backend with a single `/api/submit` endpoint to upload 1–4 photos + target/floor prices.
- **SQLite/SQLModel** schema and helpers.
- **Agent stubs** (Supervisor, Appraiser, Identifier, ConditionGrader, Copywriter, Lister).
- **MCP-style tool servers (stubs)** for OCR/Barcode, Book Metadata, Imaging, DB, and eBay (sandbox placeholder).
- **Tiny frontend** (`frontend/index.html`) to test the flow.
- A **single code path** you can expand phase-by-phase.

> This is intentionally minimal. The MCP servers are Python modules exposing functions; you can later wrap them in real MCP servers.
> The eBay tool is a no-op that writes a local JSON “listing draft”. Replace with real OAuth + Sell APIs when ready.


# 1) Create & activate a venv (example)
cd projects
python3 -m venv llm_env
source llm_env/bin/activate  
cd trinculo

# 2) Install deps
pip install -r requirements.txt

# 3)Run server
uvicorn src.app.main:app --reload
