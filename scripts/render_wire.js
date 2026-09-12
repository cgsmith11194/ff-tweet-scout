#!/usr/bin/env node
// Renders data/sunday/injury-wire.md (a markdown table) to assets/sunday/injury-wire.png.
// Run by .github/workflows/render-wire.yml on every edit to the .md; also runnable locally:
//   node scripts/render_wire.js [--out assets/sunday/injury-wire.png]
// Browser resolution: uses the `playwright` package if installed (CI), else
// `playwright-core` + CHROMIUM_PATH env (sandbox/local).

const fs = require('fs');
const path = require('path');

const SRC = path.join(__dirname, '..', 'data', 'sunday', 'injury-wire.md');
const outIdx = process.argv.indexOf('--out');
const OUT = outIdx > -1 ? process.argv[outIdx + 1]
  : path.join(__dirname, '..', 'assets', 'sunday', 'injury-wire.png');

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function parseTable(md) {
  const rows = md.split('\n')
    .map(l => l.trim())
    .filter(l => l.startsWith('|'))
    .map(l => l.replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim()));
  if (rows.length < 3) throw new Error('No table rows found in ' + SRC);
  const header = rows[0];
  if (header.length !== 5) throw new Error('Expected 5 columns, got ' + header.length);
  return rows.slice(2).filter(r => r.length === 5); // skip header + --- separator
}

function badgeClass(status) {
  const s = status.toUpperCase();
  if (s === 'IN') return 'in';
  if (s === 'OUT') return 'out';
  if (s === 'PENDING') return 'pend';
  if (s === 'EXP IN') return 'expin';   // reported/expected, NOT locked (late windows)
  if (s === 'EXP OUT') return 'expout'; // reported/expected, NOT locked (late windows)
  return 'other';
}

function buildHtml(rows) {
  let sepDone = false;
  const body = rows.map(([player, pos, status, injury, prog]) => {
    const s = status.toUpperCase();
    const notLocked = s === 'PENDING' || s.startsWith('EXP');
    const sep = notLocked && !sepDone ? ' class="sep"' : '';
    if (notLocked) sepDone = true;
    const posHtml = pos ? ` <span class="pos">${esc(pos)}</span>` : '';
    return `<tr${sep}><td class="player">${esc(player)}${posHtml}</td>` +
      `<td><span class="badge ${badgeClass(status)}">${esc(status.toUpperCase())}</span></td>` +
      `<td class="inj">${esc(injury)}</td><td>${esc(prog)}</td></tr>`;
  }).join('\n');

  return `<!doctype html>
<meta charset="utf-8">
<style>
  body { margin: 0; padding: 18px; background: #fff; width: 680px;
         font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; }
  .card { border: 1px solid #e2e2e2; border-radius: 10px; overflow: hidden;
          box-shadow: 0 1px 3px rgba(0,0,0,.06); }
  table { border-collapse: collapse; width: 100%; font-size: 14.5px; color: #1a1a1a; }
  thead th { background: #1f2937; color: #fff; text-align: left; font-size: 12px;
             text-transform: uppercase; letter-spacing: .06em; padding: 9px 12px; }
  td { padding: 8px 12px; border-top: 1px solid #ececec; vertical-align: top; line-height: 1.35; }
  tbody tr:nth-child(even) td { background: #fafafa; }
  .player { font-weight: 600; }
  .pos { color: #6b7280; font-weight: 400; font-size: 13px; white-space: nowrap; }
  .badge { display: inline-block; font-size: 11.5px; font-weight: 700; letter-spacing: .04em;
           padding: 2px 9px; border-radius: 20px; }
  .in    { background: #e7f5ee; color: #0e7a4f; }
  .out   { background: #fbebeb; color: #a02020; }
  .pend  { background: #fdf3e0; color: #8a5a00; }
  .expin  { background: #fff; color: #0e7a4f; box-shadow: inset 0 0 0 1.5px #9fd4bc; }
  .expout { background: #fff; color: #a02020; box-shadow: inset 0 0 0 1.5px #e5b3b3; }
  .other { background: #eeeeee; color: #444444; }
  .sep td { border-top: 2px solid #d8d8d8; }
  .inj { color: #444; }
</style>
<div class="card">
<table>
<thead><tr><th>Player</th><th>Status</th><th>Injury</th><th>Prognosis</th></tr></thead>
<tbody>
${body}
</tbody>
</table>
</div>
`;
}

async function launch() {
  try {
    const { chromium } = require('playwright');
    return chromium.launch({ args: ['--no-sandbox'] });
  } catch (e) {
    const { chromium } = require('playwright-core');
    const exe = process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium';
    return chromium.launch({ executablePath: exe, args: ['--no-sandbox'] });
  }
}

(async () => {
  const rows = parseTable(fs.readFileSync(SRC, 'utf8'));
  const htmlPath = path.join(require('os').tmpdir(), 'injury-wire-render.html');
  fs.writeFileSync(htmlPath, buildHtml(rows));
  const browser = await launch();
  const page = await browser.newPage({ viewport: { width: 716, height: 200 }, deviceScaleFactor: 2 });
  await page.goto('file://' + htmlPath);
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  await page.screenshot({ path: OUT, fullPage: true });
  await browser.close();
  console.log(`rendered ${rows.length} rows -> ${OUT}`);
})().catch(e => { console.error(e.message); process.exit(1); });
