// gta6-meme-x-01 · entry program · Node 22, standard library only.
//
// What the judge reads is the X post itself, fetched by the house from the
// address in POST.json. This program is the intake plumbing and nothing more:
// it moves that one file out of the repository and into the output directory.
//
// Byte-for-byte reproducible. It touches no network, reads no clock, draws no
// random value and opens nothing outside the two directories it is given, so
// running it twice yields the same output digest.
//
// Local stand-ins for the grader's /bot and /output:
//   MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

function fail(why: string): never {
  console.error(`gta6-meme-x-01: ${why}`);
  process.exit(1);
}

let payload: Buffer;
try {
  payload = readFileSync(resolve(botDir, 'POST.json'));
} catch (err) {
  fail(`POST.json is missing from ${botDir}: ${(err as Error).message}`);
}

try {
  mkdirSync(outDir, { recursive: true });
  writeFileSync(resolve(outDir, 'POST.json'), payload);
} catch (err) {
  fail(`could not write POST.json into ${outDir}: ${(err as Error).message}`);
}

console.log(`POST.json delivered to ${outDir} (${payload.length} bytes)`);
