// Filled and ghost button text contrast in default, hover and focus states, both themes, every track colour. Usage: node tools/ux/check_buttons.mjs docs
import { createRequire } from "module";
const require = createRequire((process.env.PW_PATH || "/Users/akumthekar/.devbar/pkgs/npm/24.18.0/node-v24.18.0-darwin-arm64/lib/node_modules/@playwright/mcp/node_modules") + "/");
const { chromium } = require("playwright-core");
const docs = process.argv[2] || "docs"; const b = await chromium.launch(); let fail = 0, n = 0;
const ratio = (fg, bg) => { const L = c => { const [r,g,b2] = c.map(v => { v/=255; return v<=.03928?v/12.92:((v+.055)/1.055)**2.4; }); return .2126*r+.7152*g+.0722*b2; }; const a = L(fg), z = L(bg); return (Math.max(a,z)+.05)/(Math.min(a,z)+.05); };
for (const theme of ["light", "dark"]) for (const track of ["associate", "architect", "developer", "neutral"]) {
  const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } }); await ctx.addInitScript(t => localStorage.setItem("ccs-theme", t), theme);
  const p = await ctx.newPage(); await p.goto(`file://${require("path").resolve(docs)}/index.html`);
  await p.evaluate(t => { document.body.className = "t-" + t; document.documentElement.style.scrollBehavior = "auto"; document.querySelectorAll(".btn, .pill, .steps li").forEach(e => e.style.animation = "none"); }, track);
  const sel = [".btn:not(.ghost)", ".btn.ghost", ".pill", ".steps li"];
  for (const s of sel) for (const state of ["default", "hover", "focus"]) {
    const loc = p.locator(s).first(); if (!(await loc.count())) continue;
    if (state === "hover") await loc.hover(); else if (state === "focus") await loc.evaluate(e => (e.focus && e.tabIndex < 0 && e.setAttribute("tabindex", "0"), e.focus())); else await p.mouse.move(0, 0);
    const r = await loc.evaluate((e, s) => { const pe = s === ".steps li" ? getComputedStyle(e, "::before") : getComputedStyle(e); const cv = document.createElement("canvas").getContext("2d"); const px = c => { cv.clearRect(0,0,1,1); cv.fillStyle = "#000"; cv.fillStyle = c; cv.fillRect(0,0,1,1); return [...cv.getImageData(0,0,1,1).data]; }; let bg = px(pe.backgroundColor); if (bg[3] < 255) bg = px(getComputedStyle(document.body).backgroundColor); const bc = bg.slice(0,3); const fg = px(pe.color).slice(0,3); return { fg, bg: bc }; }, s);
    const k = ratio(r.fg, r.bg); n++; if (k < 4.5) { fail++; console.log("FAIL", theme, track, s, state, k.toFixed(2)); }
  }
  await ctx.close();
}
await b.close(); console.log(`button states checked: ${n}, failures: ${fail}`); process.exit(fail ? 1 : 0);
