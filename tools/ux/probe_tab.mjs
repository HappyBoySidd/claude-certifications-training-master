import { createRequire } from "module";
const require = createRequire("/Users/akumthekar/.devbar/pkgs/npm/24.18.0/node-v24.18.0-darwin-arm64/lib/node_modules/@playwright/mcp/node_modules/");
const { chromium } = require("playwright-core");
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 320, height: 700 } })).newPage();
await p.goto("file:///Users/akumthekar/code/claude-certifications-training/docs/lessons/ccar-f/index.html");
await p.addStyleTag({content:"html{scroll-behavior:auto!important}"});
for (let i = 0; i < 120; i++) { await p.keyboard.press("Tab"); const r = await p.evaluate(() => { const e = document.activeElement; const hb = document.querySelector(".top").getBoundingClientRect().bottom; const t = e.getBoundingClientRect(); return { txt: (e.textContent||"").trim().slice(0,30), top: Math.round(t.top), bottom: Math.round(t.bottom), hb, vh: innerHeight, y: Math.round(scrollY), top_: e.closest(".top") != null }; });
 if (!r.top_ && (r.top < r.hb - 1 || r.bottom > r.vh)) console.log(i, JSON.stringify(r)); }
await b.close();
