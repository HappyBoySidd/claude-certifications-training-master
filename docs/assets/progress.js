// CCAR-F progress cues (B63-FX-12). Reads and writes only this browser's localStorage; no network calls.
// Keys: "ccs-check:<page>#<n>" = tick (shared with site.js), "ccs-checked-at:<page>#<n>" = tick date,
// "ccs-opened:<exam>:<objective>" = date opened, "ccs-last:<exam>" = last objective opened.
(function () {
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function del(k) { try { localStorage.removeItem(k); } catch (e) {} }
  function today() { return new Date().toISOString().slice(0, 10); }
  function days(d) { return d ? Math.floor((Date.now() - Date.parse(d)) / 864e5) : null; }

  document.addEventListener("DOMContentLoaded", function () {
    // Date each tick (or clear the date when unticked) so "revisit" can be based on time since checking.
    document.querySelectorAll("input[type=checkbox][data-k]").forEach(function (box) {
      box.addEventListener("change", function () {
        var k = "ccs-checked-at:" + box.getAttribute("data-k");
        if (box.checked) set(k, today()); else del(k);
        renderCue();
      });
    });

    // Objective page: remember it as the resume point and show this page's own check count.
    var cue = document.querySelector("[data-prog-obj]");
    function renderCue() {
      if (!cue) return;
      var boxes = document.querySelectorAll("input[type=checkbox][data-k]"), n = 0;
      boxes.forEach(function (b) { if (b.checked) n++; });
      cue.textContent = "";
      cue.appendChild(document.createTextNode("Your checks here: " + n + " of " + boxes.length +
        " ticked in this browser. A tick is your own record that you did the check, not proof of mastery. "));
      var a = document.createElement("a"); a.href = "progress.html"; a.textContent = "See your CCAR-F progress";
      cue.appendChild(a); cue.appendChild(document.createTextNode("."));
    }
    if (cue) {
      var obj = cue.getAttribute("data-prog-obj");
      set("ccs-last:ccar-f", obj);
      set("ccs-opened:ccar-f:" + obj, today());
      renderCue();
    }

    var mEl = document.getElementById("prog-manifest");
    if (!mEl) return;
    var m = JSON.parse(mEl.textContent), items = m.items, known = {};
    items.forEach(function (it) { it.keys.forEach(function (k) { known[k] = 1; }); });

    function render() {
      var done = 0, total = 0, objsAll = 0, objsSome = 0, next = null;
      items.forEach(function (it) {
        var ticked = 0, oldest = null;
        it.keys.forEach(function (k) {
          if (get("ccs-check:" + k) === "1") {
            ticked++;
            var d = get("ccs-checked-at:" + k);
            if (d && (!oldest || d < oldest)) oldest = d;
          }
        });
        done += ticked; total += it.keys.length;
        var opened = get("ccs-opened:ccar-f:" + it.n);
        var why;
        if (!it.keys.length) why = "This page has no checks; open it to study.";
        else if (ticked === it.keys.length) {
          objsAll++;
          var age = days(oldest);
          why = age !== null && age >= m.revisitDays
            ? "All checked, oldest " + age + " days ago. Revisit: redo a check from memory to find what has faded."
            : "All checked. Come back in about " + m.revisitDays + " days and redo one check without looking.";
        } else if (ticked) { objsSome++; why = (it.keys.length - ticked) + " check(s) left."; if (!next) next = it; }
        else { why = opened ? "Opened, no checks ticked yet." : "Not started in this browser."; if (!next) next = it; }
        var row = document.querySelector('[data-prog-row="' + it.n + '"]');
        if (!row) return;
        row.querySelector(".prog-opened").textContent = opened ? "Yes, " + opened : "Not recorded";
        row.querySelector(".prog-checked").textContent = ticked + " of " + it.keys.length;
        row.querySelector(".prog-why").textContent = why;
      });
      document.getElementById("prog-summary").textContent = "You ticked " + done + " of " + total +
        " checks. All checks ticked on " + objsAll + " of " + items.length + " objectives; some ticked on " + objsSome +
        ". These are your own ticks in this browser, not a readiness score.";

      // Resume: last objective opened, plus the first objective with checks left.
      var res = document.getElementById("prog-resume"), last = get("ccs-last:ccar-f");
      res.textContent = "";
      function line(label, it) {
        var p = document.createElement("p"); p.appendChild(document.createTextNode(label));
        var a = document.createElement("a"); a.href = it.href; a.textContent = "Objective " + it.n + " " + it.title;
        p.appendChild(a); res.appendChild(p);
      }
      var lastIt = items.filter(function (it) { return it.n === last; })[0];
      if (lastIt) line("Resume where you left off: ", lastIt);
      if (next && next !== lastIt) line("Next objective with checks left: ", next);
      if (!lastIt && !next) { var p = document.createElement("p"); p.textContent = "Every check is ticked. Revisit the objectives marked below and try fresh practice."; res.appendChild(p); }

      // Ticks saved for checks that are no longer in the course are ignored in the counts, and said so.
      var stale = 0;
      try { for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i);
        if (k && k.indexOf("ccs-check:lessons/ccar-f/objectives/") === 0 && !known[k.slice(10)]) stale++; } } catch (e) {}
      var s = document.getElementById("prog-stale");
      s.hidden = !stale;
      s.textContent = stale ? stale + " saved tick(s) belong to checks that have since changed or been removed. They are not counted. New checks start unticked." : "";
    }
    render();

    function ownKeys() {
      var out = [];
      try { for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i);
        if (k && (k.indexOf("ccs-check:lessons/ccar-f/objectives/") === 0 || k.indexOf("ccs-checked-at:lessons/ccar-f/objectives/") === 0 ||
                  k.indexOf("ccs-opened:ccar-f:") === 0 || k === "ccs-last:ccar-f")) out.push(k); } } catch (e) {}
      return out;
    }
    var msg = document.getElementById("prog-msg");
    document.getElementById("prog-export").addEventListener("click", function () {
      var data = { exam: "ccar-f", exported: today(), note: "Self-reported ticks from this browser; not a mastery or readiness score.", keys: {} };
      ownKeys().forEach(function (k) { data.keys[k] = get(k); });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }));
      a.download = "ccar-f-progress-" + today() + ".json";
      document.body.appendChild(a); a.click(); a.remove();
      msg.textContent = "Exported " + Object.keys(data.keys).length + " saved entries.";
    });
    document.getElementById("prog-reset").addEventListener("click", function () {
      if (!window.confirm("Clear all CCAR-F objective ticks, dates and the resume point in this browser? Theme and other exams stay. This cannot be undone.")) return;
      var ks = ownKeys(); ks.forEach(del);
      render();
      msg.textContent = "Cleared " + ks.length + " CCAR-F entries.";
    });
  });
})();

// Separate attempt evidence; never converts reading/checklist state into mastery.
document.addEventListener('DOMContentLoaded',function(){var target=document.getElementById('practice-evidence');if(!target)return;try{var saved=JSON.parse(localStorage.getItem('claude-cert-practice.v1')||'{}');var rows={};(saved.attempts||[]).forEach(function(a){if(!a.objective)return;var r=rows[a.objective]||(rows[a.objective]={fresh:0,right:0,repeat:0,assisted:0});if(a.evidence==='first-attempt'){r.fresh++;if(a.right)r.right++;}else if(a.evidence==='assisted')r.assisted++;else r.repeat++;});Object.keys(rows).sort().forEach(function(id){var r=rows[id],p=document.createElement('p');p.textContent='Objective '+id+': first-attempt '+r.right+'/'+r.fresh+' correct; repeats '+r.repeat+'; assisted '+r.assisted+'.';target.appendChild(p);});}catch(e){target.textContent='Practice history could not be read; saved data was preserved.';}});
