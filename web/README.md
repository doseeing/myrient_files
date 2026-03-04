# Myrient clone (Astro)

Frontend clone of [Myrient](https://myrient.erista.me/) using the [Astro](https://astro.build) framework. Directory listings are read from the `directory/` folder at the repo root (populated by the spider).

## Setup

From the repo root:

```bash
cd web
npm install
```

## Develop

```bash
npm run dev
```

Open http://localhost:4321 — Home and **Files** (from `../directory/`) will be available.

## Build

```bash
npm run build
```

Builds a static site into `web/dist/`. All paths under `directory/` that have a `listing.json` are pre-rendered.

## Preview production build

```bash
npm run preview
```

## Data source

- **Home** – Static copy of the Myrient landing content.
- **Files** – Reads `directory/**/listing.json` (same structure as the spider output). Each directory’s `listing.json` is used to render that path. Folder names with special characters (e.g. `%`, spaces) are encoded in URLs using base64url so routing stays reliable.

External links (Donate, FAQ, Discord, Telegram, Erista, and file download URLs) still point to the original Myrient domain.
