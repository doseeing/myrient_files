# myrient_files

Spider that fetches the [Myrient](https://myrient.erista.me/files/) file index and saves the directory listing locally.

> **Note:** Myrient is shutting down on 31 March 2026. Use this to capture the top-level index; extend the script if you need to archive deeper listings.

See [dev_note.md](dev_note.md) for notes on building a mirror site of Myrient.

## Requirements

- Python 3.10+
- See [requirements.txt](requirements.txt)

## Setup

```bash
pip install -r requirements.txt
# or
python3 -m pip install -r requirements.txt
```

Optional: use a virtual environment:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Usage

```bash
python spider.py
```

Or with the venv or if `python` doesn't have the deps:

```bash
python3 spider.py
# or
.venv/bin/python spider.py
```

## Output

The script writes to the **`directory/`** folder:

| File | Description |
|------|-------------|
| `listing.json` | Full listing as JSON: `name`, `href`, `url`, `is_dir`, `size`, `date` |
| `index.txt` | Same data as tab-separated text |

`directory/` is in [.gitignore](.gitignore). Remove that line if you want to commit the scraped listing.

## License

Unlicense or similar; use as you like.
