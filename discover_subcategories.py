"""
Re-discovers the live list of "Company Update" subcategories from BSE's API.

Run this occasionally (e.g. every few months) to catch new subcategories
BSE introduces, then merge any new entries into subcategories.py.

Usage:
    pip install bse
    python discover_subcategories.py
"""

import re
from datetime import datetime, timedelta

from bse import BSE
from bse import constants


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def main():
    bse = BSE(download_folder="./")
    subcats = set()
    to_date = datetime.now()

    # Walk backwards in 7-day chunks so we don't hit whatever limit breaks
    # very wide date ranges, and paginate a few pages per chunk.
    for chunk in range(8):  # ~8 weeks lookback
        fd = to_date - timedelta(days=(chunk + 1) * 7)
        td = to_date - timedelta(days=chunk * 7)
        for page in range(1, 6):
            try:
                data = bse.announcements(
                    category=constants.CATEGORY.UPDATE,
                    from_date=fd,
                    to_date=td,
                    page_no=page,
                )
            except Exception as e:
                print(f"[warn] chunk {chunk} page {page} failed: {e}")
                break
            rows = data.get("Table", [])
            if not rows:
                break
            for r in rows:
                sc = r.get("SUBCATNAME")
                if sc:
                    subcats.add(sc.strip())

    bse.exit()

    print(f"\nFound {len(subcats)} unique subcategories:\n")
    print("SUBCATEGORY_SLUGS = {")
    for s in sorted(subcats):
        print(f'    "{s}": "{slugify(s)}",')
    print("}")


if __name__ == "__main__":
    main()
