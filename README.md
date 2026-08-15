# BSE Company Update Watcher — per-subcategory ntfy topics

Polls BSE's "Company Update" announcements **once per cycle** and routes each
new announcement to its **own ntfy.sh topic**, based on subcategory
(Award of Order, Credit Rating, Change in Directorate, etc — see
`SUBCATEGORY_TOPICS.md` for the full list of ~47 topics).

One poller, many topics — instead of running a separate always-on GitHub
Actions job per subcategory (which would multiply requests to BSE by ~47x
and likely get rate-limited, and also exceed GitHub's concurrent job limits).

## Setup

1. **Push this repo to GitHub.**

2. **Add two repo secrets** (Settings → Secrets and variables → Actions):
   - `NTFY_TOPIC_PREFIX` — any unique, hard-to-guess string, e.g. `bse7f2x9k`.
     Full topic names become `<prefix>-<subcategory-slug>`.
   - `WORKFLOW_PAT` — a GitHub Personal Access Token (classic or fine-grained)
     with `workflow` scope, so the job can re-trigger itself.

3. **Subscribe to the topics you care about** in the ntfy app or at
   https://ntfy.sh/app — see `SUBCATEGORY_TOPICS.md` for the exact topic
   name per subcategory (substitute your real prefix for `YOUR-PREFIX`).

4. **Start it**: go to Actions → "BSE Announcement Watcher" → Run workflow
   (or just wait for the 6-hourly cron safety net). After that it
   self-chains continuously.

## Files

- `watcher.py` — polling + fan-out logic
- `subcategories.py` — known subcategory → topic-slug map
- `discover_subcategories.py` — re-run periodically to catch new subcategories BSE adds
- `gen_topics_doc.py` — regenerates `SUBCATEGORY_TOPICS.md` from `subcategories.py`
- `.github/workflows/watcher.yml` — self-chaining GitHub Actions workflow
- `state.json` — tracks already-alerted announcement IDs (committed back by the workflow)

## Notes

- Any BSE subcategory **not** in `subcategories.py` still gets alerted — it's
  just routed to a shared `<prefix>-uncategorized` topic instead of its own,
  so nothing is silently dropped. Run `discover_subcategories.py` every so
  often and merge new entries in.
- ntfy topics are public-by-obscurity: anyone who knows a topic name can
  read it. Keep your prefix non-guessable.
