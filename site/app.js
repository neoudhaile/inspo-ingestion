"use strict";
/*
 * Inspo graph — the library as an interactive graph.
 *
 * Reads graph.json (written by tools/ingest/export_graph.py) straight from GitHub,
 * so the page needs no server and can be hosted anywhere. Override the source with
 * ?data=<url> (e.g. ?data=../inspo/graph.json when testing locally).
 *
 *   - nodes coloured by group, pulled into category clusters, with bridges between
 *   - scroll to zoom, drag to pan, "Fit" to reset
 *   - click a node: its summary in the side panel
 *   - hover a group in the legend: its sites light up; click it: zoom to them
 *   - Purpose / Design: two clusterings of the same sites
 */
const DEFAULT_DATA =
  "https://raw.githubusercontent.com/neoudhaile/inspo-ingestion/main/inspo/graph.json";
const DATA_URL = new URLSearchParams(location.search).get("data") || DEFAULT_DATA;

const $ = (s) => document.querySelector(s);
const el = (tag, props = {}, ...kids) => {
  const n = Object.assign(document.createElement(tag), props);
  kids.forEach((k) => n.append(k));
  return n;
};

let DATA = null, VIEW = "purpose", Graph = null;
let highlight = null;      // group id under the legend cursor
let selected = null;       // node id open in the panel
let groupById = {}, nodeById = {}, neighbours = {};

// --- forces: pull each group to its own centre, each family to its own region ---
function clusterForce() {
  let nodes = [];
  function force(alpha) {
    const cen = {};
    for (const n of nodes) {
      const c = (cen[n.group] ||= { x: 0, y: 0, k: 0 });
      c.x += n.x; c.y += n.y; c.k++;
    }
    for (const n of nodes) {
      const c = cen[n.group];
      n.vx += (c.x / c.k - n.x) * 0.12 * alpha;
      n.vy += (c.y / c.k - n.y) * 0.12 * alpha;
      n.vx += (n.ax - n.x) * 0.02 * alpha;   // family anchor
      n.vy += (n.ay - n.y) * 0.02 * alpha;
    }
  }
  force.initialize = (ns) => { nodes = ns; };
  return force;
}

function buildView(name) {
  const v = DATA.views[name];
  groupById = Object.fromEntries(v.groups.map((g) => [g.id, g]));
  const fams = v.families.map((f) => f.id);
  const R = 140 + 18 * fams.length;
  const anchor = Object.fromEntries(fams.map((f, i) => {
    const a = (i / fams.length) * 2 * Math.PI;
    return [f, { x: Math.cos(a) * R, y: Math.sin(a) * R }];
  }));
  const nodes = v.nodes.map((n) => ({
    ...n, ax: anchor[n.family].x, ay: anchor[n.family].y,
    x: anchor[n.family].x + (Math.random() - 0.5) * 40,
    y: anchor[n.family].y + (Math.random() - 0.5) * 40,
  }));
  nodeById = Object.fromEntries(nodes.map((n) => [n.id, n]));
  neighbours = {};
  for (const e of v.edges) {
    (neighbours[e.source] ||= []).push({ id: e.target, kind: e.kind, w: e.w });
    (neighbours[e.target] ||= []).push({ id: e.source, kind: e.kind, w: e.w });
  }
  return { nodes, links: v.edges.map((e) => ({ ...e })) };
}

function lit(node) { return !highlight || node.group === highlight; }

function render() {
  const data = buildView(VIEW);
  if (!Graph) {
    // Mounted on its own element: force-graph clears whatever it is mounted on, and
    // mounting it on #graph wiped the toolbar and status line along with it.
    Graph = ForceGraph()($("#canvas"))
      .backgroundColor("#111")
      .nodeId("id")
      .nodeRelSize(4)
      .nodeLabel((n) => `${n.id} — ${groupById[n.group]?.name || ""}`)
      .nodeColor((n) => (lit(n) ? groupById[n.group]?.color || "#999" : "#2a2a2a"))
      .linkColor((l) => {
        const a = typeof l.source === "object" ? l.source : nodeById[l.source];
        const b = typeof l.target === "object" ? l.target : nodeById[l.target];
        if (highlight && !(lit(a) && lit(b))) return "rgba(80,80,80,.05)";
        return l.kind === "bridge" ? "rgba(255,255,255,.28)" : "rgba(200,200,200,.12)";
      })
      .linkLineDash((l) => (l.kind === "bridge" ? [3, 3] : null))
      .linkWidth((l) => (l.kind === "bridge" ? 0.8 : 0.5))
      .onNodeClick((n) => openPanel(n.id))
      .nodeCanvasObjectMode(() => "after")
      .nodeCanvasObject((n, ctx, scale) => {
        if (n.id === selected) {
          ctx.beginPath(); ctx.arc(n.x, n.y, 7, 0, 2 * Math.PI);
          ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5 / scale; ctx.stroke();
        }
        if (scale < 2.2 || !lit(n)) return;      // labels only when zoomed in
        ctx.font = `${11 / scale}px sans-serif`;
        ctx.fillStyle = "#bbb";
        ctx.fillText(n.id, n.x + 6, n.y + 3);
      });
    // Settle in ~5s instead of the 15s default, so the fit below happens promptly.
    Graph.cooldownTime(5000);
    Graph.d3Force("charge").strength(-28);
    Graph.d3Force("cluster", clusterForce());
    new ResizeObserver(() => {
      const r = $("#graph").getBoundingClientRect();
      Graph.width(r.width).height(r.height);
    }).observe($("#graph"));
  }
  Graph.d3Force("link")
    .distance((l) => (l.kind === "bridge" ? 120 : l.kind === "sibling" ? 55 : 28))
    .strength((l) => (l.kind === "bridge" ? 0.05 : l.kind === "sibling" ? 0.2 : 0.6));
  Graph.graphData(data);
  // Fit once early (so a view switch never inherits the old zoom) and again when the
  // layout settles.
  setTimeout(() => Graph.zoomToFit(400, 40), 600);
  Graph.onEngineStop(() => { Graph.onEngineStop(() => {}); Graph.zoomToFit(400, 40); });
  renderLegend();
  renderSearch();
  const v = DATA.views[VIEW];
  $("#status").textContent =
    `${v.nodes.length} sites · ${v.groups.length} groups · ` +
    `${v.edges.filter((e) => e.kind === "bridge").length} bridges · ` +
    `updated ${DATA.generated_at.slice(0, 10)}`;
}

function renderLegend() {
  const L = $("#legend");
  L.replaceChildren();
  const v = DATA.views[VIEW];
  for (const f of v.families) {
    L.append(el("div", { className: "fam", textContent: f.name }));
    for (const g of v.groups.filter((g) => g.family === f.id)) {
      const row = el("div", { className: "grp" },
        el("span", { className: "dot", style: `background:${g.color}` }),
        el("span", { textContent: g.name }),
        el("span", { className: "n", textContent: g.size }));
      row.onmouseenter = () => { highlight = g.id; Graph.nodeColor(Graph.nodeColor()); };
      row.onmouseleave = () => { highlight = null; Graph.nodeColor(Graph.nodeColor()); };
      row.onclick = () => Graph.zoomToFit(600, 60, (n) => n.group === g.id);
      L.append(row);
    }
  }
}

function renderSearch() {
  const dl = $("#sites");
  dl.replaceChildren(...DATA.views[VIEW].nodes.map((n) =>
    el("option", { value: n.id, label: DATA.sites[n.id]?.title || "" })));
}

function openPanel(id) {
  selected = id;
  const s = DATA.sites[id] || {};
  const n = nodeById[id];
  const g = n && groupById[n.group];
  const e = s.essence || {};
  const P = $("#panel");
  const row = (label, val) => (val ? [el("dt", { textContent: label }), el("dd", { textContent: val })] : []);
  const near = (neighbours[id] || []).sort((a, b) => b.w - a.w).map((x) => {
    const a = el("a", { textContent: `${x.id}${x.kind === "bridge" ? "  ↔ other family" : ""}` });
    a.onclick = () => focus(x.id);
    return a;
  });
  P.replaceChildren(
    el("span", { id: "close", textContent: "✕", onclick: closePanel }),
    el("h2", { textContent: s.title || id }),
    el("div", { className: "meta" },
      el("a", { href: s.url || `https://${id}`, target: "_blank", rel: "noopener", textContent: id }),
      document.createTextNode(g ? `  ·  ${g.name}` : "")),
    el("dl", {},
      ...row("What it is", s.what_it_is),
      ...row("Kind", e.kind), ...row("Domain", e.domain),
      ...row("For", e.for_whom), ...row("Does", e.does),
      ...row("Hosted on", e.host),
      ...row("Design", s.how_its_designed),
      ...row("Palette", s.palette), ...row("Fonts", s.fonts),
      ...row("Status", s.site_state && `site is ${s.site_state} since capture`)),
    el("dt", { textContent: "Connected" }),
    el("div", { className: "near" }, ...near));
  $("#app").classList.add("open");
  Graph.nodeColor(Graph.nodeColor());
}

function closePanel() {
  selected = null;
  $("#app").classList.remove("open");
  Graph.nodeColor(Graph.nodeColor());
}

function focus(id) {
  const n = nodeById[id];
  if (!n) return;
  Graph.centerAt(n.x, n.y, 600);
  Graph.zoom(3, 600);
  openPanel(id);
}

// --- wiring ---------------------------------------------------------------------
document.querySelectorAll("#bar [data-view]").forEach((b) => {
  b.onclick = () => {
    VIEW = b.dataset.view;
    document.querySelectorAll("#bar [data-view]").forEach((x) => x.classList.toggle("on", x === b));
    closePanel();
    render();
  };
});
$("#fit").onclick = () => Graph.zoomToFit(500, 40);
$("#search").onchange = (ev) => { focus(ev.target.value.trim()); ev.target.value = ""; };
document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") closePanel(); });

fetch(DATA_URL)
  .then((r) => { if (!r.ok) throw new Error(`${r.status} ${r.statusText}`); return r.json(); })
  .then((d) => { DATA = d; render(); })
  .catch((err) => { $("#status").textContent = `Could not load ${DATA_URL}: ${err.message}`; });
