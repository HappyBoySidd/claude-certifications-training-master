/* B-71 self-report only; never changes legacy check/attempt stores. */
(function () {
  'use strict';
  const key = 'CCTScenarioSelfCheck:v1';
  let state = {version: 1, missed: {}};
  try { const saved = JSON.parse(localStorage.getItem(key) || 'null'); if (saved && saved.version === 1 && saved.missed) state = saved; } catch (_) {}
  const boxes = Array.from(document.querySelectorAll('[data-scenario-miss]'));
  function save() { try { localStorage.setItem(key, JSON.stringify(state)); } catch (_) { const msg = document.getElementById('scenario-miss-status'); if (msg) msg.textContent = 'Storage unavailable; these checks may not survive reopening.'; } }
  boxes.forEach(box => { const id = box.dataset.scenarioMiss; box.checked = !!state.missed[id]; box.addEventListener('change', () => { if (box.checked) state.missed[id] = {markedAt: new Date().toISOString(), evidence: 'self-report'}; else delete state.missed[id]; save(); }); });
  const exportButton = document.getElementById('scenario-miss-export');
  if (exportButton) exportButton.addEventListener('click', () => { const url = URL.createObjectURL(new Blob([JSON.stringify(state, null, 2)], {type: 'application/json'})); const a = document.createElement('a'); a.href = url; a.download = 'ccarf-missed-whatifs.json'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000); });
  const resetButton = document.getElementById('scenario-miss-reset');
  if (resetButton) resetButton.addEventListener('click', () => { if (!window.confirm('Reset only the scenario what-if self-checks in this browser? Existing objective and practice progress is preserved.')) return; state = {version: 1, missed: {}}; boxes.forEach(box => {box.checked = false;}); save(); document.getElementById('scenario-miss-status').textContent = 'Scenario self-checks reset; other progress preserved.'; });
}());
