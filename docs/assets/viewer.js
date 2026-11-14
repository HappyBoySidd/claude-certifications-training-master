/* Diagram viewer (B63-FX-16). One local script, no third-party code. It wraps each diagram that
   Mermaid draws with: a contained scroll frame, Zoom in / Zoom out / Fit diagram / Reset / Open larger,
   a text version, and (for flows that already have "Step N." sections) a guided step-by-step view.
   Without JavaScript the page is unchanged: the diagram source is shown as before. */
(function () {
  "use strict";
  var pres = Array.prototype.slice.call(document.querySelectorAll("pre.mermaid"));
  // Capture the diagram source now, before Mermaid replaces it with the drawn SVG.
  var sources = pres.map(function (p) { return p.textContent; });

  var STEP = 1.25, MIN = 0.2, MAX = 4, MAXH = function () { return Math.max(260, Math.min(window.innerHeight * 0.7, window.innerWidth >= 1600 ? 780 : 640)); };

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }
  function btn(label, fn) {
    var b = el("button", "dv-btn", label);
    b.type = "button";
    b.addEventListener("click", fn);
    return b;
  }

  // ---- text version -------------------------------------------------------------------
  // Sequence diagrams become numbered prose steps (who sends what to whom); loops, alternatives and
  // parallel branches become indented "While / If / Otherwise / At the same time" lines.
  function sequenceProse(lines) {
    var names = {}, out = [], depth = 0, n = 0, stack = [];
    function nm(id) { id = id.trim(); return names[id] || id; }
    function pad() { return new Array(depth + 1).join("    "); }
    lines.forEach(function (raw) {
      var l = raw.trim(), m;
      if (/^(sequenceDiagram|autonumber)\b/.test(l)) return;
      if ((m = l.match(/^(?:participant|actor)\s+(\S+)(?:\s+as\s+(.+))?$/))) { names[m[1]] = (m[2] || m[1]).trim(); return; }
      if ((m = l.match(/^loop\s+(.*)$/))) { out.push(pad() + "Repeat, " + m[1] + ":"); depth++; stack.push("loop"); return; }
      if ((m = l.match(/^alt\s+(.*)$/))) { out.push(pad() + "If " + m[1] + ":"); depth++; stack.push("alt"); return; }
      if ((m = l.match(/^opt\s+(.*)$/))) { out.push(pad() + "Optionally, if " + m[1] + ":"); depth++; stack.push("opt"); return; }
      if ((m = l.match(/^par\s*(.*)$/))) { out.push(pad() + "At the same time (" + m[1] + "):"); depth++; stack.push("par"); return; }
      if ((m = l.match(/^else\s*(.*)$/))) { depth = Math.max(0, depth - 1); out.push(pad() + "Otherwise, " + (m[1] || "in the other case") + ":"); depth++; return; }
      if ((m = l.match(/^and\s*(.*)$/))) { depth = Math.max(0, depth - 1); out.push(pad() + "And also (" + m[1] + "):"); depth++; return; }
      if (l === "end") { depth = Math.max(0, depth - 1); stack.pop(); return; }
      if ((m = l.match(/^Note\s+(?:over|left of|right of)\s+([^:]+):\s*(.*)$/i))) {
        out.push(pad() + "Note (" + m[1].split(",").map(nm).join(" and ") + "): " + m[2]); return;
      }
      if ((m = l.match(/^(\S+?)\s*(--?>>|--?x|--?>|-\)|--\))\s*([^:\s]+)\s*:\s*(.*)$/))) {
        n++;
        var verb = /x$/.test(m[2]) ? "fails to get a reply from" : /^--/.test(m[2]) ? "replies to" : "sends to";
        if (m[1] === m[3]) out.push(pad() + n + ". " + nm(m[1]) + " does this itself: " + m[4]);
        else out.push(pad() + n + ". " + nm(m[1]) + " " + verb + " " + nm(m[3]) + ": " + m[4]);
        return;
      }
      out.push(pad() + l);  // unrecognised line: keep it, never drop content
    });
    return out.join("\n");
  }
  function textVersion(src) {
    var lines = src.split("\n").filter(function (l) {
      return l.trim() && !/^\s*%%/.test(l) && !/^\s*(classDef|class|click|style|linkStyle)\b/.test(l);
    });
    var labels = {};
    lines.forEach(function (l) {
      var m = l.match(/^\s*([A-Za-z0-9_]+)\s*(?:\(\[|\[\[|\[|\{|\(\()\s*"([^"]*)"/);
      if (m) labels[m[1]] = m[2];
    });
    if (lines.some(function (l) { return /^\s*sequenceDiagram\b/.test(l); })) return sequenceProse(lines);
    var flow = lines.some(function (l) { return /^\s*(flowchart|graph)\b/.test(l); });
    var out = [];
    lines.forEach(function (l) {
      if (/^\s*(flowchart|graph|sequenceDiagram)\b/.test(l)) return;
      if (flow) {
        if (/^\s*[A-Za-z0-9_]+\s*(?:\(\[|\[\[|\[|\{|\(\()\s*"[^"]*"\s*(?:\]\)|\]\]|\]|\}|\)\))\s*$/.test(l)) return;
        var t = l.trim().replace(/\b([A-Za-z0-9_]+)\b(?=\s*(?:--|-\.|==|-->|$))/g, function (id) { return labels[id] || id; });
        t = t.replace(/\s*-->\s*/g, " leads to ").replace(/\s*--\s*"([^"]*)"\s*leads to\s*/g, " — if \"$1\" — goes to ").replace(/\s*-\.-\s*/g, " is linked to ");
        out.push(t);
      } else {
        out.push(l.trim());
      }
    });
    return out.join("\n");
  }

  // ---- zoom / pan controller for one frame -----------------------------------------------
  function statusEl() {
    var s = el("span", "dv-zoom");
    s.setAttribute("role", "status");
    return s;
  }
  function controller(frame, getSvg, status) {
    var c = { scale: 1, mode: "init", cap: 1 };
    function natural() {
      var s = getSvg();
      if (!s) return null;
      var vb = s.viewBox && s.viewBox.baseVal;
      var w = vb && vb.width, h = vb && vb.height;
      if (!w || !h) { var r = s.getBoundingClientRect(); w = r.width; h = r.height; }
      return w && h ? { w: w, h: h } : null;
    }
    function apply() {
      var s = getSvg(), n = natural();
      if (!s || !n) return;
      s.removeAttribute("width"); s.removeAttribute("height");
      s.style.maxWidth = "none"; s.style.minWidth = "0";
      s.style.width = Math.round(n.w * c.scale) + "px";
      s.style.height = Math.round(n.h * c.scale) + "px";
      frame.classList.toggle("dv-portrait", n.w / n.h < 0.45);
      var pct = Math.round(c.scale * 100);
      var msg = "Zoom " + pct + "%" + (c.mode === "fit" ? " (whole-diagram overview" + (c.scale < 0.85 ? "; zoom in to read" : "") + ")" : c.mode === "init" ? " (reading size; scroll inside if needed)" : "");
      if (status && status.textContent !== msg) status.textContent = msg;
    }
    function fw() { var cs = getComputedStyle(frame); return frame.clientWidth - parseFloat(cs.paddingLeft || 0) - parseFloat(cs.paddingRight || 0); }
    c.fitWidth = function () { var n = natural(); if (!n || fw() < 20) return; c.scale = Math.max(0.85, Math.min(c.cap, fw() / n.w)); c.mode = "init"; apply();
      // At reading size a branching flow may overflow horizontally. Start on its
      // first authored node, rather than an orphan branch at the left edge.
      var first = getSvg().querySelector(".node");
      if (first) {
        var nr = first.getBoundingClientRect(), fr = frame.getBoundingClientRect();
        frame.scrollLeft += nr.left + nr.width / 2 - fr.left - frame.clientLeft - frame.clientWidth / 2;
      } else frame.scrollLeft = 0;
    };
    c.fit = function () { var n = natural(); if (!n || fw() < 20) return; c.scale = Math.min(fw() / n.w, Math.max(120, c.maxH() - 34) / n.h, 1.5); c.mode = "fit"; apply(); frame.scrollLeft = 0; frame.scrollTop = 0; };
    c.maxH = function () { return frame.closest(".dv-dialog") ? Math.max(160, window.innerHeight - 260) : MAXH(); };
    c.zoom = function (f) { c.scale = Math.max(Math.min(MIN, c.scale), Math.min(MAX, c.scale * f)); c.mode = "zoom"; apply(); };
    c.reset = function () { c.fitWidth(); frame.scrollTop = 0; };
    c.refresh = function () { if (c.mode === "init") c.fitWidth(); else if (c.mode === "fit") c.fit(); else apply(); };
    if (window.ResizeObserver) {
      c.ro = new ResizeObserver(function () { if (c.mode !== "zoom") c.refresh(); });
      c.ro.observe(frame);
    }
    // Keyboard on the focused frame only: + - 0 (arrows scroll the overflowing element; Tab leaves).
    frame.addEventListener("keydown", function (e) {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.key === "+" || e.key === "=") { c.zoom(STEP); e.preventDefault(); }
      else if (e.key === "-" || e.key === "_") { c.zoom(1 / STEP); e.preventDefault(); }
      else if (e.key === "0") { c.reset(); e.preventDefault(); }
      else if (e.key.indexOf("Arrow") === 0) {
        // The overflow may sit on the inner pre, not the frame: scroll whichever one overflows.
        var dx = e.key === "ArrowLeft" ? -40 : e.key === "ArrowRight" ? 40 : 0;
        var dy = e.key === "ArrowUp" ? -40 : e.key === "ArrowDown" ? 40 : 0;
        var inner = frame.querySelector("pre");
        var cands = [frame, inner].filter(Boolean);
        for (var i = 0; i < cands.length; i++) {
          var t = cands[i], l = t.scrollLeft, tp = t.scrollTop;
          t.scrollLeft += dx; t.scrollTop += dy;
          if (t.scrollLeft !== l || t.scrollTop !== tp) { e.preventDefault(); break; }  // none moved: let the page scroll
        }
      }
    });
    // Mouse drag pans when the diagram is larger than the frame. Touch uses native scrolling.
    var drag = null;
    frame.addEventListener("pointerdown", function (e) {
      if (e.pointerType !== "mouse" || e.button !== 0 || e.target.closest('a, [role="button"], button, input, select, summary')) return;
      if (frame.scrollWidth <= frame.clientWidth && frame.scrollHeight <= frame.clientHeight) return;
      drag = { x: e.clientX, y: e.clientY, l: frame.scrollLeft, t: frame.scrollTop };
      frame.classList.add("dv-drag");
      frame.setPointerCapture(e.pointerId);
    });
    frame.addEventListener("pointermove", function (e) {
      if (!drag) return;
      frame.scrollLeft = drag.l - (e.clientX - drag.x);
      frame.scrollTop = drag.t - (e.clientY - drag.y);
    });
    function end() { drag = null; frame.classList.remove("dv-drag"); }
    frame.addEventListener("pointerup", end);
    frame.addEventListener("pointercancel", end);
    return c;
  }

  function toolbar(c, extra, status) {
    var bar = el("div", "dv-bar");
    bar.setAttribute("role", "group");
    bar.setAttribute("aria-label", "Diagram controls");
    bar.appendChild(btn("Zoom out", function () { c.zoom(1 / STEP); }));
    bar.appendChild(btn("Zoom in", function () { c.zoom(STEP); }));
    bar.appendChild(btn("Fit diagram", function () { c.fit(); }));
    bar.appendChild(btn("Reset", function () { c.reset(); }));
    (extra || []).forEach(function (b) { bar.appendChild(b); });
    bar.appendChild(status);
    return bar;
  }

  // ---- guided steps (only for flows that already have "Step N." sections) ---------------------
  function collectSteps(start) {
    var steps = [], cur = null, n = start.nextElementSibling, seenH2 = false;
    while (n) {
      var t = n.tagName;
      if (t === "H2" && !seenH2 && steps.length === 0 && /^step by step/i.test(n.textContent.trim())) { seenH2 = true; cur = null; n = n.nextElementSibling; continue; }
      if (t === "H2" || n.matches(".mmd, details.mmd-toggle") || (n.querySelector && n.querySelector("pre.mermaid"))) break;
      if (t === "H3") {
        cur = /^Step\s+\d+/i.test(n.textContent.trim()) ? { title: n.textContent.trim(), nodes: [] } : null;
        if (cur) steps.push(cur);
      } else if (cur) {
        cur.nodes.push(n); // Keep code/schema fixtures with their guided step.
      }
      n = n.nextElementSibling;
    }
    return steps.length >= 2 ? steps : null;
  }
  function stripIds(node) {
    node.removeAttribute && node.removeAttribute("id");
    node.querySelectorAll && node.querySelectorAll("[id]").forEach(function (x) { x.removeAttribute("id"); });
    return node;
  }
  function stepPanel(st, closeFn) {
    var host = el("div", "dv-steps");
    host.hidden = true;
    var head = el("p", "dv-steps-h"), body = el("div", "dv-steps-b");
    var nav = el("div", "dv-bar");
    var prev = btn("Previous step", function () { st.go(st.i - 1); });
    var next = btn("Next step", function () { st.go(st.i + 1); });
    var whole = btn("View whole flow", function () { closeFn(); });
    nav.appendChild(prev); nav.appendChild(next); nav.appendChild(whole);
    host.appendChild(head); host.appendChild(body); host.appendChild(nav);
    head.setAttribute("aria-live", "polite");
    function render() {
      var s = st.steps[st.i];
      head.textContent = "Step " + (st.i + 1) + " of " + st.steps.length + ": " + s.title.replace(/^Step\s+\d+\.?\s*/i, "");
      body.textContent = "";
      s.nodes.forEach(function (nd) { body.appendChild(stripIds(nd.cloneNode(true))); });
      prev.disabled = st.i === 0; next.disabled = st.i === st.steps.length - 1;
    }
    st.subs.push(render);
    host.dispose = function () { var k = st.subs.indexOf(render); if (k >= 0) st.subs.splice(k, 1); };
    render();
    return host;
  }

  // Clone a Mermaid SVG for the dialog with every id renamed (the SVG, its markers and its scoped <style>
  // all use the original id), so the page never holds duplicate ids and arrowheads still resolve even if
  // the original sits inside a closed <details>.
  var cloneN = 0;
  function cloneSvg(svg) {
    var copy = svg.cloneNode(true), suffix = "-lg" + (++cloneN);
    var ids = [];
    if (copy.id) ids.push(copy.id);
    copy.querySelectorAll("[id]").forEach(function (x) { ids.push(x.id); });
    if (!ids.length) return copy;
    // Longest ids first so "actor10" is not clipped by "actor1"; only rewrite id attributes and #id references
    // (CSS selectors, url(#id), href="#id"), never visible label text.
    ids.sort(function (a, b) { return b.length - a.length; });
    var html = copy.outerHTML;
    ids.forEach(function (id) {
      var esc = id.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      html = html.replace(new RegExp('(\\sid=")' + esc + '(")', "g"), "$1" + id + suffix + "$2");
      html = html.replace(new RegExp("(#)" + esc + "(?![\\w-])", "g"), "$1" + id + suffix);
    });
    var t = document.createElement("template");
    t.innerHTML = html;
    return t.content.firstElementChild;
  }

  // One semantic target per node, actor or message. Pinned reading stays outside pan/zoom.
  function annotationTargets(svg) {
    return Array.from(svg.querySelectorAll('g.node, g.actor, text.actor, text.messageText, g.edgeLabel')).filter(function(anchor) {
      return !anchor.parentElement.closest('g.node, g.actor, g.edgeLabel');
    });
  }
  function bindTeaching(svg, annotations, info, src, getSvg) {
    var bound = new WeakSet();
    function bind() {
      svg=(getSvg&&getSvg())||svg; info.svg=svg;
      annotationTargets(svg).forEach(function(anchor) {
        if (bound.has(anchor)) return;
        var label=(anchor.textContent||'').replace(/\s+/g,' ').trim();
        if (!label) return;
        bound.add(anchor); anchor.classList.add('dg-helpable');
        anchor.classList.remove('dg-inspected'); anchor.setAttribute('aria-expanded','false');
        var id=(anchor.id||'').replace(/^flowchart-/,'').replace(/-\d+$/,'');
        var related=id?src.split('\n').filter(function(line){return line.includes(id);}).join('\n'):'';
        var record=info.teaching,gated=window.CCS_CoachingIsAttemptFirst&&window.CCS_CoachingIsAttemptFirst();
        annotations.bind(anchor, {
          title:label,
          purpose:gated ? 'Attempt the exercise before opening a separate worked example.' : record ? record.plain_prompt : 'Context only: this is an authored diagram label, not a separate practice question.',
          rows:record&&!gated ? [['Technical decision',record.technical_prompt],['Why inspect this boundary',record.reason],['Related source statements',related||info.text.slice(0,650)]] : [['Diagram context',related||info.text.slice(0,650)]],
          content:record&&window.CCS_CreateDiagramCoaching ? window.CCS_CreateDiagramCoaching(record,!!info.coachingDepth,info.anchor) : null
        });
      });
    }
    bind();
    return bind;
  }

  // ---- larger view --------------------------------------------------------------------
  var dlg = null;
  function openLarger(info, invoker) {
    if (!dlg) {
      dlg = el("dialog", "dv-dialog");
      dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
      document.body.appendChild(dlg);
    }
    if (typeof dlg.showModal !== "function") return;
    var y = window.scrollY, dialogPanel = null, jumped = false;
    dlg.textContent = "";
    dlg.setAttribute("aria-label", info.title + " (larger view)");
    var head = el("div", "dv-dhead");
    head.appendChild(el("h2", "dv-dtitle", info.title));
    var close = btn("Close", function () { dlg.close(); });
    close.classList.add("dv-close");
    head.appendChild(close);
    dlg.appendChild(head);
    var frame = el("div", "dv-frame mermaid");
    frame.tabIndex = 0;
    frame.setAttribute("role", "group");
    frame.setAttribute("aria-label", info.title + ": diagram, scrollable");
    frame.__maxH = Math.max(300, window.innerHeight - 260);
    var svg = cloneSvg(info.svg);
    frame.appendChild(svg);
    var status = statusEl();
    var c = controller(frame, function () { return svg; }, status);
    var bar = toolbar(c, [], status);
    dlg.appendChild(bar);
    var surface=el("div", "dv-surface");surface.appendChild(frame);dlg.appendChild(surface);
    if(window.CCS_DiagramAnnotations){
      var expandedAnnotations=window.CCS_DiagramAnnotations.attach(surface,frame);
      bindTeaching(svg,expandedAnnotations,info,info.source||'');
    }
    if (info.st) {
      var sb, panel;
      panel = stepPanel(info.st, function () { panel.hidden = true; sb.setAttribute("aria-expanded", "false"); sb.focus(); });
      dialogPanel = panel;
      sb = btn("Step by step", function () { panel.hidden = !panel.hidden; sb.setAttribute("aria-expanded", String(!panel.hidden)); });
      sb.setAttribute("aria-expanded", "false");
      bar.insertBefore(sb, status);
      dlg.appendChild(panel);
    }
    dlg.appendChild(textDetails(info.text));
    if (info.anchor) {
      var p = el("p", "dv-orig");
      var a = el("a", "", "Go to the original section");
      a.href = "#" + info.anchor;
      a.addEventListener("click", function () { jumped = true; dlg.close(); });
      p.appendChild(a);
      dlg.appendChild(p);
    }
    dlg.addEventListener("close", function onclose() {
      dlg.removeEventListener("close", onclose);
      if (c.ro) c.ro.disconnect();
      if (dialogPanel) dialogPanel.dispose();
      dlg.textContent = "";
      if (jumped) {
        var target = info.anchor && document.getElementById(info.anchor);
        if (target) {
          if (target.tabIndex < 0 && !target.hasAttribute("tabindex")) target.setAttribute("tabindex", "-1");
          target.focus({ preventScroll: true });
          target.scrollIntoView();
        }
        return;
      }
      window.scrollTo(0, y);
      if (invoker) invoker.focus({ preventScroll: true });
    });
    dlg.showModal();
    c.cap = 1;
    c.reset();
  }

  function textDetails(text) {
    var d = el("details", "dv-text");
    d.appendChild(el("summary", "", "Text version of this diagram"));
    var pre = el("pre", "dv-pre");
    pre.textContent = text;
    d.appendChild(pre);
    return d;
  }

  // ---- wrap one drawn diagram -------------------------------------------------------------
  function enhance(pre, src) {
    var svg = pre.querySelector("svg");
    if (!svg || pre.__dv || pre.closest(".dv")) return;
    pre.__dv = true;
    var mmd = pre.closest(".mmd") || pre.parentElement;
    var h = null, n = mmd.closest("details.mmd-toggle") || mmd;
    for (var p = n.previousElementSibling; p; p = p.previousElementSibling) {
      if (/^H[1-6]$/.test(p.tagName)) { h = p; break; }
    }
    var title = h ? h.textContent.trim() : "Diagram";
    var wrap = el("div", "dv");
    mmd.parentNode.insertBefore(wrap, mmd);
    var frame = mmd;
    frame.classList.add("dv-frame");
    frame.tabIndex = 0;
    frame.setAttribute("role", "group");
    frame.setAttribute("aria-label", title + ": diagram, scrollable. Arrow keys scroll; plus and minus zoom; 0 resets.");
    var status = statusEl();
    var c = controller(frame, function () { return pre.querySelector("svg"); }, status);
    var text = textVersion(src);
    var tb = toolbar(c, [], status);
    var key=pre.dataset.teachingKey;
    var info = { title: title, svg: svg, text: text, source:src, coachingDepth:pre.dataset.coachingDepth, teaching:key&&window.CCS_COURSE_COACH&&window.CCS_COURSE_COACH.diagrams[key], anchor: (h && h.id)||pre.id, st: null };
    var steps = collectSteps(n);
    if (steps) {
      info.st = { steps: steps, i: 0, subs: [], go: function (i) { this.i = Math.max(0, Math.min(this.steps.length - 1, i)); this.subs.forEach(function (f) { f(); }); } };
    }
    var larger = btn("Open larger", function () { info.svg = pre.querySelector("svg"); openLarger(info, larger); });
    tb.insertBefore(larger, status);
    wrap.appendChild(tb);
    var surface=el("div", "dv-surface");surface.appendChild(frame);wrap.appendChild(surface);
    if (info.st) {
      var sb, panel;
      panel = stepPanel(info.st, function () { panel.hidden = true; sb.setAttribute("aria-expanded", "false"); sb.focus(); });
      sb = btn("Step by step", function () { panel.hidden = !panel.hidden; sb.setAttribute("aria-expanded", String(!panel.hidden)); });
      sb.setAttribute("aria-expanded", "false");
      tb.insertBefore(sb, larger);
      wrap.appendChild(panel);
    }
    wrap.appendChild(textDetails(text));
    wrap.appendChild(el("p", "dv-hint", "Drag or scroll the diagram to move it. With the diagram focused, arrow keys scroll it, + and - zoom, and 0 resets. Tab moves on to the next control."));
    if(window.CCS_DiagramAnnotations){
      var guide=el('div','dg-source-guide');guide.appendChild(el('strong','',title));guide.appendChild(el('span','','Inspect here: hover, focus or tap a labeled box or message. Explanations use the existing diagram and lesson text.'));frame.insertBefore(guide,frame.firstChild);
      var local=window.CCS_DiagramAnnotations.attach(surface,frame);svg.setAttribute('role','group');svg.setAttribute('aria-label',title);
      var bindLabels=bindTeaching(svg,local,info,src,function(){return pre.querySelector("svg");});
      new MutationObserver(bindLabels).observe(pre,{childList:true,subtree:true,characterData:true});
    }
    c.refresh();
    var det = n.tagName === "DETAILS" ? n : null;
    if (det) det.addEventListener("toggle", function () { if (det.open) c.refresh(); });
  }

  // Print: open every text version so the printed page keeps its text alternative.
  var reopen = [];
  window.addEventListener("beforeprint", function () {
    document.querySelectorAll("details.dv-text").forEach(function (d) { if (!d.open) { d.open = true; reopen.push(d); } });
  });
  window.addEventListener("afterprint", function () { reopen.forEach(function (d) { d.open = false; }); reopen = []; });

  var pending = new WeakSet(), captured = new WeakMap();
  pres.forEach(function(pre,i){captured.set(pre,sources[i]);});
  window.CCS_EnhanceDiagrams=function(container) {
    var targets=Array.from((container||document).querySelectorAll('pre.mermaid'));
    if(container&&container.matches&&container.matches('pre.mermaid'))targets.unshift(container);
    targets.forEach(function(pre){
      if(pre.__dv||pre.closest('.dv'))return;
      if(!captured.has(pre))captured.set(pre,pre.textContent);
      if(pre.querySelector('svg'))return enhance(pre,captured.get(pre));
      if(pending.has(pre))return;
      pending.add(pre);
      var mo=new MutationObserver(function(){if(pre.querySelector('svg')){mo.disconnect();pending.delete(pre);enhance(pre,captured.get(pre));}});
      mo.observe(pre,{childList:true,subtree:true});
    });
  };
  document.addEventListener('DOMContentLoaded',function(){window.CCS_EnhanceDiagrams(document);});
})();
