// Browser check for B63-FX-2: text contrast on actual backgrounds, and anchor/focus targets clear of the sticky header.
// Contrast scan EXCLUDES svg, pre.mermaid and .mmd: Mermaid text is drawn inside SVG with its own theme colours, so computed-background sampling gives false positives. Dark theme shows the diagram on a fixed light panel (#f4f1ea behind #1b2430, about 13:1 by calculation); node colours inside the diagram are not measured.
// Env: CONTRAST_WIDTHS=320,768,1440 (default 1280), CONTRAST_ONLY=1 (skip anchor/focus passes).
// Usage: node tools/ux/check_ux.mjs <docs-dir> [--pages N] [--zoom]   (needs playwright-core and a Chromium; set PW_PATH to its node_modules)
import { createRequire } from "module";
import fs from "fs"; import path from "path";
const require = createRequire((process.env.PW_PATH || "/Users/akumthekar/.devbar/pkgs/npm/24.18.0/node-v24.18.0-darwin-arm64/lib/node_modules/@playwright/mcp/node_modules") + "/");
const { chromium } = require("playwright-core");
const docs = path.resolve(process.argv[2] || "docs");
const pi = process.argv.indexOf("--pages");
const limit = pi > 0 ? Number(process.argv[pi + 1]) : 0;
const widths = [320, 375, 390, 768, 901, 1024, 1280, 1440];
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? (e.name === "assets" ? [] : walk(path.join(d, e.name))) : e.name.endsWith(".html") ? [path.join(d, e.name)] : []);
let pages = walk(docs).sort();
if (process.env.MATCH) pages = pages.filter(f => new RegExp(process.env.MATCH).test(f.replace(docs, "")));
if (limit) { const step = Math.max(1, Math.floor(pages.length / limit)); pages = pages.filter((_, i) => i % step === 0).slice(0, limit); }

const contrastFn = () => {
  const cv = document.createElement("canvas"); cv.width = cv.height = 1; const cx = cv.getContext("2d", { willReadFrequently: true });
  const rgba = c => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = "#000"; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
  const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
  const bgOf = el => {
    const layers = [];
    for (let e = el; e; e = e.parentElement) { const c = rgba(getComputedStyle(e).backgroundColor); if (c[3] > 0) layers.push(c); if (c[3] >= 1) break; }
    let base = [255, 255, 255];
    if (!layers.length || layers[layers.length - 1][3] < 1) base = rgba(getComputedStyle(document.documentElement).backgroundColor).slice(0, 3);
    for (let i = layers.length - 1; i >= 0; i--) { const [r, g, b, a] = layers[i]; base = [r * a + base[0] * (1 - a), g * a + base[1] * (1 - a), b * a + base[2] * (1 - a)]; }
    return base;
  };
  const out = []; const seen = new Set();
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = w.nextNode());) {
    if (!n.textContent.trim()) continue; const el = n.parentElement; if (!el || seen.has(el)) continue; seen.add(el);
    if (el.closest("svg, pre.mermaid, script, style, .mmd, [hidden]")) continue;
    const cs = getComputedStyle(el); if (cs.visibility === "hidden" || cs.display === "none") continue;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const fg = rgba(cs.color), bg = bgOf(el); const fgm = [0, 1, 2].map(i => fg[i] * fg[3] + bg[i] * (1 - fg[3]));
    const a = lum(fgm), b = lum(bg), ratio = (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
    const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700; const large = size >= 24 || (size >= 18.66 && bold);
    if (ratio < (large ? 3 : 4.5)) out.push({ sel: el.tagName.toLowerCase() + (el.className && typeof el.className === "string" ? "." + el.className.trim().split(/\s+/).join(".") : ""), text: n.textContent.trim().slice(0, 40), ratio: +ratio.toFixed(2) });
  }
  return out;
};
const anchorFn = () => {
  const root = document.documentElement; root.style.scrollBehavior = "auto";
  const hdr = document.querySelector(".top"); const out = []; let n = 0;
  const ids = [...document.querySelectorAll('a[href*="#"]')].map(a => { const u = new URL(a.href, location.href); return u.pathname === location.pathname ? decodeURIComponent(u.hash.slice(1)) : ""; }).filter(Boolean);
  ids.push(...[...document.querySelectorAll("main [id]")].map(e => e.id));
  for (const id of new Set(ids)) {
    const el = document.getElementById(id); if (!el || el.closest("svg, defs, [hidden]")) continue; const bb = el.getBoundingClientRect(); if (!bb.width && !bb.height) continue; n++;
    history.replaceState(null, "", "#" + id); el.scrollIntoView();
    const hb = hdr.getBoundingClientRect().bottom, t = el.getBoundingClientRect().top;
    const atEnd = root.scrollHeight - innerHeight - scrollY <= 1;
    if (t < hb - 1 && !atEnd) out.push({ id, top: Math.round(t), headerBottom: Math.round(hb) });
  }
  return { n, out };
};
const focusFn = () => {
  const tall = { n: 0 }; document.documentElement.style.scrollBehavior = "auto";
  const hdr = document.querySelector(".top"); const out = [];
  const els = [...document.querySelectorAll("main a[href], main button, main summary, main input")].filter(e => !e.closest(".top")).slice(0, 60);
  for (const e of els) {
    const r0 = e.getBoundingClientRect(); if (!r0.width) continue;
    window.scrollTo(0, 0); e.focus(); const r = e.getBoundingClientRect(); const hb = hdr.getBoundingClientRect().bottom;
    if (r.height > innerHeight - hb - 8) { tall.n++; continue; }
    if (r.top < hb - 1 && scrollY > 0) out.push({ el: e.tagName + ":" + (e.textContent || "").trim().slice(0, 30), top: Math.round(r.top), hb: Math.round(hb) });
  }
  return { n: els.length, out, tall: tall.n };
};
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined });
const res = { contrast: {}, anchors: [], focus: [], anchorsChecked: 0, focusChecked: 0, tallSkipped: 0 };
const cw = (process.env.CONTRAST_WIDTHS || "1280").split(",").map(Number);   // e.g. CONTRAST_WIDTHS=320,768,1440
for (const theme of ["light", "dark"]) for (const cwid of cw) {
  const ctx = await browser.newContext({ viewport: { width: cwid, height: 800 } });
  await ctx.addInitScript(t => { try { localStorage.setItem("ccs-theme", t); } catch (e) {} }, theme);
  const pg = await ctx.newPage();
  for (const f of pages) {
    await pg.goto("file://" + f);
    for (const r of await pg.evaluate(contrastFn)) { const k = theme + " @" + cwid + " " + r.sel + " " + r.ratio; (res.contrast[k] ||= { n: 0, ex: f.replace(docs, ""), text: r.text }).n++; }
  }
  await ctx.close();
}
for (const w of (process.env.CONTRAST_ONLY ? [] : widths)) for (const mode of ["closed", "menu-open", "zoom200"]) {
  if (mode === "menu-open" && w > 900) continue;
  if (mode === "zoom200" && !(process.argv.includes("--zoom") && w >= 1280)) continue;
  const vw = mode === "zoom200" ? Math.floor(w / 2) : w;
  const ctx = await browser.newContext({ viewport: { width: vw, height: mode === "zoom200" ? 450 : 800 } }); const pg = await ctx.newPage();
  for (const f of pages) {
    await pg.goto("file://" + f); if (mode === "menu-open") { await pg.click(".menu"); await pg.waitForTimeout(30); }
    const a = await pg.evaluate(anchorFn); res.anchorsChecked += a.n; for (const o of a.out) res.anchors.push({ w, mode, page: f.replace(docs, ""), ...o });
    const fo = await pg.evaluate(focusFn); res.focusChecked += fo.n; res.tallSkipped += fo.tall; for (const o of fo.out) res.focus.push({ w, mode, page: f.replace(docs, ""), ...o });
  }
  await ctx.close();
}
await browser.close();
console.log(JSON.stringify({ pages: pages.length, anchorsChecked: res.anchorsChecked, focusChecked: res.focusChecked, tallSkipped: res.tallSkipped, anchorFailures: res.anchors.length, focusFailures: res.focus.length, contrastKinds: Object.keys(res.contrast).length, contrast: res.contrast, anchorSample: res.anchors.slice(0, 8), focusSample: res.focus.slice(0, 8) }, null, 1));
