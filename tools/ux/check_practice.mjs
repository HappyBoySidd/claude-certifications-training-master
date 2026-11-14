// B63-FX-11 local checks for the practice tool: counts, keyboard flow, resume/recovery, fresh vs repeated, blocked storage.
// Synthetic, disposable browser profiles only (a new context per case). Never reads anyone's saved progress.
// Usage: node tools/ux/check_practice.mjs [path/to/practice/index.html]
import { createRequire } from "module";
const require = createRequire((process.env.PW_PATH || "/Users/akumthekar/.devbar/pkgs/npm/24.18.0/node-v24.18.0-darwin-arm64/lib/node_modules/@playwright/mcp/node_modules") + "/");
const { chromium } = require("playwright-core");
const file = "file://" + require("path").resolve(process.argv[2] || "practice/index.html");
const b = await chromium.launch(); let fail = 0, n = 0;
const ok = (c, msg) => { n++; if (!c) { fail++; console.log("FAIL", msg); } else console.log("ok  ", msg); };
const KEY = "claude-cert-practice.v1";
async function open(init, opts = {}) {
  const ctx = await b.newContext({ viewport: { width: 1000, height: 900 } });
  if (init) await ctx.addInitScript(init.fn, init.arg);
  const p = await ctx.newPage(); p.on("dialog", d => d.accept());
  const errs = []; p.on("pageerror", e => errs.push(String(e))); p.errs = errs;
  await p.goto(file); return { ctx, p };
}
const counts = p => p.evaluate(() => Object.fromEntries([...document.querySelectorAll("[data-count]")].map(e => [e.dataset.count, e.textContent.trim()])));
const num = (c, k) => parseInt(c[k], 10);
const reconcile = (c, label) => ok(num(c, "drawn") === num(c, "attempted") + num(c, "skipped") && num(c, "attempted") === num(c, "correct") + num(c, "incorrect"), `${label}: counts reconcile ${JSON.stringify(c)}`);
async function selectExam(p, code) { await p.locator(`input[name=exam][value=${code}]`).check(); }
async function startDrill(p, n = 20, exam = "CCAO-F") { await selectExam(p, exam); await p.fill("#drillN", String(n)); await p.getByRole("button", { name: "Start drill" }).click(); }
const cur = p => p.evaluate(() => { const q = state.qs[state.i]; return { id: q.id, ans: q.answer, multi: q.answer.length > 1, wrong: Object.keys(q.options).filter(k => !q.answer.includes(k)) }; });
async function answerCorrect(p) { const q = await cur(p); for (const k of q.ans) await p.locator(`input[name=opt][value=${k}]`).check(); }
async function answerWrong(p) { const q = await cur(p); if (q.multi) { for (const k of q.wrong.slice(0, q.ans.length)) await p.locator(`input[name=opt][value=${k}]`).check(); } else await p.locator(`input[name=opt][value=${q.wrong[0]}]`).check(); }
async function allKeys(p, size) { return p.evaluate(() => Object.keys(DATA.exams)); }

// 1. one correct + 19 skipped
{ const { ctx, p } = await open(); await startDrill(p);
  await answerCorrect(p); await p.getByRole("button", { name: "Check answer" }).click(); await p.getByRole("button", { name: "Next" }).click();
  for (let i = 0; i < 19; i++) await p.getByRole("button", { name: "Skip" }).click();
  const c = await counts(p); reconcile(c, "1 correct + 19 skipped");
  ok(num(c, "drawn") === 20 && num(c, "attempted") === 1 && num(c, "correct") === 1 && num(c, "skipped") === 19, "1 correct + 19 skipped values");
  const body = await p.locator("body").innerText();
  ok(!/Nothing missed\./.test(body) && /Incomplete/.test(body) && !/estimated scaled score/.test(body), "incomplete drill: no Nothing missed, flagged incomplete, no scaled score");
  ok(!/\b1\/20\b.*100%/.test(body) && /1 of 1/.test(body), "headline is 1 of 1 attempted, not a perfect drill");
  ok(p.errs.length === 0, "no page errors"); await ctx.close(); }
// 2. all skipped
{ const { ctx, p } = await open(); await startDrill(p);
  for (let i = 0; i < 20; i++) await p.getByRole("button", { name: "Skip" }).click();
  const c = await counts(p); reconcile(c, "all skipped"); ok(num(c, "attempted") === 0 && num(c, "skipped") === 20, "all skipped values");
  ok(!/Nothing missed\./.test(await p.locator("body").innerText()), "all skipped: no Nothing missed"); await ctx.close(); }
// 3. all answered correctly (includes any multi-select in the draw) via keyboard-driven buttons
{ const { ctx, p } = await open(); await startDrill(p); let multi = 0;
  for (let i = 0; i < 20; i++) { if ((await cur(p)).multi) multi++; await answerCorrect(p); await p.getByRole("button", { name: "Check answer" }).click(); await p.getByRole("button", { name: i === 19 ? "See results" : "Next" }).click(); }
  const c = await counts(p); reconcile(c, "all answered"); ok(num(c, "correct") === 20 && num(c, "skipped") === 0, "all answered all correct (" + multi + " multi-select in draw)");
  ok(/Nothing missed\./.test(await p.locator("body").innerText()), "complete perfect drill may say Nothing missed"); await ctx.close(); }
// 4. multi-select: partial and exact, forced draw; wrong answers
{ const { ctx, p } = await open();
  await p.evaluate(() => { const base = DATA.questions.find(q => q.exam === "CCAO-F" && !q.warmup_only); const mk = (id, ans) => Object.assign({}, base, { id, answer: ans, explain: {} }); DATA.questions.push(mk("synthetic-multi-1", ["A", "C"]), mk("synthetic-multi-2", ["B", "C"])); const m = DATA.questions.filter(q => q.id.startsWith("synthetic-multi")); const s = DATA.questions.filter(q => q.exam === "CCAO-F" && q.answer.length === 1 && !q.warmup_only).slice(0, 1); window.__m = m.length; begin({ mode: "Quick drill", exam: "CCAO-F", qs: m.concat(s), timed: false, feedback: true }); });
  const nm = await p.evaluate(() => window.__m); ok(nm === 2, "synthetic multi-select questions injected (the public bank has none)");
  // q1 partial pick (one of the required) -> incorrect
  const q1 = await cur(p); await p.locator(`input[name=opt][value=${q1.ans[0]}]`).check(); await p.getByRole("button", { name: "Check answer" }).click();
  ok(/Not quite/.test(await p.locator("#verdict").innerText()), "partial multi-select is incorrect"); await p.getByRole("button", { name: "Next" }).click();
  await answerCorrect(p); await p.getByRole("button", { name: "Check answer" }).click(); await p.getByRole("button", { name: "Next" }).click();
  await answerWrong(p); await p.getByRole("button", { name: "Check answer" }).click(); await p.getByRole("button", { name: "See results" }).click();
  const c = await counts(p); reconcile(c, "multi-select"); ok(num(c, "correct") === 1 && num(c, "incorrect") === 2, "multi-select values " + JSON.stringify(c)); await ctx.close(); }
// 5. review mode (Fix my mistakes) from a legacy v1 save with one bad entry; migration + salvage
{ const seed = { fn: ([k]) => { if (!localStorage.getItem(k)) { const ids = JSON.parse(JSON.stringify(window.__ids || [])); } }, arg: [KEY] };
  const ctx = await b.newContext(); const p = await ctx.newPage(); await p.goto(file);
  const ids = await p.evaluate(() => DATA.questions.filter(q => q.exam === "CCAR-F" && !q.warmup_only).slice(0, 5).map(q => q.id)); await ctx.close();
  const legacy = JSON.stringify({ q: { [ids[0]]: { seen: 2, right: 1, last: false }, [ids[1]]: { seen: 1, right: 0, last: false }, [ids[2]]: { seen: 3, right: 3, last: true }, [ids[3]]: "garbage" }, runs: [{ at: 1, exam: "CCAR-F", mode: "Mock exam", right: 30, total: 60, scaled: 550 }, { nope: 1 }], prefs: { exam: "CCAR-F" } });
  const { ctx: c2, p: p2 } = await open({ fn: ([k, v]) => { if (!sessionStorage.getItem("seeded")) { localStorage.setItem(k, v); sessionStorage.setItem("seeded", "1"); } }, arg: [KEY, legacy] });
  const body = await p2.locator("body").innerText();
  ok(/unreadable and were skipped \(2\)/.test(body) && /upgraded/.test(body), "legacy save: salvaged valid entries, reported 2 skipped, reported upgrade");
  ok(/Mock exam/.test(body) && /550/.test(body), "legacy run kept and shown");
  await p2.getByRole("button", { name: "Start review" }).click();
  const qs = await p2.evaluate(() => state.qs.map(q => q.id)); ok(qs.length === 2 && qs.includes(ids[0]) && qs.includes(ids[1]), "review mode draws exactly the 2 last-wrong questions");
  await answerCorrect(p2); await p2.getByRole("button", { name: "Check answer" }).click(); await p2.getByRole("button", { name: "Next" }).click();
  await answerWrong(p2); await p2.getByRole("button", { name: "Check answer" }).click(); await p2.getByRole("button", { name: "See results" }).click();
  const c = await counts(p2); reconcile(c, "review mode"); ok(num(c, "correct") === 1 && num(c, "incorrect") === 1, "review mode values");
  const st = await p2.evaluate(k => JSON.parse(localStorage.getItem(k)), KEY); ok(st.v === 2, "store rewritten as version 2");
  const rec = st.q[ids[0]]; ok(rec.seen === 3 && Array.isArray(rec.hist), "history appended to existing record");
  const bodyr = await p2.locator("body").innerText(); ok(/New to you versus repeated/.test(bodyr) && /Repeated \(seen before\)\s+\d+\s+2/.test(bodyr.replace(/\n/g, " ")), "review: both questions counted as repeated");
  await c2.close(); }
// 5b. CCAR-F public mock is short (12 questions): honest, no estimate
{ const { ctx, p } = await open(); await selectExam(p, "CCAR-F");
  ok(/only \d+ are available/.test(await p.locator("body").innerText()), "mock card says how many questions are really available");
  await p.getByRole("button", { name: "Start mock" }).click(); const n12 = await p.evaluate(() => state.qs.length);
  await p.evaluate(() => { state.qs.forEach(q => { state.picks[q.id] = q.answer.slice(); }); finish(false); });
  const body = await p.locator("body").innerText(); ok(n12 < 60 && /not a full-length mock/.test(body) && !/estimated scaled score, not/.test(body), "short mock (" + n12 + " drawn): no estimate, says not full-length");
  await ctx.close(); }
// 6. keyboard only: exam select, start, answer, feedback, next, results, return
{ const { ctx, p } = await open(); const press = k => p.keyboard.press(k);
  const tabTo = async (sel, max = 120) => { for (let i = 0; i < max; i++) { if (await p.evaluate(s => document.activeElement && document.activeElement.matches(s), sel)) return true; await press("Tab"); } return false; };
  ok(await tabTo("input[name=exam]"), "keyboard reaches exam radios");
  await p.evaluate(() => document.querySelector("input[name=exam][value=CCAR-F]").focus()); await press("Space");
  ok(await p.evaluate(() => store.prefs.exam) === "CCAR-F", "keyboard selects exam");
  ok(await p.evaluate(() => document.activeElement.value) === "CCAR-F", "focus stays on the exam radio after re-render");
  await p.fill("#drillN", "5");
  ok(await tabTo("button.primary"), "keyboard reaches a start button");
  await p.getByRole("button", { name: "Start drill" }).focus(); await press("Enter");
  ok(await p.evaluate(() => !!state), "keyboard starts drill");
  ok(await p.evaluate(() => document.activeElement.dataset.fk) === "qhead", "focus moves to the question heading on start");
  for (let i = 0; i < 5; i++) {
    const q = await cur(p); ok(await tabTo("input[name=opt]"), "Tab reaches answer options");
    for (const k of q.ans) { await p.locator(`input[name=opt][value=${k}]`).focus(); await press("Space"); ok(await p.evaluate(() => document.activeElement.name) === "opt", "focus kept on option after pick (re-render)"); }
    await p.getByRole("button", { name: "Check answer" }).focus(); await press("Enter");
    ok(await p.evaluate(() => document.activeElement.id) === "verdict", "focus moves to feedback after check");
    await p.waitForFunction(() => /Correct\./.test(document.getElementById("live").textContent), null, { timeout: 2000 }).then(() => ok(true, "feedback announced in live region"), () => ok(false, "feedback announced in live region"));
    ok(await tabTo("[data-fk=next]", 5), "Tab from feedback reaches Next"); await press("Enter");
  }
  const body = await p.locator("body").innerText(); ok(/results/.test(body) && await p.evaluate(() => document.activeElement.dataset.fk) === "results-h", "results reached and focused by keyboard");
  const c = await counts(p); reconcile(c, "keyboard drill"); ok(num(c, "correct") === 5, "keyboard drill all correct");
  await p.getByRole("button", { name: "Back to home" }).focus(); await press("Enter"); ok(await p.evaluate(() => !state && document.querySelector("[data-fk=home-h]") !== null), "keyboard returns home");
  await ctx.close(); }
// 7. mock: reload right after start, halfway, then recover; timer semantics
{ const { ctx, p } = await open({ fn: () => {}, arg: null }); await selectExam(p, "CCAO-F"); await p.getByRole("button", { name: "Start mock" }).click();
  const before = await p.evaluate(() => ({ ids: state.qs.map(q => q.id), n: state.qs.length, left: state.endsAt - Date.now() }));
  await p.reload(); // newly-started mock reload
  let body = await p.locator("body").innerText(); ok(/mock exam in progress/i.test(body) && /Resume/.test(body) && /timer is paused/.test(body), "newly started mock survives reload and offers Resume / Discard");
  await p.getByRole("button", { name: "Resume" }).click();
  const a1 = await p.evaluate(() => ({ ids: state.qs.map(q => q.id), left: state.endsAt - Date.now() }));
  ok(JSON.stringify(a1.ids) === JSON.stringify(before.ids), "question order restored after reload");
  ok(a1.left <= before.left && before.left - a1.left < 8000, "timer restored (paused while away): " + Math.round((before.left - a1.left) / 1000) + "s lost");
  // answer 10 questions halfway, flag one, go to q 11, wait, reload
  for (let i = 0; i < 10; i++) { await answerCorrect(p); await p.getByRole("button", { name: "Next" }).click(); }
  await p.getByRole("button", { name: /Flag for review/ }).click(); await p.waitForTimeout(2200);
  const mid = await p.evaluate(() => ({ i: state.i, picks: JSON.stringify(state.picks), flags: [...state.flags], left: state.endsAt - Date.now() }));
  await p.reload(); await p.waitForTimeout(1500); await p.getByRole("button", { name: "Resume" }).click();
  const after = await p.evaluate(() => ({ i: state.i, picks: JSON.stringify(state.picks), flags: [...state.flags], left: state.endsAt - Date.now() }));
  ok(after.i === mid.i && after.picks === mid.picks && JSON.stringify(after.flags) === JSON.stringify(mid.flags), "position, 10 answers and flag restored halfway");
  ok(after.left <= mid.left && mid.left - after.left < 8000, "timer did not run while closed: " + Math.round((mid.left - after.left) / 1000) + "s difference");
  // finish with 10 of 60 answered: counts + estimate suppressed
  await p.evaluate(() => finish(false)); const c = await counts(p); reconcile(c, "mock 10/60");
  ok(num(c, "drawn") === 60 && num(c, "attempted") === 10 && num(c, "skipped") === 50, "mock 10/60 values");
  body = await p.locator("body").innerText(); ok(/No estimated scaled score/.test(body) && !/estimated scaled score, not/.test(body), "estimate suppressed when under half answered");
  ok(await p.evaluate(() => store.session) === null && !/in progress/.test(await p.evaluate(() => (renderHome(), document.body.innerText))), "finishing clears the saved session");
  const unseen = await p.evaluate(() => Object.keys(store.q).length); ok(unseen === 10, "only the 10 attempted questions entered history (skipped ones did not): " + unseen);
  await ctx.close(); }
// 8. mock full answered shows labelled estimate; fresh vs repeated
{ const { ctx, p } = await open(); await selectExam(p, "CCAO-F"); await p.getByRole("button", { name: "Start mock" }).click();
  await p.evaluate(() => { state.qs.forEach((q, i) => { state.picks[q.id] = i % 2 ? q.answer.slice() : [Object.keys(q.options).find(k => !q.answer.includes(k))]; }); });
  await p.evaluate(() => finish(false)); const c = await counts(p); reconcile(c, "full mock"); ok(num(c, "attempted") === 60 && num(c, "correct") === 30, "full mock 30 of 60");
  const body = await p.locator("body").innerText(); ok(/estimated scaled score, not an official score/.test(body), "full mock estimate is labelled not official");
  // second run of the same questions is 'repeated'
  const ids = await p.evaluate(() => store.runs.at(-1).fresh); ok(ids.n === 60, "first pass: all 60 answered were new to you");
  await p.evaluate(() => { renderHome(); }); await selectExam(p, "CCAO-F");
  await p.evaluate(() => { const qs = DATA.questions.filter(q => store.q[q.id]).slice(0, 3); begin({ mode: "Quick drill", exam: "CCAO-F", qs, timed: false, feedback: true }); });
  for (let i = 0; i < 3; i++) { await answerCorrect(p); await p.getByRole("button", { name: "Check answer" }).click(); await p.getByRole("button", { name: i === 2 ? "See results" : "Next" }).click(); }
  const run = await p.evaluate(() => store.runs.at(-1)); ok(run.repeat.n === 3 && run.fresh.n === 0, "repeated drill classed as repeated, not new");
  const rec = await p.evaluate(() => { const id = Object.keys(store.q).find(i => store.q[i].seen === 2); return store.q[id]; });
  ok(typeof rec.first === "boolean" && rec.hist.length === 2, "first attempt kept apart from latest; history has both attempts");
  await p.getByRole("button", { name: "Back to home" }).click(); const home = await p.locator("body").innerText(); ok(/First-try accuracy/.test(home) && /Latest accuracy/.test(home), "home shows first-try and latest accuracy separately");
  await ctx.close(); }
// 9. corrupt / newer / changed-bank recovery
{ const { ctx, p } = await open({ fn: ([k]) => { if (!sessionStorage.getItem("s")) { localStorage.setItem(k, "{not json"); sessionStorage.setItem("s", "1"); } }, arg: [KEY] });
  let body = await p.locator("body").innerText(); ok(/could not be read/.test(body) && /download the unreadable data/.test(body), "corrupt save: clear notice with download and fresh-start options");
  ok(await p.evaluate(k => localStorage.getItem(k + ".corrupt-backup") === "{not json", KEY), "corrupt data backed up");
  await startDrill(p, 5); for (let i = 0; i < 5; i++) await p.getByRole("button", { name: "Skip" }).click();
  ok(await p.evaluate(k => localStorage.getItem(k), KEY) === "{not json", "corrupt save is NOT overwritten while held");
  await p.getByRole("button", { name: "Back to home" }).click(); await p.getByRole("button", { name: /start fresh/ }).click();
  ok(await p.evaluate(k => JSON.parse(localStorage.getItem(k)).v, KEY) === 2, "start fresh replaces it only on request"); await ctx.close(); }
{ const { ctx, p } = await open({ fn: ([k]) => { if (!sessionStorage.getItem("s")) { localStorage.setItem(k, JSON.stringify({ v: 99, q: { x: 1 } })); sessionStorage.setItem("s", "1"); } }, arg: [KEY] });
  ok(/newer version/.test(await p.locator("body").innerText()), "newer-format save explained");
  await startDrill(p, 5); for (let i = 0; i < 5; i++) await p.getByRole("button", { name: "Skip" }).click();
  ok(await p.evaluate(k => JSON.parse(localStorage.getItem(k)).v, KEY) === 99, "newer-format save untouched"); await ctx.close(); }
{ const sess = { v: 1, mode: "Mock exam", exam: "CCAR-F", timed: true, feedback: false, qids: ["no-such-question"], i: 0, picks: {}, checked: {}, flags: [], wasSeen: {}, remainingMs: 1000 };
  const { ctx, p } = await open({ fn: ([k, v]) => { if (!sessionStorage.getItem("s")) { localStorage.setItem(k, v); sessionStorage.setItem("s", "1"); } }, arg: [KEY, JSON.stringify({ v: 2, q: {}, runs: [], prefs: {}, session: sess })] });
  const body = await p.locator("body").innerText(); ok(/cannot be resumed/.test(body) && /no longer in this question bank/.test(body) && /Discard it/.test(body), "changed question bank: session recovery message with Discard");
  await p.getByRole("button", { name: "Discard it" }).click(); ok(!/cannot be resumed/.test(await p.locator("body").innerText()), "discard clears it"); await ctx.close(); }
// 10. storage blocked
{ const { ctx, p } = await open({ fn: () => { const t = () => { throw new DOMException("blocked", "SecurityError"); }; Storage.prototype.getItem = t; Storage.prototype.setItem = t; Storage.prototype.removeItem = t; }, arg: null });
  ok(/blocking storage/.test(await p.locator("body").innerText()), "blocked storage: visible notice");
  await startDrill(p, 5); await answerCorrect(p); await p.getByRole("button", { name: "Check answer" }).click(); await p.getByRole("button", { name: "Next" }).click();
  for (let i = 0; i < 4; i++) await p.getByRole("button", { name: "Skip" }).click();
  const c = await counts(p); reconcile(c, "blocked storage"); ok(num(c, "correct") === 1 && num(c, "skipped") === 4 && p.errs.length === 0, "app fully usable with storage blocked, no errors");
  await ctx.close(); }
await b.close(); console.log(`practice checks: ${n}, failures: ${fail}`); process.exit(fail ? 1 : 0);
