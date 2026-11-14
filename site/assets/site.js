// Claude Certifications Study Site. Stores only theme and checklist ticks in this browser.
(function () {
  var root = document.documentElement;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  var saved = store.get("ccs-theme");
  if (saved) root.setAttribute("data-theme", saved);
  else if (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches) root.setAttribute("data-theme", "dark");

  document.addEventListener("DOMContentLoaded", function () {
    // Keep --header-h equal to the real sticky header height (wrapping, open menu, zoom) so anchors and the side list clear it.
    var top = document.querySelector(".top");
    if (top) {
      var setH = function () { root.style.setProperty("--header-h", Math.ceil(top.getBoundingClientRect().height) + "px"); };
      setH();
      if (window.ResizeObserver) new ResizeObserver(setH).observe(top);
      window.addEventListener("resize", setH);
      window.addEventListener("load", function () { setH(); if (location.hash) { var el = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (el) el.scrollIntoView(); } });
    }

    var mobileCourse = window.matchMedia("(max-width: 959px)");
    function courseLayout() { document.querySelectorAll("details.course-nav").forEach(function (d) { d.open = !mobileCourse.matches; }); }
    courseLayout(); if (mobileCourse.addEventListener) mobileCourse.addEventListener("change", courseLayout);
    // Sections on this page: closed in the HTML, opened by site.js on wide screens.
    if (window.matchMedia && !matchMedia("(max-width: 720px)").matches) {
      document.querySelectorAll("details.toc").forEach(function (d) { d.setAttribute("open", ""); });
    }

    // Open the side outline with the current page in view (scroll only the outline, not the page).
    var here = document.querySelector(".side [aria-current=page]");
    if (here) {
      var side = here.closest(".side");
      if (side && side.scrollHeight > side.clientHeight) side.scrollTop = Math.max(0, here.offsetTop - side.clientHeight / 3);
    }

    var theme = document.querySelector(".theme");
    if (theme) theme.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store.set("ccs-theme", next);
    });

    var menu = document.querySelector(".menu"), nav = document.getElementById("nav");
    if (menu && nav) menu.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menu.setAttribute("aria-expanded", open ? "true" : "false");
      if (!open && top) root.style.setProperty("--header-h", Math.ceil(top.getBoundingClientRect().height) + "px");
    });
    // A hash jump made while the menu is open closes it first, so the target is not placed under a full-height header.
    window.addEventListener("hashchange", function () {
      if (nav && nav.classList.contains("open")) { nav.classList.remove("open"); menu.setAttribute("aria-expanded", "false"); if (top) root.style.setProperty("--header-h", Math.ceil(top.getBoundingClientRect().height) + "px"); var el = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (el) el.scrollIntoView(); }
    });

    document.querySelectorAll("input[type=checkbox][data-k]").forEach(function (box) {
      var key = "ccs-check:" + box.getAttribute("data-k");
      if (store.get(key) === "1") box.checked = true;
      box.addEventListener("change", function () { store.set(key, box.checked ? "1" : "0"); });
    });

    var planner = document.querySelector(".planner");
    if (!planner) return;
    var hours = JSON.parse(planner.getAttribute("data-hours"));
    var range = document.getElementById("hpw"), out = document.getElementById("hpw-out");
    var list = planner.querySelector(".plan-out");
    var buttons = document.querySelectorAll(".chooser button");
    var path = (store.get("ccs-path") || "CCAR-F,CCAR-P,CCDV-F,CCAO-F").split(",");
    var hpw = parseInt(store.get("ccs-hpw") || range.value, 10);
    range.value = hpw;

    function render() {
      out.textContent = range.value;
      var per = parseInt(range.value, 10), total = 0;
      list.innerHTML = "";
      path.forEach(function (code) {
        var h = hours[code][0][1], weeks = Math.max(1, Math.ceil(h / per));
        total += weeks;
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = "exams/" + hours[code][1] + ".html";
        a.textContent = code;
        li.appendChild(a);
        li.appendChild(document.createTextNode(" · about " + weeks + (weeks === 1 ? " week" : " weeks") + " (" + h + " h)"));
        list.appendChild(li);
      });
      var t = document.createElement("li");
      t.className = "total";
      t.textContent = "Total: about " + total + " weeks at " + per + " hours a week";
      list.appendChild(t);
      document.querySelectorAll(".map .node").forEach(function (n) {
        var on = path.indexOf(n.getAttribute("data-code")) !== -1;
        n.classList.toggle("on", on);
        n.classList.toggle("off", !on);
      });
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-path") === path.join(",") ? "true" : "false"); });
    }
    buttons.forEach(function (b) {
      b.addEventListener("click", function () {
        path = b.getAttribute("data-path").split(",");
        store.set("ccs-path", path.join(","));
        render();
      });
    });
    range.addEventListener("input", function () { store.set("ccs-hpw", range.value); render(); });
    render();
  });

  // Flashcards (B63-FX-5): Reference mode opens or closes every answer, keeping the button where it was on screen.
  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.querySelector(".fc-all");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var on = btn.getAttribute("aria-pressed") !== "true";
      var y = btn.getBoundingClientRect().top;
      document.querySelectorAll("details.fc-a").forEach(function (d) { d.open = on; });
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.textContent = on ? "Back to study mode: hide all answers" : "Reference mode: show all answers";
      window.scrollBy(0, btn.getBoundingClientRect().top - y);
    });
  });
  // A link into a closed <details> (for example the real-life band) opens it first.
  function openTarget() {
    var id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (e) { return; }
    var el = id && document.getElementById(id);
    for (var d = el && el.closest("details"); d; d = d.parentElement && d.parentElement.closest("details")) d.open = true;
    if (el) el.scrollIntoView();
  }
  window.addEventListener("hashchange", openTarget);
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (a && a.getAttribute("href") === location.hash) setTimeout(openTarget, 0);
  });
  document.addEventListener("DOMContentLoaded", function () { if (location.hash) openTarget(); });

  // Real tooltip node: keyboard description, Escape dismissal, pointer persistence and a touch help button.
  document.addEventListener("DOMContentLoaded", function () {
    var popup = document.createElement("div"), active = null, timer;
    popup.id = "context-help"; popup.className = "tip-popup"; popup.setAttribute("role", "tooltip"); popup.hidden = true;
    document.body.appendChild(popup);
    function hide() { popup.hidden = true; if (active) { active.removeAttribute("aria-describedby"); if (active.hasAttribute("aria-expanded")) active.setAttribute("aria-expanded", "false"); } active = null; }
    function show(trigger, text) {
      clearTimeout(timer); if (active && active !== trigger) { active.removeAttribute("aria-describedby"); if (active.hasAttribute("aria-expanded")) active.setAttribute("aria-expanded", "false"); }
      active = trigger; popup.textContent = text; popup.hidden = false; trigger.setAttribute("aria-describedby", popup.id);
      var r = trigger.getBoundingClientRect();
      popup.style.left = Math.max(12, Math.min(r.left, window.innerWidth - popup.offsetWidth - 12)) + "px";
      popup.style.top = Math.max(12, Math.min(r.bottom + 6, window.innerHeight - popup.offsetHeight - 12)) + "px";
    }
    function later() { timer = setTimeout(hide, 180); }
    popup.addEventListener("pointerenter", function () { clearTimeout(timer); }); popup.addEventListener("pointerleave", later);
    document.querySelectorAll("abbr[data-tip]").forEach(function (abbr) {
      abbr.removeAttribute("tabindex"); var trigger = abbr.closest("a") || abbr;
      var help = document.createElement("button"); help.type = "button"; help.className = "context-help-button";
      help.textContent = "?"; help.setAttribute("aria-label", "Explain " + abbr.textContent); help.setAttribute("aria-expanded", "false");
      trigger.insertAdjacentElement("afterend", help);
      trigger.addEventListener("pointerenter", function () { show(trigger, abbr.dataset.tip); }); trigger.addEventListener("pointerleave", later);
      trigger.addEventListener("focus", function () { show(trigger, abbr.dataset.tip); }); trigger.addEventListener("blur", later);
      help.addEventListener("click", function () { if (active === help && !popup.hidden) { hide(); help.setAttribute("aria-expanded", "false"); } else { show(help, abbr.dataset.tip); help.setAttribute("aria-expanded", "true"); } });
      help.addEventListener("blur", later);
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !popup.hidden) { hide(); document.querySelectorAll(".context-help-button").forEach(function (b) { b.setAttribute("aria-expanded", "false"); }); } });
    window.addEventListener("resize", hide); window.addEventListener("scroll", hide, true);
  });

  // Diagrams: the pinned Mermaid copy in assets/vendor draws them in the browser; nothing is loaded from outside.
  document.addEventListener("DOMContentLoaded", function () {
    var blocks = document.querySelectorAll("pre.mermaid");
    if (!blocks.length || !window.mermaid) return;
    // The diagrams carry their own light palette, so they sit on a light card in both themes (site.css).
    window.mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: "default" });
    // Draw while every diagram is visible: Mermaid measures text, and a closed <details> measures zero.
    var openedForMeasure = [];
    blocks.forEach(function(block) { for(var d=block.closest('details');d;d=d.parentElement&&d.parentElement.closest('details')){if(!d.open){openedForMeasure.push(d);d.open=true;}} });
    window.mermaid.run({ nodes: blocks }).catch(function () {}).then(function () {
      openedForMeasure.forEach(function(d){d.open=false;});
      if (window.matchMedia && matchMedia("(max-width: 600px)").matches) {
        document.querySelectorAll("details.mmd-toggle").forEach(function (d) { d.open = false; });
      }
      if (location.hash) openTarget();  // drawing the charts moved the page; land on the target again
    });
  });
})();

// Study exposure changes freshness, never attempts, answers or scores.
window.CCS_RecordTeachingExposure=function(ids,reason){try{var key='claude-cert-practice.v1',raw=localStorage.getItem(key),s=raw?JSON.parse(raw):{};if(!s||typeof s!=='object'||Array.isArray(s))return;s.q=s.q||{};ids.forEach(function(id){var q=s.q[id]||(s.q[id]={seen:0,right:0});q.exposed=true;q.exposure_reason=reason||'Opened a teaching page containing this practice scene';});localStorage.setItem(key,JSON.stringify(s));}catch(e){}};
document.addEventListener('DOMContentLoaded',function(){var ids=[];document.querySelectorAll('[data-assessment-exposure]').forEach(function(el){ids=ids.concat(el.getAttribute('data-assessment-exposure').split(',').filter(Boolean));});if(ids.length)window.CCS_RecordTeachingExposure(ids);});

// Exact return to browser-local active practice; no selections or scores enter the URL.
document.addEventListener('DOMContentLoaded',function(){if(new URLSearchParams(location.search).get('practiceReturn')!=='1')return;var main=document.querySelector('main');if(!main)return;var a=document.createElement('a');a.className='practice-return';var script=document.querySelector('script[src*="assets/site.js"]');a.href=new URL('../practice/index.html?resume=1',script?script.src:location.href).href;a.textContent='Return to your saved practice question';main.insertBefore(a,main.firstChild);});

// Fit at first user expansion after the disclosure has measurable layout. Preserve later user zoom.
document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('details.point-aid').forEach(function(d){var fitted=false;d.addEventListener('toggle',function(){if(!d.open||fitted)return;var button=Array.from(d.querySelectorAll('button')).find(function(b){return b.textContent==='Fit diagram';});if(button){button.click();fitted=true;}});});});

// Print only the explicitly marked offline reference evidence, then restore user state.
// Does not open quiz answers, coaching gates or any other disclosure.
(function(){
  var openedForReferencePrint=[];
  window.addEventListener('beforeprint',function(){
    document.querySelectorAll('details.benchmark-reference').forEach(function(d){
      if(!d.open){d.open=true;openedForReferencePrint.push(d);}
    });
  });
  window.addEventListener('afterprint',function(){
    openedForReferencePrint.forEach(function(d){d.open=false;});
    openedForReferencePrint=[];
  });
})();
