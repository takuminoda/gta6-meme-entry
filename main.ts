// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The judged artifact is the X post itself: its first picture (meme.png, drawn by
// make_meme.py from assets/mark-1024.png) and its text. This program is only the
// plumbing the gate needs -- it copies POST.json (the post's address, filled in by
// the operator after posting) from the repository root to /output/POST.json, where
// the house reads it before it builds the judge's dossier.
//
// Locally MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Deliberately dependency-free and deterministic: no network, no wall clock, no
// files outside the repository, so two runs write the same bytes.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });

try {
  copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
