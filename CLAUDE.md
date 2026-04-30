# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A single-file Streamlit dashboard (`app.py`) that pulls daily quotes for three Brazilian stocks — Petrobras (`PETR4.SA`), Itaú (`ITUB4.SA`) and Vale (`VALE3.SA`) — from Yahoo Finance via `yfinance` and renders price metrics, per-stock line charts, and a base-100 comparative chart. The user-facing language is Portuguese (pt-BR).

## Running the app

A virtualenv lives at `.venv/` (Windows layout: `.venv/Scripts/...`). On Git Bash use forward slashes:

```bash
.venv/Scripts/python.exe -m streamlit run app.py
```

Or activate first: `source .venv/Scripts/activate` then `streamlit run app.py`. Default URL is `http://localhost:8501`.

To rebuild the venv from scratch:

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

There is no test suite, linter config, or build step. "Verifying" a change means running the app and clicking through the period selector in the sidebar.

## Architecture notes

- **Single module.** All UI, data fetching, and computation lives in `app.py`. Don't split into packages unless the file genuinely outgrows one screen of logic — Streamlit apps idiomatically run top-to-bottom on every interaction.
- **Tickers and periods are dicts at module top.** `TICKERS` maps a display name to the Yahoo Finance symbol (the `.SA` suffix is what routes to B3 — dropping it returns NYSE ADRs, which are different securities). `PERIODS` maps Portuguese labels to the strings `yfinance` accepts (`1mo`, `6mo`, `1y`, `5y`).
- **Caching is load-bearing.** `fetch_history` is wrapped in `@st.cache_data(ttl=3600)`. Streamlit re-executes the whole script on every widget change, so without the cache each interaction would re-hit Yahoo Finance three times. Preserve this when refactoring.
- **Empty-DataFrame guard.** After each fetch the code checks `df.empty` and calls `st.error` + `st.stop()`. `yfinance` returns an empty frame (not an exception) when a symbol is wrong or the network fails — keep this guard if you change the fetch path.
- **Comparison chart uses base 100.** `df["Close"] / df["Close"].iloc[0] * 100`. This is the only normalization in the app; the per-stock charts show raw BRL prices.

## Conventions

- Keep user-facing strings in Portuguese.
- Don't introduce Plotly/Altair custom charts unless a feature genuinely needs them — `st.line_chart` and `st.metric` are deliberately the whole vocabulary right now.
- The plan that produced this app is at `C:/Users/diego/.claude/plans/criei-um-site-ethereal-puffin.md` and lists what is intentionally out of scope (moving averages, volume, volatility, deploy).

## GitHub auto-sync

The repo is at https://github.com/DiegoLemos93/Vscode-claude (public). Every Claude Code turn automatically commits and pushes any uncommitted changes via a `Stop` hook configured in `.claude/settings.local.json` (gitignored, personal). The hook runs `.claude/auto-sync.sh`, which is a no-op when `git status` is clean and silently swallows push errors so it never blocks a response. The commit message is fixed: `Auto-sync: Claude Code update`.

Don't make manual `git commit` / `git push` calls during a session — the hook handles it. If you need a different commit message for a specific change, edit the file, then `git commit --amend -m "..."` and `git push --force-with-lease` *after* the hook has already pushed.
