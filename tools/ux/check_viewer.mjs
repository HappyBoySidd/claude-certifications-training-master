// Interaction test for the diagram viewer (B63-FX-16).
// Usage: node tools/ux/check_viewer.mjs <docs-dir> [page-relative-path ...]
// Needs playwright-core + Chromium (PW_PATH, as in check_ux.mjs). Exit code 1 if any check fails.
import { createRequire } from "module"; import path from "path";
const require = createRequire((process.env.PW_PATH || "/Users/akumthekar/.devbar/pkgs/npm/24.18.0/node-v24.18.0-darwin-arm64/lib/node_modules/@playwright/mcp/node_modules") + "/");
const { chromium } = require("playwright-core");
const docs = path.resolve(process.argv[2] || "docs");
const pages = process.argv.length > 3 ? process.argv.slice(3) : ["lessons/ccar-f/deep-practice/sequence-diagrams.html", "lessons/ccar-f/deep-practice/02-tool-design-and-mcp-integration.html"];
const sizes = [[320, 700, "320"], [375, 700, "375"], [390, 700, "390"], [640, 450, "200% zoom of 1280"], [1280, 800, "1280"]];
let fails = 0, checks = 0;
const log = (ok, msg) => { checks++; if (!ok) fails++; console.log((ok ? "PASS " : "FAIL ") + msg); };
const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
const cr = (a, b) => (Math.max(lum(a), lum(b)) + .05) / (Math.min(lum(a), lum(b)) + .05);
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined });
for (const theme of ["light", "dark"]) for (const [w, h, label] of sizes) for (const pg of pages) {
  const tag = `[${theme} ${label}px ${pg.split("/").pop()}]`;
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  await ctx.addInitScript(t => { try { localStorage.setItem("ccs-theme", t); } catch (e) {} }, theme);
  const p = await ctx.newPage(); const errs = []; p.on("pageerror", e => errs.push(String(e)));
  await p.goto("file://" + path.join(docs, pg));
  try { await p.waitForSelector(".dv .dv-frame svg", { timeout: 15000 }); } catch (e) { log(false, tag + " no enhanced diagram appeared"); await ctx.close(); continue; }
  // Mermaid draws in stages; wait until every diagram is wrapped (or 15 s).
  await p.waitForFunction(() => document.querySelectorAll(".dv").length === document.querySelectorAll("pre.mermaid").length, null, { timeout: 15000 }).catch(() => {});
  await p.waitForTimeout(500);
  const total = await p.locator("pre.mermaid").count(), enh = await p.locator(".dv").count();
  log(total === enh, `${tag} diagrams enhanced ${enh}/${total}`);
  log(errs.length === 0, `${tag} no page errors ${errs.join("|").slice(0, 100)}`);
  const ov = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  log(ov <= 0, `${tag} document overflow ${ov}px`);
  const texts = await p.$$eval(".dv details.dv-text pre", e => e.map(x => x.textContent));
  const raw = texts.filter(t => /->>|-->>|sequenceDiagram|^\s*participant\b/m.test(t));
  log(raw.length === 0, `${tag} text versions free of raw Mermaid (${texts.length} checked, ${raw.length} raw)`);
  // Diagrams may sit in a closed <details class="mmd-toggle">; open the one around the first diagram.
  await p.evaluate(() => { const d = document.querySelector(".dv").nextElementSibling; let e = document.querySelector(".dv"); for (; e; e = e.parentElement) if (e.tagName === "DETAILS") e.open = true; const n = document.querySelector(".dv + details, .dv + * details"); if (n) n.open = true; document.querySelectorAll("details.mmd-toggle").forEach((x, i) => { if (i === 0) x.open = true; }); });
  await p.waitForTimeout(400);
  const idx = await p.evaluate(() => [...document.querySelectorAll(".dv")].findIndex(d => d.querySelector(".dv-frame").getBoundingClientRect().height > 0));
  log(idx >= 0, `${tag} a visible diagram exists (index ${idx})`);
  if (idx < 0) { await ctx.close(); continue; }
  const first = p.locator(".dv").nth(idx);
  await first.scrollIntoViewIfNeeded();
  const frame = first.locator(".dv-frame"); await frame.focus();
  const z0 = await first.locator(".dv-zoom").textContent(); await p.keyboard.press("+"); await p.keyboard.press("+");
  const z1 = await first.locator(".dv-zoom").textContent(); log(z0 !== z1, `${tag} '+' zooms (${z0} -> ${z1})`);
  await p.keyboard.press("ArrowRight"); const sl = await frame.evaluate(f => f.scrollLeft);
  const canScroll = await frame.evaluate(f => f.scrollWidth > f.clientWidth);
  log(sl > 0 || !canScroll, `${tag} ArrowRight scrolls zoomed frame (scrollLeft ${sl}, scrollable ${canScroll})`);
  const o2 = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  log(o2 <= 0, `${tag} no document overflow while zoomed (${o2}px)`);
  await p.keyboard.press("0"); const z2 = await first.locator(".dv-zoom").textContent(); log(z2 === z0 && await frame.evaluate(f => f.scrollTop === 0), `${tag} '0' restores initial reading view (${z2})`);
  const dc = await p.evaluate(() => {
    const b = document.createElement("button"); b.className = "dv-btn"; b.disabled = true; b.textContent = "x"; document.querySelector(".dv-bar").appendChild(b);
    const cv = document.createElement("canvas").getContext("2d", { willReadFrequently: true });
    const rgb = c => { cv.clearRect(0, 0, 1, 1); cv.fillStyle = "#000"; cv.fillStyle = c; cv.fillRect(0, 0, 1, 1); return [...cv.getImageData(0, 0, 1, 1).data].slice(0, 3); };
    let bg = null; for (let e = b; e && !bg; e = e.parentElement) { const c = getComputedStyle(e).backgroundColor; if (!/rgba\(0, 0, 0, 0\)|transparent/.test(c)) bg = c; }
    const cs = getComputedStyle(b); const r = { fg: rgb(cs.color), bd: rgb(cs.borderTopColor), bg: rgb(bg || "#fff"), op: cs.opacity }; b.remove(); return r;
  });
  log(cr(dc.fg, dc.bg) >= 4.5 && cr(dc.bd, dc.bg) >= 3 && dc.op === "1", `${tag} disabled text ${cr(dc.fg, dc.bg).toFixed(1)}:1, border ${cr(dc.bd, dc.bg).toFixed(1)}:1, opacity ${dc.op}`);
  const btn = first.getByRole("button", { name: "Open larger" }); await btn.focus(); await p.keyboard.press("Enter");
  await p.waitForTimeout(600);
  const d = await p.evaluate(() => {
    const dl = document.querySelector("dialog.dv-dialog"); if (!dl || !dl.open) return null; const r = dl.getBoundingClientRect();
    const ids = [...document.querySelectorAll("[id]")].map(e => e.id); const dup = ids.filter((x, i) => ids.indexOf(x) !== i);
    return { l: r.left, r: r.right, b: r.bottom, vw: innerWidth, vh: innerHeight, dup: [...new Set(dup)].slice(0, 3), svg: !!dl.querySelector("svg"), sw: dl.scrollWidth - dl.clientWidth, focusIn: dl.contains(document.activeElement) };
  });
  log(!!d && d.svg, `${tag} dialog opens with diagram`);
  if (d) {
    log(d.l >= -1 && d.r <= d.vw + 1 && d.b <= d.vh + 1, `${tag} dialog inside viewport (${Math.round(d.l)}..${Math.round(d.r)} of ${d.vw}, bottom ${Math.round(d.b)} of ${d.vh})`);
    log(d.dup.length === 0, `${tag} no duplicate ids with dialog open ${d.dup.join(",")}`);
    log(d.sw <= 0, `${tag} dialog no horizontal overflow (${d.sw})`);
    log(d.focusIn, `${tag} focus moved into dialog`);
    const bb = await p.locator("dialog.dv-dialog svg").first().boundingBox();
    log(!!bb && bb.width > 20 && bb.height > 20, `${tag} dialog svg renders ${bb && Math.round(bb.width)}x${bb && Math.round(bb.height)}`);
    const o3 = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    log(o3 <= 0, `${tag} no document overflow with dialog open (${o3}px)`);
  }
  await p.keyboard.press("Escape"); await p.waitForTimeout(300);
  const back = await p.evaluate(() => ({ open: !!document.querySelector("dialog.dv-dialog[open]"), name: document.activeElement && document.activeElement.textContent.trim() }));
  log(!back.open && back.name === "Open larger", `${tag} Escape closes and focus returns to 'Open larger' (got '${back.name}')`);
  await ctx.close();
}
await browser.close();
console.log(`\n${checks - fails}/${checks} checks passed, ${fails} failed`);
process.exit(fails ? 1 : 0);
