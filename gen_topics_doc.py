from subcategories import SUBCATEGORY_SLUGS, FALLBACK_SLUG

PREFIX = "YOUR-PREFIX"
lines = [
    "# ntfy.sh Topics Reference",
    "",
    "Set the `NTFY_TOPIC_PREFIX` repo secret to your own unique value. "
    "Topics below assume that secret is `YOUR-PREFIX` — substitute your real prefix.",
    "",
    "Subscribe to any of these in the ntfy app/website to get alerts for just that subcategory.",
    "",
    "| Subcategory | ntfy Topic |",
    "|---|---|",
]
for name, slug in sorted(SUBCATEGORY_SLUGS.items()):
    lines.append(f"| {name} | `{PREFIX}-{slug}` |")
lines.append(f"| *(anything not listed above)* | `{PREFIX}-{FALLBACK_SLUG}` |")

with open("SUBCATEGORY_TOPICS.md", "w") as f:
    f.write("\n".join(lines) + "\n")

print("written, total rows:", len(SUBCATEGORY_SLUGS) + 1)
