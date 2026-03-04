import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';

/** URL-safe base64 encode for path segments (avoids % and other problematic chars) */
export function encodePathSegment(s: string): string {
  return Buffer.from(s, 'utf-8').toString('base64url');
}

export function decodePathSegment(s: string): string {
  return Buffer.from(s, 'base64url').toString('utf-8');
}

/** Path to the directory data (parent of web/). */
export function getDirectoryRoot(): string {
  return resolve(process.cwd(), '..', 'directory');
}

export interface ListingEntry {
  name: string;
  href: string;
  url: string;
  is_dir: boolean;
  size: string | null;
  date: string | null;
}

/**
 * Load listing.json for a given path (array of segment names as on disk).
 * pathSegments are the raw folder names, e.g. ['eXo', 'eXoDOS'].
 */
export function loadListing(pathSegments: string[]): ListingEntry[] | null {
  const root = getDirectoryRoot();
  const dir = pathSegments.length ? join(root, ...pathSegments) : root;
  const file = join(dir, 'listing.json');
  if (!existsSync(file)) return null;
  try {
    const data = JSON.parse(readFileSync(file, 'utf-8'));
    return Array.isArray(data) ? data : null;
  } catch {
    return null;
  }
}

/**
 * Recursively collect all path segments that have a listing.json.
 * Returns array of path arrays, e.g. [[], ['eXo'], ['eXo','eXoDOS']].
 */
export function collectAllPaths(): string[][] {
  const root = getDirectoryRoot();
  const paths: string[][] = [];

  function walk(segments: string[]) {
    const dir = segments.length ? join(root, ...segments) : root;
    const listingPath = join(dir, 'listing.json');
    if (!existsSync(listingPath)) return;
    paths.push(segments);
    if (!existsSync(dir)) return;
    const entries = readdirSync(dir, { withFileTypes: true });
    for (const e of entries) {
      if (e.isDirectory() && e.name !== '.' && e.name !== '..') {
        walk([...segments, e.name]);
      }
    }
  }

  walk([]);
  return paths;
}
