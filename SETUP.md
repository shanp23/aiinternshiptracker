# Your AI Business Internship Engine — Setup (no coding needed)

This repo finds **non-technical AI internships** (product, analyst, strategy,
marketing, prompt/content, policy, trust & safety, sales) for **Fall 2026 and
Summer 2027**, keeps only **Raleigh–Durham–Chapel Hill (🏠) or US-remote** roles,
and **drops any posting that requires prior coding**. It refreshes itself
**every hour** using GitHub's free automation. No AI/LLM API. $0 to run.

## One-time setup (about 10 minutes)

1. Create a free account at github.com (if you don't have one).
2. Click "+" (top right) → **New repository** → name it anything →
   set it to **Public** (public = free automation minutes) → Create.
3. Easiest upload: install **GitHub Desktop** (desktop.github.com), sign in,
   File → Clone your new empty repo, drag ALL files from this folder into it
   (including the hidden `.github` folder), then Commit + Push.
   (Web-only fallback: on the repo page use "uploading an existing file" and
   drag the folder in — if the `.github` folder doesn't upload, create the two
   workflow files by hand via Add file → Create new file, pasting their contents.)
4. On your repo page: **Actions** tab → click "I understand… enable workflows".
5. Actions → **Update internships** → **Run workflow** to do the first run now.
   After it finishes (a few minutes), your README becomes the live list.

## Reading the list

- 🏠 = Triangle-area role (always sorted to the top)
- 📚 = employer says they'll train you / no experience needed
- 🧪 = a data tool (SQL/Tableau/etc.) is a *plus*, never required
- 🆕 = appeared in the last 48 hours
- Anything that *requires* coding never appears at all.

## Tuning later (all plain-text edits, no code)

- `data/config.json` — cycles, list caps, age limit.
- `src/intern_engine/filters.py` — bottom section holds all role/location
  patterns (clearly labeled "FORK ADDITIONS").
- `src/intern_engine/coding.py` — the strict no-coding rules.
- `.github/workflows/update.yml` — the hourly schedule.

## Honest expectations

Non-technical AI internships are a thin, real market. Early runs may surface
only a handful of roles; the list grows as companies post through fall 2026.
The weekly "discover" job keeps adding companies automatically.
