/**
 * Ecommerce Analytics Platform — API Helper
 * All fetch calls go through here so we only change BASE_URL once.
 */
const API = (() => {
  const BASE = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "";  // same-origin when served via /app

  async function request(method, path, body = null) {
    const opts = {
      method,
      headers: { "Content-Type": "application/json" },
    };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(BASE + path, opts);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || res.statusText);
    }
    return res.json();
  }

  return {
    get: (path) => request("GET", path),
    post: (path, body) => request("POST", path, body),

    // ── Domain endpoints ──────────────────────────────────────────────────
    health: () => request("GET", "/health"),
    overview: () => request("GET", "/analytics/overview"),
    performance: () => request("GET", "/analytics/performance-dashboard"),

    // Case studies
    caseStudies: () => request("GET", "/casestudies/list"),
    caseStudy: (id) => request("GET", `/casestudies/${id}`),

    // Model registry
    modelsList: () => request("GET", "/models/list"),
    modelInfo: (group) => request("GET", `/models/${group}/info`),
    allMetrics: () => request("GET", "/models/all-metrics"),
    artifacts: () => request("GET", "/models/artifacts"),

    // Predictions
    predictChurn: (features) => request("POST", "/churn/predict", features),
    churnMetrics: () => request("GET", "/churn/metrics"),
    churnImportance: () => request("GET", "/churn/feature-importance"),

    predictCLV: (features) => request("POST", "/clv/predict", features),
    clvMetrics: () => request("GET", "/clv/metrics"),
    clvComparison: () => request("GET", "/clv/model-comparison"),

    recommendSVD: (body) => request("POST", "/recommendations/svd", body),
    topItems: (n = 10) => request("POST", `/recommendations/top-items?top_n=${n}`),
    recMetrics: () => request("GET", "/recommendations/metrics"),

    predictFraud: (features) => request("POST", "/fraud/predict", features),
    fraudMetrics: () => request("GET", "/fraud/metrics"),

    predictSegment: (features) => request("POST", "/segmentation/predict", features),
    clusterProfiles: () => request("GET", "/segmentation/cluster-profiles"),
    segMetrics: () => request("GET", "/segmentation/metrics"),

    forecastDemand: (body) => request("POST", "/demand/forecast", body),
    demandMetrics: () => request("GET", "/demand/metrics"),
    demandComparison: () => request("GET", "/demand/model-comparison"),

    predictSentiment: (body) => request("POST", "/sentiment/predict", body),
    sentimentMetrics: () => request("GET", "/sentiment/metrics"),
  };
})();

// ── Utility helpers ────────────────────────────────────────────────────────────

function fmtPct(v) {
  return (v * 100).toFixed(1) + "%";
}

function fmtNum(v, decimals = 2) {
  return Number(v).toLocaleString("en-US", { maximumFractionDigits: decimals });
}

function badge(text, color = "blue") {
  const colors = {
    blue:   "bg-blue-100 text-blue-800",
    green:  "bg-green-100 text-green-800",
    red:    "bg-red-100 text-red-800",
    yellow: "bg-yellow-100 text-yellow-800",
    purple: "bg-purple-100 text-purple-800",
    gray:   "bg-gray-100 text-gray-700",
  };
  return `<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[color] || colors.blue}">${text}</span>`;
}

function metricCard(label, value, sub = "", color = "blue") {
  const border = {
    blue: "border-blue-500", green: "border-green-500",
    red: "border-red-500", yellow: "border-yellow-500",
    purple: "border-purple-500",
  };
  return `
    <div class="bg-white rounded-xl shadow-sm border-l-4 ${border[color] || border.blue} p-4">
      <p class="text-xs text-gray-500 uppercase tracking-wide">${label}</p>
      <p class="text-2xl font-bold text-gray-900 mt-1">${value}</p>
      ${sub ? `<p class="text-xs text-gray-400 mt-1">${sub}</p>` : ""}
    </div>`;
}

function showLoading(el) {
  el.innerHTML = `<div class="flex items-center justify-center h-24">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
  </div>`;
}

function showError(el, msg) {
  el.innerHTML = `<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700 text-sm">
    <strong>Error:</strong> ${msg}
  </div>`;
}

function navLink(href, label, icon, active = false) {
  const base = "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors";
  const cls = active
    ? `${base} bg-blue-600 text-white`
    : `${base} text-gray-600 hover:bg-gray-100`;
  return `<a href="${href}" class="${cls}">${icon} ${label}</a>`;
}

// Global status indicator
async function updateHealthBadge(el) {
  try {
    const h = await API.health();
    el.innerHTML = `<span class="inline-flex items-center gap-1 text-xs text-green-700 bg-green-100 px-2 py-1 rounded-full">
      <span class="w-2 h-2 bg-green-500 rounded-full"></span> API Online
    </span>`;
  } catch {
    el.innerHTML = `<span class="inline-flex items-center gap-1 text-xs text-red-700 bg-red-100 px-2 py-1 rounded-full">
      <span class="w-2 h-2 bg-red-500 rounded-full"></span> API Offline
    </span>`;
  }
}
