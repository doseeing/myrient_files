"""
Spider to fetch https://myrient.erista.me/files/ recursively and store file
system info into the directory/ folder, mirroring the remote structure.
"""

import json
import time
from pathlib import Path
from urllib.parse import urljoin, unquote

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://myrient.erista.me/files/"
OUTPUT_DIR = Path(__file__).resolve().parent / "directory"
DELAY_SECONDS = 0.5  # between requests to avoid hammering the server


def fetch_page(url: str) -> str:
    """Fetch page content."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_directory_listing(html: str, base_url: str) -> list[dict]:
    """Parse Apache-style directory listing table into list of entries."""
    soup = BeautifulSoup(html, "html.parser")
    entries = []

    # Find the table (index listing)
    table = soup.find("table")
    if not table:
        return entries

    rows = table.find_all("tr")
    # Skip header row
    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        # First cell: link + name
        link_el = cells[0].find("a")
        if not link_el:
            continue

        href = link_el.get("href") or ""
        name = (link_el.get_text() or "").strip()
        if not name or name in ("./", "../", "Parent directory/"):
            continue

        # Normalize name (remove trailing slash for display, keep for is_dir)
        is_dir = href.endswith("/") or name.endswith("/")
        if name.endswith("/"):
            name = name.rstrip("/")
        if href.startswith("./"):
            href = href[2:]
        if href.startswith("../"):
            continue
        name = unquote(name)

        size_cell = (cells[1].get_text() or "").strip()
        date_cell = (cells[2].get_text() or "").strip()

        full_url = urljoin(base_url, href) if href else base_url

        entries.append({
            "name": name,
            "href": href,
            "url": full_url,
            "is_dir": is_dir,
            "size": size_cell if size_cell != "-" else None,
            "date": date_cell if date_cell != "-" else None,
        })

    return entries


def save_listing(entries: list[dict], path: Path) -> None:
    """Write listing to directory as JSON and a readable index."""
    path.mkdir(parents=True, exist_ok=True)

    (path / "listing.json").write_text(
        json.dumps(entries, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = ["name\tis_dir\tsize\tdate\n"]
    for e in entries:
        lines.append(
            f"{e['name']}\t{e['is_dir']}\t{e['size'] or '-'}\t{e['date'] or '-'}\n"
        )
    (path / "index.txt").write_text("".join(lines), encoding="utf-8")


def safe_path_component(name: str) -> str:
    """Sanitize a directory name for use as a filesystem path component."""
    return name.replace("/", "_").replace("\\", "_").strip() or "unnamed"


def crawl_recursive(url: str, local_path: Path, visited: set[str]) -> None:
    """Fetch a directory listing, save it, and recurse into subdirectories."""
    url_normalized = url.rstrip("/") + "/"
    if url_normalized in visited:
        return
    visited.add(url_normalized)

    print(f"Fetching {url_normalized} ...")
    try:
        html = fetch_page(url_normalized)
    except requests.RequestException as e:
        print(f"  Error: {e}")
        return

    time.sleep(DELAY_SECONDS)

    entries = parse_directory_listing(html, url_normalized)
    print(f"  Parsed {len(entries)} entries -> {local_path}")
    save_listing(entries, local_path)

    for e in entries:
        if e["is_dir"] and e.get("url"):
            sub_path = local_path / safe_path_component(e["name"])
            crawl_recursive(e["url"], sub_path, visited)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    visited: set[str] = set()
    crawl_recursive(BASE_URL, OUTPUT_DIR, visited)
    print(f"Done. Saved under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
