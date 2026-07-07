# Summer 2027 Tech Internships

[![CI](https://github.com/shanp23/aiinternshiptracker/actions/workflows/ci.yml/badge.svg)](https://github.com/shanp23/aiinternshiptracker/actions/workflows/ci.yml) ![Open roles](https://img.shields.io/badge/dynamic/json?label=open%20roles&query=open_total&url=https%3A%2F%2Fshanp23.github.io%2Faiinternshiptracker%2Fapi%2Fstats.json&color=2f81f7) ![Updates](https://img.shields.io/badge/updates-every%202%20hours-3fb950) [![RSS](https://img.shields.io/badge/RSS-subscribe-e67e22)](https://shanp23.github.io/aiinternshiptracker/feed.xml)

A self-updating engine that tracks tech internships so you don't have to. Instead of refreshing a dozen career pages by hand, it reads company hiring feeds directly and keeps one live list, newest roles on top, refreshed automatically throughout the day.

**0 open roles · 0 new this week · 3,606 companies tracked · updated Jul 07, 2026 at 23:09 UTC**

**⭐Star this repo⭐** to save it and get updates when new roles are added.

**Live:** [dashboard](https://shanp23.github.io/aiinternshiptracker/) · [RSS feed](https://shanp23.github.io/aiinternshiptracker/feed.xml) (instant alerts in any RSS app) · [JSON API](https://shanp23.github.io/aiinternshiptracker/api/jobs.json)

**🔔 New roles in your inbox:** [subscribe by email](https://shanp23.github.io/aiinternshiptracker/#subscribe) - one email a day, only when new internships actually appeared, one-click unsubscribe. (Prefer RSS-to-email? [Feedrabbit works too](https://feedrabbit.com/subscriptions/new?url=https%3A%2F%2Fraw.githubusercontent.com%2Fshanp23%2Faiinternshiptracker%2Fmain%2Fdocs%2Ffeed.xml).)

## What this is

This is an engine, not a hand-kept list. It polls company career feeds several times a day, finds the internships, removes duplicates, and rebuilds this page on its own. Every link comes straight from the source, so it's real and current, not a stale list someone forgot to update (speed matters).

## What makes this different

- **📅 [Drop Radar](#drop-radar)** - the only list that shows **what's coming**: each company's expected posting window, projected from last cycle's real first-post dates.
- **No-code intel, computed** - 📚 will-train / 🧪 tools-preferred badges detected automatically from every job description, plus ✓ for employers with a real H-1B track record (official USCIS data). The big lists crowdsource this by hand; here it's code.
- **Real posted dates on every role** - pulled from each job portal itself, so newest-first actually means newest.
- **Alerts your way** - [email digests](https://shanp23.github.io/aiinternshiptracker/#subscribe), [RSS](https://shanp23.github.io/aiinternshiptracker/feed.xml), or Discord - plus a [live dashboard](https://shanp23.github.io/aiinternshiptracker/) with search, filters, and an F-1 friendly toggle.
- **An engine, not a spreadsheet** - 3,606 companies polled every 2 hours across 11 job platforms, ~100 tests, full source in this repo.

## Scope

- **Roles:** Software Engineering, Data Science & Machine Learning (and closely related technical internships)
- **Region:** United States (primary), with a separate International section
- **Cycles:** Summer 2027 and Fall 2026

## About

I'm a US-based international student studying in the United States, so I built this for the search I'm doing myself. It started US-focused and now covers international roles too. Use it to spot roles early and apply before they fill up - being first genuinely helps.

## Where this is going

I'm building this in the open and adding to it as it grows. Recently shipped: **email alerts**, the **Drop Radar**, **auto-detected sponsorship flags**, and the **live dashboard**. Next up: personalized alerts (pick your categories), per-company hiring pages, and a ghost-posting detector. If it helps you, a star means a lot and tells me to keep going.

## How to use

- Roles are grouped by cycle below - **newest posting on top, oldest at the bottom.**
- The **Posted** column is the date the company published the role.
- **Flags:** 🇺🇸 = requires U.S. citizenship or a security clearance · 🛂 = the posting says it won't sponsor a work visa · 🆕 = spotted in the last 48 hours. Sponsorship flags are detected automatically from each job description - treat them as a strong hint and confirm on the posting.
- **✓ after a company name** = a real H-1B track record: USCIS approved 10+ petitions for that employer in FY2022–2023 (matched automatically against the official [H-1B Employer Data Hub](https://www.uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub)). No ✓ doesn't mean they won't sponsor - it means we can't prove they have.
- Track your applications with [`data/internships.csv`](data/internships.csv) (opens in Excel / Google Sheets).
- Missing a company? Adding one takes a single line, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

_No matching roles right now, the list fills as companies post. Star it and check back._

<a id="drop-radar"></a>

## 📅 Drop Radar — when companies usually post for Summer 2027

Stop refreshing career pages. This is each company's **first intern posting last cycle**, projected forward a year — so you know who drops next. ✅ = already live in the list above.

> **Heads up:** companies trend *earlier* every cycle — this year's first ✅s appeared months ahead of their projected dates. Treat "expected" as the **latest** point to start watching, not a promise of the drop day.

| Company | First posted last cycle | Expected this cycle | Status |
|---|---|---|---|
| Rippling | Jun 07 | ~Jun 07 · any day now | ⏳ waiting |
| Tesla | Aug 03 | ~Aug 03 · in ~27d | ⏳ waiting |
| Notion | Aug 08 | ~Aug 08 · in ~32d | ⏳ waiting |
| Atomic Semi | Aug 15 | ~Aug 15 · in ~39d | ⏳ waiting |
| Datadog | Aug 18 | ~Aug 18 · in ~42d | ⏳ waiting |
| Shopify | Aug 19 | ~Aug 19 · in ~43d | ⏳ waiting |
| Capital One | Aug 20 | ~Aug 20 · in ~44d | ⏳ waiting |
| NVIDIA | Aug 24 | ~Aug 24 | ⏳ waiting |
| Pinterest | Sep 24 | ~Sep 24 | ⏳ waiting |
| Amazon | Oct 04 | ~Oct 04 | ⏳ waiting |
| Figure | Oct 22 | ~Oct 22 | ⏳ waiting |
| Rivian and Volkswagen Group Technologies | Oct 30 | ~Oct 30 | ⏳ waiting |
| Leidos | by Nov 05 | ~Nov 05 or earlier | ⏳ waiting |
| Meta | by Nov 05 | ~Nov 05 or earlier | ⏳ waiting |
| T-Mobile | by Nov 05 | ~Nov 05 or earlier | ⏳ waiting |
| Sun Life | by Nov 05 | ~Nov 05 or earlier | ⏳ waiting |
| Copart | by Nov 05 | ~Nov 05 or earlier | ⏳ waiting |
| Samsung Research America | by Nov 05 | ~Nov 05 or earlier | ⏳ waiting |
| Electronic Arts | by Nov 05 | ~Nov 05 or earlier | ⏳ waiting |
| State Street | by Nov 05 | ~Nov 05 or earlier | ⏳ waiting |

_867 companies on the [full radar](https://shanp23.github.io/aiinternshiptracker/#radar). "by Nov 05" = the role was already up when last cycle's reference window opened - treat it as a latest bound. "waiting" means not seen in our tracked feeds yet, not a guarantee it isn't out somewhere else._

---

## Hiring timeline

Internships posted per week, from each role's real published date - redrawn automatically on every run. When this line takes off, recruiting season is open:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/trends-dark.svg">
  <img alt="Internships posted per week, drawn from real published dates" src="docs/trends-light.svg">
</picture>

## How it stays current

A small Python engine reads public company hiring feeds directly, keeps the roles that match the scope above, de-duplicates across sources, records each role's published date once (so it never shifts), and regenerates this page through GitHub Actions. It polls every company concurrently (async) with retry/backoff and per-host rate limits. The full source is in this repo.

_Engine (last run): 3,606 companies across 11 ATS platforms · 98% fetch success · completed in 251.9s._

## Contributing

Adding a company takes one line, see [CONTRIBUTING.md](CONTRIBUTING.md). Suggestions and pull requests are welcome.

## Note on dates

The **Posted** column shows when a role was published, with the newest at the top. I pull the posting date straight from each job portal, but a lot of them don't expose one publicly, so those rows show a dash (—) for now instead of a guessed date. The ones that do publish a date are dated. Know the real date for a dashed role? Open a PR and I'll merge it.

Roles can close at any time, so always confirm on the company's own site before applying.
