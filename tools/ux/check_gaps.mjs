// B63-FX-2 fix round: closes review gaps 1-5. Usage: node tools/ux/check_gaps.mjs <docs-dir> [anchor-remeasure.json]  (or CERT_SRC / ANCHOR_JSON env)
import { createRequire } from "module"; import fs from "fs"; import path from "path";
const require = createRequire((process.env.PW_PATH || "/Users/akumthekar/.devbar/pkgs/npm/24.18.0/node-v24.18.0-darwin-arm64/lib/node_modules/@playwright/mcp/node_modules") + "/");
const { chromium } = require("playwright-core");
const docs = path.resolve(process.argv[2] || "docs");
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? (e.name === "assets" ? [] : walk(path.join(d, e.name))) : e.name.endsWith(".html") ? [path.join(d, e.name)] : []);
const pages = walk(docs).sort();
// Anchor-replay data: argv[3], else $ANCHOR_JSON, else $CERT_SRC/site-audit-crew-2026-10-08/data/anchor-remeasure.json. Fail loudly with a clear message, never a bare crash.
const anchorJson = process.argv[3] || process.env.ANCHOR_JSON || (process.env.CERT_SRC ? path.join(process.env.CERT_SRC, "site-audit-crew-2026-10-08/data/anchor-remeasure.json") : "");
if (!anchorJson || !fs.existsSync(anchorJson)) { console.error("check_gaps: anchor-remeasure.json not found. Pass it as argv[3], or set ANCHOR_JSON or CERT_SRC. Tried: " + (anchorJson || "(nothing)")); process.exit(2); }
const b = await chromium.launch(); const R = {};
const vis = () => { const hb = document.querySelector(".top").getBoundingClientRect().bottom; return hb; };
// Gap 1: replay the original anchor cases by real cross-page hash arrival
{ const j = JSON.parse(fs.readFileSync(anchorJson, "utf8")); const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } }); const p = await ctx.newPage(); const rows = [];
  for (const c of j.results) { await p.goto("file://" + path.join(docs, c.page) + c.hash); await p.waitForTimeout(1200);
    const r = await p.evaluate(h => { const e = document.getElementById(decodeURIComponent(h.slice(1))); const hb = document.querySelector(".top").getBoundingClientRect().bottom; const t = e ? e.getBoundingClientRect().top : null; const end = document.documentElement.scrollHeight - innerHeight - scrollY <= 1; return { t, hb, end }; }, c.hash);
    rows.push({ ...c, now: r, hidden: r.t === null ? "missing" : (r.t < r.hb - 1 && !r.end) }); }
  R.originalEight = { n: rows.length, hidden: rows.filter(r => r.hidden).length, rows: rows.map(r => `${r.page}${r.hash} top=${Math.round(r.now.t)} hb=${Math.round(r.now.hb)} hidden=${r.hidden}`) }; await ctx.close(); }
// Gap 1b: cross-page arrivals, every page, 4 sampled hashes, widths 320/768/1440, real hash load
{ let n = 0, bad = []; for (const w of [320, 768, 1440]) { const ctx = await b.newContext({ viewport: { width: w, height: 800 } }); const p = await ctx.newPage();
  for (const f of pages) { const ids = await (async () => { await p.goto("file://" + f); return p.evaluate(() => { const a = [...document.querySelectorAll("main [id]")].filter(e => e.getBoundingClientRect().height && !e.closest("svg")).map(e => e.id); return [a[0], a[Math.floor(a.length / 2)], a[a.length - 1]].filter(Boolean); }); })();
    for (const id of new Set(ids)) { await p.goto("file://" + f + "#" + id); await p.waitForTimeout(250); n++;
      const r = await p.evaluate(id => { const e = document.getElementById(id); const hb = document.querySelector(".top").getBoundingClientRect().bottom; return { t: e.getBoundingClientRect().top, hb, end: document.documentElement.scrollHeight - innerHeight - scrollY <= 1 }; }, id);
      if (r.t < r.hb - 1 && !r.end) bad.push(`${w} ${f.replace(docs, "")}#${id}`); } await p.goto("about:blank"); }
  await ctx.close(); } R.crossPageArrivals = { n, hidden: bad.length, sample: bad.slice(0, 5) }; }
// Gap 3: header + menu per width, wrapped state, cap-and-scroll, keyboard inside menu
{ const out = []; const f = path.join(docs, "lessons/ccar-f/index.html");
  for (const w of [320, 375, 390, 768, 900, 901, 1024, 1280, 1440]) { const ctx = await b.newContext({ viewport: { width: w, height: 700 } }); const p = await ctx.newPage(); await p.goto("file://" + f);
    const closed = await p.evaluate(() => ({ hh: Math.round(document.querySelector(".top").getBoundingClientRect().height), menuBtn: getComputedStyle(document.querySelector(".menu")).display })); let open = null;
    if (closed.menuBtn !== "none") { await p.click(".menu"); await p.waitForTimeout(60);
      open = await p.evaluate(() => { const t = document.querySelector(".top"); const r = t.getBoundingClientRect(); const nav = [...t.querySelectorAll("a,button")].filter(e => e.getBoundingClientRect().width); const sc = [...t.querySelectorAll("*")].filter(e => e.scrollHeight > e.clientHeight + 1 && /(auto|scroll)/.test(getComputedStyle(e).overflowY)); return { hh: Math.round(r.height), vh: innerHeight, fits: r.height <= innerHeight + 1, scrollers: sc.length, links: nav.length }; });
      // Tab through the open menu; every focused element must be visible inside viewport and header must not exceed it
      const bad = []; for (let i = 0; i < 40; i++) { await p.keyboard.press("Tab"); const s = await p.evaluate(() => { const e = document.activeElement; const r = e.getBoundingClientRect(); const inTop = !!e.closest(".top"); return { inTop, top: Math.round(r.top), bottom: Math.round(r.bottom), vh: innerHeight, w: r.width }; }); if (s.inTop && s.w && (s.top < 0 || s.bottom > s.vh + 1)) bad.push(s); if (!s.inTop) break; }
      open.tabOffscreen = bad.length; }
    out.push({ w, closed, open }); await ctx.close(); } R.header = out; }
// Gap 2: zoom equivalent (CSS viewport halved/quartered with DPR 2/4 = Chromium browser zoom 200/400%)
{ const bad = []; let n = 0; for (const [w, h, dpr] of [[640, 450, 2], [720, 450, 2], [320, 225, 4]]) { const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dpr }); const p = await ctx.newPage();
  for (const f of pages.filter((_, i) => i % 4 === 0)) { await p.goto("file://" + f); const r = await p.evaluate(() => { const hb = document.querySelector(".top").getBoundingClientRect(); const ids = [...document.querySelectorAll("main [id]")].filter(e => e.getBoundingClientRect().height && !e.closest("svg")).map(e => e.id); document.documentElement.style.scrollBehavior = "auto"; const o = []; for (const id of ids) { const e = document.getElementById(id); e.scrollIntoView(); const t = e.getBoundingClientRect().top; const hb2 = document.querySelector(".top").getBoundingClientRect().bottom; const end = document.documentElement.scrollHeight - innerHeight - scrollY <= 1; if (t < hb2 - 1 && !end) o.push(id); } return { n: ids.length, o, hbH: hb.height, vh: innerHeight, hOverflow: document.documentElement.scrollWidth > innerWidth + 1 }; }); n += r.n; if (r.o.length) bad.push(`${w} ${f.replace(docs, "")} ${r.o.length}`); if (r.hOverflow) bad.push(`${w} hscroll ${f.replace(docs, "")}`); }
  await ctx.close(); } R.zoom = { checked: n, problems: bad.length, sample: bad.slice(0, 6) }; }
// Gap 4: contrast of hover/focus states on links, cards, nav at 375 and 1024 light+dark
{ const bad = {}; let n = 0; const sample = pages.filter((_, i) => i % 6 === 0);
  for (const theme of ["light", "dark"]) for (const w of [375, 1024]) { const ctx = await b.newContext({ viewport: { width: w, height: 800 } }); await ctx.addInitScript(t => { try { localStorage.setItem("ccs-theme", t); } catch (e) {} }, theme); const p = await ctx.newPage();
    for (const f of sample) { await p.goto("file://" + f); const sels = await p.evaluate(() => [...document.querySelectorAll("a[href], .card, summary, button")].filter(e => e.getBoundingClientRect().width && !e.closest("svg")).slice(0, 25).map((e, i) => { e.setAttribute("data-t", i); return i; }));
      for (const i of sels) for (const st of ["hover", "focus"]) { const el = p.locator(`[data-t="${i}"]`).first(); try { if (st === "hover") await el.hover({ timeout: 800, force: true }); else await el.focus({ timeout: 800 }); } catch (e) { continue; }
        const r = await p.evaluate(i => { const e = document.querySelector(`[data-t="${i}"]`); const rgba = c => { const x = document.createElement("canvas").getContext("2d", { willReadFrequently: true }); x.fillStyle = "#000"; x.fillStyle = c; x.fillRect(0, 0, 1, 1); const d = x.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
          const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
          const out = []; for (const el of [e, ...e.querySelectorAll("*")]) { if (![...el.childNodes].some(c => c.nodeType === 3 && c.textContent.trim())) continue; const cs = getComputedStyle(el); if (cs.display === "none") continue; const fg = rgba(cs.color); let bg = [255, 255, 255]; const ls = []; for (let q = el; q; q = q.parentElement) { const c = rgba(getComputedStyle(q).backgroundColor); if (c[3] > 0) ls.push(c); if (c[3] >= 1) break; } if (!ls.length || ls[ls.length - 1][3] < 1) bg = rgba(getComputedStyle(document.documentElement).backgroundColor).slice(0, 3); for (let k = ls.length - 1; k >= 0; k--) { const [r, g, b, a] = ls[k]; bg = [r * a + bg[0] * (1 - a), g * a + bg[1] * (1 - a), b * a + bg[2] * (1 - a)]; }
            const fm = [0, 1, 2].map(k => fg[k] * fg[3] + bg[k] * (1 - fg[3])); const a = lum(fm), b2 = lum(bg), ratio = (Math.max(a, b2) + .05) / (Math.min(a, b2) + .05); const sz = parseFloat(cs.fontSize); const large = sz >= 24 || (sz >= 18.66 && parseInt(cs.fontWeight) >= 700); if (ratio < (large ? 3 : 4.5)) out.push(el.tagName + "." + (el.className || "") + " " + ratio.toFixed(2)); } return out; }, i);
        n++; for (const x of r) (bad[`${theme} ${w} ${st} ${x}`] ||= []).push(f.replace(docs, "")); } } await ctx.close(); }
  R.stateContrast = { statesChecked: n, failureKinds: Object.keys(bad).length, sample: Object.entries(bad).slice(0, 8).map(([k, v]) => `${k} (${v.length}) e.g. ${v[0]}`) }; }
// Gap 5: real Tab through whole-card links taller than viewport, all lesson/exam index pages at 320
{ const ctx = await b.newContext({ viewport: { width: 320, height: 700 } }); const p = await ctx.newPage(); let tabs = 0; const bad = [];
  for (const f of pages.filter(f => /index\.html$|exams\/|scenarios/.test(f)).slice(0, 40)) { await p.goto("file://" + f); await p.addStyleTag({ content: "html{scroll-behavior:auto!important}" });
    for (let i = 0; i < 80; i++) { await p.keyboard.press("Tab"); const r = await p.evaluate(() => { const e = document.activeElement; if (e === document.body) return null; const t = e.getBoundingClientRect(); const hb = document.querySelector(".top").getBoundingClientRect().bottom; return { inTop: !!e.closest(".top"), top: t.top, bottom: t.bottom, hb, vh: innerHeight, tall: t.height > innerHeight - hb }; }); if (!r) break; tabs++;
      if (r.inTop) continue; const ok = r.tall ? (r.top < r.vh && r.bottom > r.hb) : (r.top >= r.hb - 1 && r.bottom <= r.vh + 1); if (!ok) bad.push(`${f.replace(docs, "")} #${i} top=${Math.round(r.top)} bottom=${Math.round(r.bottom)} hb=${Math.round(r.hb)}`); } }
  R.tabTall = { tabs, notVisible: bad.length, sample: bad.slice(0, 30) }; await ctx.close(); }
await b.close(); console.log(JSON.stringify(R, null, 1));
