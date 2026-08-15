"""
BSE Corporate Announcements — Real-time Watcher (GitHub Actions edition)
--------------------------------------------------------------------------
Polls BSE's "Company Update" category ONCE per cycle, then fans each new
announcement out to its OWN ntfy.sh topic based on its subcategory
(e.g. "Award of Order / Receipt of Order" -> bse-<prefix>-award-of-order...).

This deliberately avoids running one workflow per subcategory: BSE would
otherwise get hit by N parallel pollers, and GitHub Actions would hit its
concurrent-job cap. One poller, N topics.

  - Runs for a bounded duration (default 5h50m — just under GitHub's 6-hour
    per-job limit), then exits cleanly so the workflow can re-trigger itself.
  - Persists "already seen" announcement IDs to state.json, committed back
    to the repo, so the next chained run doesn't re-alert on old news.
  - Sends push notifications via ntfy.sh (free, no signup).
  - Any subcategory not in subcategories.py still gets alerted — just routed
    to a shared "uncategorized" topic instead of its own, so nothing is
    ever silently dropped.

Install once (handled by the workflow's pip install step):
    pip install bse requests
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from bse import BSE
from bse import constants
import requests

from subcategories import SUBCATEGORY_SLUGS, FALLBACK_SLUG

# ---------- CONFIG ----------
POLL_INTERVAL_SECONDS = 3
RUN_DURATION_MINUTES = 350          # ~5h50m, safely under GitHub's 6h job cap
STATE_FILE = Path("state.json")

# Only poll this category; subcategories within it are fanned out to
# separate topics below. Set to None to fan out ALL categories instead
# (subcategory names would then need to be unique across categories too).
CATEGORY_FILTER = constants.CATEGORY.UPDATE

# ntfy.sh topic PREFIX — pick your own unique, hard-to-guess prefix.
# Full topic per subcategory = "<prefix>-<subcategory-slug>", e.g.
# "myprefix123-award-of-order-receipt-of-order".
# Anyone who knows a topic name can read that topic's alerts, so don't
# use something guessable.
NTFY_TOPIC_PREFIX = os.environ.get("NTFY_TOPIC_PREFIX", "bse-alerts-CHANGE-ME-12345")
NTFY_BASE_URL = "https://ntfy.sh"
# -----------------------------


def load_state() -> set:
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            return set(data.get("seen_ids", []))
        except Exception:
            return set()
    return set()


def save_state(seen_ids: set):
    # Keep only the most recent N ids so the file doesn't grow forever
    trimmed = list(seen_ids)[-5000:]
    STATE_FILE.write_text(json.dumps({"seen_ids": trimmed}, indent=2))


def pdf_url(item: dict) -> str | None:
    name = item.get("ATTACHMENTNAME")
    return f"https://www.bseindia.com/xml-data/corpfiling/AttachLive/{name}" if name else None


def topic_for(item: dict) -> str:
    subcat = (item.get("SUBCATNAME") or "").strip()
    slug = SUBCATEGORY_SLUGS.get(subcat, FALLBACK_SLUG)
    return f"{NTFY_TOPIC_PREFIX}-{slug}"


def send_alert(item: dict):
    company = item.get("SLONGNAME")
    scrip = item.get("SCRIP_CD")
    headline = item.get("HEADLINE") or item.get("NEWSSUB")
    category = item.get("CATEGORYNAME")
    subcategory = item.get("SUBCATNAME")
    more_text = (item.get("MORE") or "").strip()
    dissem = item.get("DissemDT")
    pdf = pdf_url(item)
    topic = topic_for(item)
    ntfy_url = f"{NTFY_BASE_URL}/{topic}"

    # Console log (visible in the GitHub Actions run log)
    print(f"\n🔔 [{topic}] {company} ({scrip}) — {headline}")
    print(f"   {category} / {subcategory} | Dissem: {dissem}")
    if pdf:
        print(f"   PDF: {pdf}")

    # Push notification via ntfy.sh
    body_lines = [headline]
    if more_text:
        body_lines.append(more_text[:400])
    if pdf:
        body_lines.append(f"PDF: {pdf}")
    body = "\n\n".join(body_lines)

    try:
        requests.post(
            ntfy_url,
            data=body.encode("utf-8"),
            headers={
                "Title": f"{company} ({scrip}) — {subcategory}".encode("utf-8"),
                "Priority": "default",
                "Tags": "bell",
            },
            timeout=10,
        )
    except Exception as e:
        print(f"[warn] ntfy push failed for topic {topic}: {e}")


def run():
    bse = BSE(download_folder="./")
    seen_ids = load_state()
    first_pass = len(seen_ids) == 0  # only true on the very first-ever run

    deadline = datetime.now() + timedelta(minutes=RUN_DURATION_MINUTES)
    print(f"Starting watcher. Will run until {deadline.isoformat(timespec='seconds')}")
    print(f"Loaded {len(seen_ids)} previously-seen announcement IDs.")
    print(f"Fanning out to {len(SUBCATEGORY_SLUGS)} known subcategory topics "
          f"(+ 1 fallback) under prefix '{NTFY_TOPIC_PREFIX}'.")

    save_counter = 0

    try:
        while datetime.now() < deadline:
            try:
                if CATEGORY_FILTER:
                    data = bse.announcements(category=CATEGORY_FILTER)
                else:
                    data = bse.announcements()
                rows = data.get("Table", [])
                rows.sort(key=lambda r: r.get("DissemDT") or "")

                for item in rows:
                    news_id = item.get("NEWSID")
                    if not news_id or news_id in seen_ids:
                        continue
                    seen_ids.add(news_id)
                    if not first_pass:
                        send_alert(item)

                first_pass = False

            except Exception as e:
                print(f"[warn] fetch failed, will retry: {e}")

            # Periodically persist state so a mid-run crash doesn't lose everything
            save_counter += 1
            if save_counter % 20 == 0:  # roughly every ~1 min at 3s interval
                save_state(seen_ids)

            time.sleep(POLL_INTERVAL_SECONDS)

    finally:
        save_state(seen_ids)
        bse.exit()
        print("Run finished, state saved.")


if __name__ == "__main__":
    run()
