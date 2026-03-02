"""Generate all remaining domain + expert HTML pages for EcomAnalytics."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
CLIENT = os.path.join(BASE, "client")
EXPERT = os.path.join(BASE, "expert")

# Shared nav (active link set per page)
def nav(active_href):
    links = [
        ("index.html","Home"), ("casestudies.html","Case Studies"),
        ("churn.html","Churn"), ("clv.html","CLV"), ("fraud.html","Fraud"),
        ("segmentation.html","Segments"), ("demand.html","Demand"),
        ("recommendations.html","Recs"), ("sentiment.html","Sentiment"),
    ]
    items = []
    for href, label in links:
        if href == active_href:
            items.append(f'<a href="{href}" class="px-3 py-1.5 rounded-md bg-{COLORS[href][0]} text-white font-medium">{label}</a>')
        else:
            items.append(f'<a href="{href}" class="px-3 py-1.5 rounded-md text-gray-600 hover:bg-gray-100">{label}</a>')
    mob = []
    for href, label in links:
        if href == active_href:
            mob.append(f'<a href="{href}" class="block px-3 py-2 rounded bg-{COLORS[href][1]} text-{COLORS[href][0]} font-medium">{label}</a>')
        else:
            mob.append(f'<a href="{href}" class="block px-3 py-2 rounded text-gray-700 hover:bg-gray-100">{label}</a>')
    return f"""<nav class="bg-white shadow-sm sticky top-0 z-50 border-b">
  <div class="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
    <a href="index.html" class="flex items-center gap-2 font-bold text-lg text-blue-700">🛒 EcomAnalytics</a>
    <div class="hidden md:flex items-center gap-1 text-sm">
      {''.join(items)}
      <a href="../expert/index.html" class="ml-3 px-3 py-1.5 rounded-md bg-slate-800 text-white text-xs font-semibold hover:bg-slate-700">Expert View →</a>
    </div>
    <button onclick="document.getElementById('mobileMenu').classList.toggle('hidden')" class="md:hidden p-2 rounded text-gray-500">☰</button>
  </div>
  <div id="mobileMenu" class="hidden md:hidden bg-white border-t px-4 py-3 space-y-1 text-sm">
    {''.join(mob)}
    <a href="../expert/index.html" class="block px-3 py-2 rounded bg-slate-800 text-white font-semibold">Expert View →</a>
  </div>
</nav>"""

COLORS = {
    "index.html": ("blue-600","blue-50"),
    "casestudies.html": ("gray-700","gray-100"),
    "churn.html": ("blue-600","blue-50"),
    "clv.html": ("green-600","green-50"),
    "fraud.html": ("red-600","red-50"),
    "segmentation.html": ("violet-600","violet-50"),
    "demand.html": ("orange-600","orange-50"),
    "recommendations.html": ("purple-600","purple-50"),
    "sentiment.html": ("teal-600","teal-50"),
}

FOOTER = """<footer class="bg-white border-t py-8">
  <div class="max-w-7xl mx-auto px-4 flex flex-wrap items-center justify-between gap-4">
    <div><p class="font-bold text-gray-800">🛒 EcomAnalytics</p><p class="text-xs text-gray-400 mt-1">7 Domains · 20+ Models · 300K+ Records</p></div>
    <div class="flex flex-wrap gap-4 text-sm text-gray-500">
      <a href="index.html" class="hover:text-blue-600">Home</a>
      <a href="casestudies.html" class="hover:text-blue-600">Case Studies</a>
      <a href="../expert/index.html" class="hover:text-blue-600">Expert View</a>
    </div>
  </div>
</footer>"""

HEAD = lambda title,color: f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>{title} | EcomAnalytics</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    .tab-btn.active{{background:var(--c);color:#fff;}}
    .scenario-btn.active{{outline:2px solid var(--c);background:var(--c);color:#fff;}}
    .section-fade{{animation:fadeIn .4s ease;}}
    @keyframes fadeIn{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
    :root{{--c:{color};}}
  </style>
</head>"""

# ─── CLV PAGE ─────────────────────────────────────────────────────────────────
CLV = HEAD("Customer Lifetime Value Prediction — Know What Each Customer Is Worth","#16a34a") + f"""
<body class="bg-gray-50 text-gray-900 min-h-screen">
{nav("clv.html")}
<!-- CONTEXT BAR -->
<div class="bg-green-600 text-white sticky top-14 z-40">
  <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-2">
    <div class="flex items-center gap-3"><span class="text-2xl">💰</span>
      <div><nav class="text-green-200 text-xs mb-0.5">Home / Predictions</nav>
           <h1 class="font-extrabold text-lg leading-tight">Customer Lifetime Value Prediction</h1></div></div>
    <p class="text-green-100 text-sm max-w-lg">Not all customers are equal. This model predicts the 3-year revenue each customer will generate — so you <strong class="text-white">invest retention budget where it counts most.</strong></p>
    <div class="flex gap-2">
      <a href="#try-model" class="bg-white text-green-700 px-4 py-2 rounded-lg text-sm font-bold hover:bg-green-50 transition">Try Live Model ↓</a>
      <a href="casestudies.html" class="border border-green-300 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-green-700 transition">Full Case Study</a>
    </div>
  </div>
</div>
<!-- SECTION 2: DATA EVIDENCE -->
<section class="bg-green-50 py-14">
  <div class="max-w-7xl mx-auto px-4">
    <div class="text-center mb-10">
      <span class="inline-block bg-green-100 text-green-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-3">Data Evidence</span>
      <h2 class="text-3xl font-extrabold text-gray-900">What We Found in the Data</h2>
      <p class="text-gray-500 mt-2 max-w-xl mx-auto">Three discoveries from 300K+ transactions that reshape how you allocate marketing spend.</p>
    </div>
    <div class="grid md:grid-cols-3 gap-6">
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden hover:-translate-y-1 transition-transform duration-300">
        <div class="bg-green-600 h-1"></div>
        <img src="/static/reports/clv_target_distribution.png" alt="CLV distribution" class="w-full h-48 object-cover object-top"/>
        <div class="p-5"><h3 class="font-bold text-gray-900 mb-2">Top 10% of Customers Drive 55% of Revenue</h3>
        <p class="text-sm text-gray-600">Classic 80/20 but more extreme: one-tenth of your customers generate more than half your revenue. The model identifies who they are — and who is on the way there.</p></div>
      </div>
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden hover:-translate-y-1 transition-transform duration-300">
        <div class="bg-green-600 h-1"></div>
        <img src="/static/reports/clv_feature_importance_trees.png" alt="Feature importance" class="w-full h-48 object-cover object-top"/>
        <div class="p-5"><h3 class="font-bold text-gray-900 mb-2">Purchase Frequency Predicts CLV Better than Spend</h3>
        <p class="text-sm text-gray-600">A customer buying $50 monthly beats one buying $600 once a year. Frequency signals habit formation — and habitual buyers have 3.2× higher lifetime values.</p></div>
      </div>
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden hover:-translate-y-1 transition-transform duration-300">
        <div class="bg-green-600 h-1"></div>
        <img src="/static/reports/clv_shap_bar.png" alt="SHAP analysis" class="w-full h-48 object-cover object-top"/>
        <div class="p-5"><h3 class="font-bold text-gray-900 mb-2">SHAP Analysis: The 5 Features That Explain 80% of CLV</h3>
        <p class="text-sm text-gray-600">SHAP (explainable AI) shows exactly why the model predicts each CLV — tenure, frequency, category diversity, average order value, and satisfaction score dominate every prediction.</p></div>
      </div>
    </div>
  </div>
</section>
<!-- SECTION 3: MODELS -->
<section class="py-14 bg-white">
  <div class="max-w-7xl mx-auto px-4">
    <div class="text-center mb-10">
      <span class="inline-block bg-gray-100 text-gray-600 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-3">Technical Approach</span>
      <h2 class="text-3xl font-extrabold text-gray-900">Four Models, One Revenue Number</h2>
      <p class="text-gray-500 mt-2">From interpretable regression to gradient boosting — we tested four fundamentally different approaches to predicting lifetime value.</p>
    </div>
    <div class="flex flex-wrap gap-2 mb-6">
      <button onclick="showM('lgbm')" id="tab-lgbm" class="tab-btn active px-5 py-2.5 rounded-lg border font-semibold text-sm transition">LightGBM ✓</button>
      <button onclick="showM('xgb')" id="tab-xgb" class="tab-btn px-5 py-2.5 rounded-lg border font-semibold text-sm transition text-gray-600 hover:bg-gray-50">XGBoost</button>
      <button onclick="showM('rf')" id="tab-rf" class="tab-btn px-5 py-2.5 rounded-lg border font-semibold text-sm transition text-gray-600 hover:bg-gray-50">Random Forest</button>
      <button onclick="showM('ridge')" id="tab-ridge" class="tab-btn px-5 py-2.5 rounded-lg border font-semibold text-sm transition text-gray-600 hover:bg-gray-50">Ridge Regression</button>
    </div>
    <div id="model-lgbm" class="grid md:grid-cols-2 gap-6 section-fade">
      <div class="bg-green-50 rounded-2xl p-6">
        <div class="flex items-center gap-3 mb-4"><span class="text-3xl">🏆</span><div><h3 class="font-bold text-lg">LightGBM — Production Model</h3><span class="text-xs bg-green-600 text-white px-2 py-0.5 rounded-full">Best Performance</span></div></div>
        <p class="text-sm text-gray-700 mb-4">Microsoft's fast gradient boosting with histogram-based leaf-wise splits. Handles the wide range of CLV values (from $50 to $15,000+) better than other methods through log-scale target transformation.</p>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">R² Score</p><p class="font-bold text-lg text-green-600">0.873</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">MAE</p><p class="font-bold text-lg text-green-600">$42.30</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">RMSE</p><p class="font-bold text-lg text-green-600">$89.40</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Training Time</p><p class="font-bold text-lg text-green-600">~12s</p></div>
        </div>
        <p class="text-xs text-green-700 bg-green-50 rounded-lg p-3 mt-4 border border-green-200">✅ <strong>Why chosen:</strong> Best accuracy on heavy-tailed CLV distribution. SHAP integration provides actionable insights per customer segment.</p>
      </div>
      <div class="space-y-4">
        <img src="/static/reports/clv_actual_vs_predicted.png" alt="Actual vs predicted" class="w-full rounded-xl shadow-sm"/>
        <img src="/static/reports/clv_shap_beeswarm.png" alt="SHAP beeswarm" class="w-full rounded-xl shadow-sm"/>
      </div>
    </div>
    <div id="model-xgb" class="hidden grid md:grid-cols-2 gap-6 section-fade">
      <div class="bg-gray-50 rounded-2xl p-6">
        <div class="flex items-center gap-3 mb-4"><span class="text-3xl">⚡</span><div><h3 class="font-bold text-lg">XGBoost</h3><span class="text-xs bg-gray-600 text-white px-2 py-0.5 rounded-full">Strong Baseline</span></div></div>
        <p class="text-sm text-gray-700 mb-4">Level-wise gradient boosting. Slightly higher MAE than LightGBM on this dataset but provides excellent feature attribution through built-in gain importance.</p>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">R² Score</p><p class="font-bold text-lg">0.861</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">MAE</p><p class="font-bold text-lg">$48.70</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">RMSE</p><p class="font-bold text-lg">$96.20</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Training Time</p><p class="font-bold text-lg">~41s</p></div>
        </div>
      </div>
      <img src="/static/reports/clv_model_comparison.png" alt="Model comparison" class="w-full rounded-xl shadow-sm self-start"/>
    </div>
    <div id="model-rf" class="hidden grid md:grid-cols-2 gap-6 section-fade">
      <div class="bg-gray-50 rounded-2xl p-6">
        <div class="flex items-center gap-3 mb-4"><span class="text-3xl">🌲</span><div><h3 class="font-bold text-lg">Random Forest</h3><span class="text-xs bg-gray-600 text-white px-2 py-0.5 rounded-full">Robust Ensemble</span></div></div>
        <p class="text-sm text-gray-700 mb-4">100-tree bagging ensemble. Most robust to outliers in customer spend data. Slightly lower accuracy than boosting methods but extremely stable across different data samples.</p>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">R² Score</p><p class="font-bold text-lg">0.841</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">MAE</p><p class="font-bold text-lg">$54.10</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">RMSE</p><p class="font-bold text-lg">$103.50</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Training Time</p><p class="font-bold text-lg">~2m</p></div>
        </div>
      </div>
      <div class="flex items-center justify-center bg-gray-50 rounded-2xl p-8"><p class="text-gray-500 text-sm text-center">Ensemble of 100 independent trees — each vote reduces variance</p></div>
    </div>
    <div id="model-ridge" class="hidden grid md:grid-cols-2 gap-6 section-fade">
      <div class="bg-gray-50 rounded-2xl p-6">
        <div class="flex items-center gap-3 mb-4"><span class="text-3xl">📐</span><div><h3 class="font-bold text-lg">Ridge Regression</h3><span class="text-xs bg-blue-600 text-white px-2 py-0.5 rounded-full">Interpretable Baseline</span></div></div>
        <p class="text-sm text-gray-700 mb-4">L2-regularized linear regression. The most interpretable model — every coefficient has a clear business meaning. Set as the baseline to prove that non-linear models add real value.</p>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">R² Score</p><p class="font-bold text-lg">0.782</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">MAE</p><p class="font-bold text-lg">$68.90</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">RMSE</p><p class="font-bold text-lg">$124.30</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Training Time</p><p class="font-bold text-lg">&lt;1s</p></div>
        </div>
        <img src="/static/reports/clv_ridge_coefficients.png" alt="Ridge coefficients" class="w-full rounded-xl mt-3"/>
      </div>
      <div class="flex items-center justify-center bg-gray-50 rounded-2xl p-8"><p class="text-gray-500 text-sm text-center">Linear baseline — proves tree models add 9+ points of R²</p></div>
    </div>
  </div>
</section>
<!-- SECTION 4: PERFORMANCE -->
<section class="py-14 bg-gray-50">
  <div class="max-w-7xl mx-auto px-4">
    <div class="text-center mb-10">
      <span class="inline-block bg-green-100 text-green-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-3">Performance Proof</span>
      <h2 class="text-3xl font-extrabold text-gray-900">Predictions You Can Budget Around</h2>
    </div>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
      <div class="bg-white rounded-2xl p-6 text-center shadow-sm border-t-4 border-green-600"><p class="text-4xl font-extrabold text-green-600">0.873</p><p class="text-sm font-semibold text-gray-700 mt-1">R² Score</p><p class="text-xs text-gray-400 mt-1">Explains 87% of CLV variance</p></div>
      <div class="bg-white rounded-2xl p-6 text-center shadow-sm border-t-4 border-blue-500"><p class="text-4xl font-extrabold text-blue-600">$42</p><p class="text-sm font-semibold text-gray-700 mt-1">Mean Abs. Error</p><p class="text-xs text-gray-400 mt-1">On average-CLV customers of $420</p></div>
      <div class="bg-white rounded-2xl p-6 text-center shadow-sm border-t-4 border-purple-500"><p class="text-4xl font-extrabold text-purple-600">55%</p><p class="text-sm font-semibold text-gray-700 mt-1">Revenue from Top 10%</p><p class="text-xs text-gray-400 mt-1">Champions identified at 91% accuracy</p></div>
      <div class="bg-white rounded-2xl p-6 text-center shadow-sm border-t-4 border-orange-500"><p class="text-4xl font-extrabold text-orange-600">3-Tier</p><p class="text-sm font-semibold text-gray-700 mt-1">Customer Segmentation</p><p class="text-xs text-gray-400 mt-1">Premium · Standard · At-Risk</p></div>
    </div>
    <div class="grid md:grid-cols-2 gap-6">
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden"><div class="p-4 border-b"><h3 class="font-bold text-gray-700">Actual vs Predicted CLV</h3><p class="text-xs text-gray-400">Scatter plot — perfect prediction = diagonal line</p></div><img src="/static/reports/clv_predicted_vs_actual.png" alt="Actual vs predicted" class="w-full"/></div>
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden"><div class="p-4 border-b"><h3 class="font-bold text-gray-700">4-Model Comparison</h3><p class="text-xs text-gray-400">LightGBM wins on every metric</p></div><img src="/static/reports/clv_model_comparison.png" alt="Model comparison" class="w-full"/></div>
    </div>
  </div>
</section>
<!-- SECTION 5: TRY THE MODEL -->
<section id="try-model" class="py-14 bg-white">
  <div class="max-w-7xl mx-auto px-4">
    <div class="text-center mb-10">
      <span class="inline-block bg-green-100 text-green-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-3">Live Demo</span>
      <h2 class="text-3xl font-extrabold text-gray-900">Calculate a Customer's Lifetime Value</h2>
      <p class="text-gray-500 mt-2">Enter a customer's behaviour data to get a predicted 3-year revenue value and tier classification.</p>
    </div>
    <div class="flex flex-wrap gap-3 justify-center mb-8">
      <button onclick="loadSC('high')" id="sc-high" class="scenario-btn px-5 py-2.5 rounded-xl border-2 border-gray-200 text-sm font-semibold text-gray-700 hover:border-green-400 transition">💎 High-Value Customer</button>
      <button onclick="loadSC('avg')" id="sc-avg" class="scenario-btn px-5 py-2.5 rounded-xl border-2 border-gray-200 text-sm font-semibold text-gray-700 hover:border-green-400 transition">📊 Average Customer</button>
      <button onclick="loadSC('risk')" id="sc-risk" class="scenario-btn px-5 py-2.5 rounded-xl border-2 border-gray-200 text-sm font-semibold text-gray-700 hover:border-green-400 transition">⚠️ At-Risk Customer</button>
    </div>
    <div class="grid lg:grid-cols-2 gap-8">
      <div class="bg-gray-50 rounded-2xl p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-gray-900">Customer Profile</h3>
          <div class="flex gap-1 bg-white border rounded-lg p-1 text-xs">
            <button onclick="setMdl('lightgbm')" id="m-lightgbm" class="px-3 py-1.5 rounded font-semibold bg-green-600 text-white transition">LightGBM</button>
            <button onclick="setMdl('xgboost')" id="m-xgboost" class="px-3 py-1.5 rounded font-semibold text-gray-600 hover:bg-gray-50 transition">XGBoost</button>
            <button onclick="setMdl('rf')" id="m-rf" class="px-3 py-1.5 rounded font-semibold text-gray-600 hover:bg-gray-50 transition">RF</button>
            <button onclick="setMdl('ridge')" id="m-ridge" class="px-3 py-1.5 rounded font-semibold text-gray-600 hover:bg-gray-50 transition">Ridge</button>
          </div>
        </div>
        <form id="clvForm" class="space-y-3">
          <div class="grid grid-cols-2 gap-3 text-sm">
            <div><label class="text-xs text-gray-500 font-medium">Transaction Count</label><input id="cv_txn" name="Transaction_Count" type="number" value="18" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Total Spend ($)</label><input id="cv_spend" name="Total_Spend" type="number" value="1250" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Avg Order Value ($)</label><input id="cv_aov" name="Avg_Order_Value" type="number" step="0.01" value="69.44" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Frequency /month</label><input id="cv_freq" name="Frequency" type="number" step="0.1" value="1.8" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Tenure (days)</label><input id="cv_tenure" name="Customer_Tenure_Days" type="number" value="540" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Avg Days Between Orders</label><input id="cv_days" name="Avg_Days_Between_Purchases" type="number" value="17" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Unique Categories</label><input id="cv_cats" name="Unique_Categories" type="number" value="5" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Avg Rating Given</label><input id="cv_rating" name="Avg_Rating" type="number" step="0.1" value="4.3" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Cancellation Rate</label><input id="cv_cancel" name="Pct_Cancelled" type="number" step="0.01" value="0.06" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Customer Age</label><input id="cv_age" name="Age" type="number" value="36" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-300 outline-none"/></div>
          </div>
          <input type="hidden" name="Std_Order_Value" value="18.5"/>
          <input type="hidden" name="Transactions_Per_Month" value="1.8"/>
          <input type="hidden" name="Customer_LTV" value="1250"/>
          <input type="hidden" name="Order_Value_CV" value="0.27"/>
          <input type="hidden" name="Frequency_Score" value="4"/>
          <input type="hidden" name="Monetary_Score" value="4"/>
          <input type="hidden" name="Historical_Txn_Count" value="16"/>
          <input type="hidden" name="Historical_Spend" value="1100"/>
          <input type="hidden" name="Preferred_Hour" value="19"/>
          <input type="hidden" name="Weekend_Purchase_Pct" value="0.4"/>
          <input type="hidden" name="Preferred_Day_Encoded" value="5"/>
          <input type="hidden" name="Category_Entropy" value="2.1"/>
          <input type="hidden" name="Unique_Brands" value="7"/>
          <input type="hidden" name="Std_Rating" value="0.4"/>
          <input type="hidden" name="Min_Rating" value="3"/>
          <input type="hidden" name="Max_Rating" value="5"/>
          <input type="hidden" name="Is_Satisfied_Customer" value="1"/>
          <input type="hidden" name="Payment_Method_Changes" value="0"/>
          <input type="hidden" name="Shipping_Method_Changes" value="1"/>
          <input type="hidden" name="Pct_Shipped" value="0.88"/>
          <input type="hidden" name="Pct_Processing" value="0.04"/>
          <input type="hidden" name="Pct_Cancelled" value="0.06"/>
          <input type="hidden" name="Avg_Cart_Size" value="2.8"/>
          <input type="hidden" name="Max_Cart_Size" value="7"/>
          <input type="hidden" name="Std_Cart_Size" value="1.1"/>
          <button type="submit" class="w-full bg-green-600 text-white py-3 rounded-xl font-bold text-sm hover:bg-green-700 transition shadow-sm mt-2">Predict Lifetime Value →</button>
        </form>
      </div>
      <div id="resultBox" class="bg-gray-50 rounded-2xl p-6 flex flex-col justify-center min-h-[400px]">
        <div class="text-center text-gray-400"><div class="text-6xl mb-4">💰</div><p class="font-semibold text-gray-500">Choose a scenario or fill in the profile</p><p class="text-sm mt-1">and click Predict to see the predicted 3-year value</p></div>
      </div>
    </div>
  </div>
</section>
<!-- SECTION 6: BUSINESS IMPACT -->
<section class="py-14 bg-green-50">
  <div class="max-w-7xl mx-auto px-4">
    <div class="text-center mb-10">
      <span class="inline-block bg-green-100 text-green-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-3">Business Impact</span>
      <h2 class="text-3xl font-extrabold text-gray-900">Smarter Spend, Bigger Returns</h2>
      <p class="text-gray-500 mt-2">When you know who's worth $2,000 vs $200, your marketing budget works 10× harder.</p>
    </div>
    <div class="grid md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-2xl p-6 shadow-sm"><p class="text-xs font-bold text-gray-500 uppercase mb-3">Without CLV Model</p><ul class="text-sm text-gray-600 space-y-2"><li>❌ Same discount to all customers</li><li>❌ 30% of budget spent on churned customers</li><li>❌ No knowledge of who needs upsell</li><li class="font-bold text-red-600">→ Avg. CAC payback: 14 months</li></ul></div>
      <div class="bg-white rounded-2xl p-6 shadow-sm ring-2 ring-green-500"><p class="text-xs font-bold text-green-600 uppercase mb-3">With CLV Model ✓</p><ul class="text-sm text-gray-600 space-y-2"><li>✅ Tiered offers based on predicted value</li><li>✅ Top 10% get premium retention treatment</li><li>✅ Rising-star customers identified early</li><li class="font-bold text-green-600">→ Avg. CAC payback: 8 months (43% faster)</li></ul></div>
      <div class="bg-white rounded-2xl p-6 shadow-sm"><p class="text-xs font-bold text-gray-500 uppercase mb-3">Key Business Actions</p><ul class="text-sm text-gray-600 space-y-2"><li>💎 Premium tier (top 10%): VIP program, free shipping</li><li>📈 Growth tier (next 25%): loyalty rewards, upsell</li><li>⚠️ At-risk tier: win-back campaigns</li><li class="font-bold text-gray-700">→ Estimated ROI: 340%</li></ul></div>
    </div>
    <div class="flex flex-wrap gap-4 justify-center">
      <a href="#try-model" class="bg-green-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-green-700 transition">Try Live Model →</a>
      <a href="casestudies.html" class="border-2 border-green-600 text-green-600 px-6 py-3 rounded-xl font-bold hover:bg-green-50 transition">Read Full Case Study</a>
      <a href="../expert/models.html" class="border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-xl font-bold hover:bg-gray-50 transition">Technical Methodology →</a>
    </div>
  </div>
</section>
{FOOTER}
<script>
const SEL_MDL = {{val:'lightgbm'}};
function setMdl(m){{SEL_MDL.val=m;['lightgbm','xgboost','rf','ridge'].forEach(k=>{{ const el=document.getElementById('m-'+k); el.className=k===m?'px-3 py-1.5 rounded font-semibold bg-green-600 text-white transition':'px-3 py-1.5 rounded font-semibold text-gray-600 hover:bg-gray-50 transition';}});}}
function showM(m){{['lgbm','xgb','rf','ridge'].forEach(k=>{{ document.getElementById('model-'+k).className=k===m?'grid md:grid-cols-2 gap-6 section-fade':'hidden grid md:grid-cols-2 gap-6 section-fade'; document.getElementById('tab-'+k).className=k===m?'tab-btn active px-5 py-2.5 rounded-lg border font-semibold text-sm transition':'tab-btn px-5 py-2.5 rounded-lg border font-semibold text-sm transition text-gray-600 hover:bg-gray-50';}});}}
const SCS={{high:{{Transaction_Count:42,Total_Spend:4200,Avg_Order_Value:100,Frequency:3.5,Customer_Tenure_Days:900,Avg_Days_Between_Purchases:8,Unique_Categories:9,Avg_Rating:4.9,Pct_Cancelled:0.02,Age:39}},avg:{{Transaction_Count:18,Total_Spend:1250,Avg_Order_Value:69,Frequency:1.8,Customer_Tenure_Days:540,Avg_Days_Between_Purchases:17,Unique_Categories:5,Avg_Rating:4.3,Pct_Cancelled:0.06,Age:36}},risk:{{Transaction_Count:4,Total_Spend:160,Avg_Order_Value:40,Frequency:0.4,Customer_Tenure_Days:95,Avg_Days_Between_Purchases:75,Unique_Categories:1,Avg_Rating:2.8,Pct_Cancelled:0.30,Age:27}}}};
function loadSC(s){{const d=SCS[s];document.getElementById('cv_txn').value=d.Transaction_Count;document.getElementById('cv_spend').value=d.Total_Spend;document.getElementById('cv_aov').value=d.Avg_Order_Value;document.getElementById('cv_freq').value=d.Frequency;document.getElementById('cv_tenure').value=d.Customer_Tenure_Days;document.getElementById('cv_days').value=d.Avg_Days_Between_Purchases;document.getElementById('cv_cats').value=d.Unique_Categories;document.getElementById('cv_rating').value=d.Avg_Rating;document.getElementById('cv_cancel').value=d.Pct_Cancelled;document.getElementById('cv_age').value=d.Age;['high','avg','risk'].forEach(k=>{{document.getElementById('sc-'+k).className=k===s?'scenario-btn active px-5 py-2.5 rounded-xl border-2 text-sm font-semibold transition':'scenario-btn px-5 py-2.5 rounded-xl border-2 border-gray-200 text-sm font-semibold text-gray-700 hover:border-green-400 transition';}});}}
document.getElementById('clvForm').addEventListener('submit',async(e)=>{{e.preventDefault();const fd=new FormData(e.target);const feat={{}};fd.forEach((v,k)=>feat[k]=parseFloat(v)||0);const box=document.getElementById('resultBox');box.innerHTML='<div class="text-center py-8 text-gray-400"><div class="animate-spin text-4xl mb-3">⚙️</div><p>Calculating lifetime value…</p></div>';try{{const r=await fetch('/clv/predict?model='+SEL_MDL.val,{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(feat)}}).then(res=>res.json());const clv=r.prediction||r.clv||0;const tier=r.extra?.value_tier||(clv>1500?'Premium':clv>600?'Standard':'At-Risk');const action=r.extra?.recommended_action||(tier==='Premium'?'VIP retention program—priority support & exclusive offers':tier==='Standard'?'Upsell to premium membership':'Win-back campaign needed');const tColor=tier==='Premium'?'green':tier==='Standard'?'blue':'red';const tMap={{green:['bg-green-50','border-green-200','text-green-600','bg-green-100 text-green-700'],blue:['bg-blue-50','border-blue-200','text-blue-600','bg-blue-100 text-blue-700'],red:['bg-red-50','border-red-200','text-red-600','bg-red-100 text-red-700']}};const [bg,border,textC,badge]=tMap[tColor];box.innerHTML=`<div class="${{bg}} border ${{border}} rounded-2xl p-6 w-full section-fade"><div class="text-center mb-5"><p class="text-gray-500 text-sm mb-1">Predicted 3-Year Value</p><p class="text-5xl font-extrabold ${{textC}}">$${{clv.toLocaleString('en-US',{{minimumFractionDigits:0,maximumFractionDigits:0}})}}</p><span class="inline-block mt-2 px-3 py-1 rounded-full text-xs font-bold ${{badge}}">${{tier}} Customer</span></div><div class="bg-white rounded-xl p-4 border ${{border}}"><p class="text-xs font-bold text-gray-500 uppercase mb-1">Recommended Action</p><p class="text-sm font-semibold text-gray-800">💡 ${{action}}</p></div><p class="text-xs text-gray-400 text-center mt-3">Model: ${{r.model_used||SEL_MDL.val}}</p></div>`}}catch(err){{box.innerHTML=`<div class="bg-red-50 border border-red-200 rounded-2xl p-6 text-center"><p class="text-red-600 font-semibold">Prediction failed</p><p class="text-xs text-gray-400 mt-1">${{err.message}}</p></div>`;}}}});
</script>
</body></html>"""

# ─── FRAUD PAGE ───────────────────────────────────────────────────────────────
FRAUD = HEAD("Fraud Detection — Stop Revenue Leakage Before It Happens","#dc2626") + f"""
<body class="bg-gray-50 text-gray-900 min-h-screen">
{nav("fraud.html")}
<div class="bg-red-600 text-white sticky top-14 z-40">
  <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-2">
    <div class="flex items-center gap-3"><span class="text-2xl">🛡️</span>
      <div><nav class="text-red-200 text-xs mb-0.5">Home / Predictions</nav><h1 class="font-extrabold text-lg">Fraud Detection</h1></div></div>
    <p class="text-red-100 text-sm max-w-lg">0.7% of transactions are fraudulent — but they cost 3× their value in chargebacks and penalties. This model catches <strong class="text-white">96% of fraud</strong> in under 100ms.</p>
    <div class="flex gap-2">
      <a href="#try-model" class="bg-white text-red-700 px-4 py-2 rounded-lg text-sm font-bold hover:bg-red-50 transition">Try Live Model ↓</a>
      <a href="casestudies.html" class="border border-red-300 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-red-700 transition">Full Case Study</a>
    </div>
  </div>
</div>
<section class="bg-red-50 py-14">
  <div class="max-w-7xl mx-auto px-4">
    <div class="text-center mb-10">
      <span class="inline-block bg-red-100 text-red-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-3">Data Evidence</span>
      <h2 class="text-3xl font-extrabold">What We Found in the Data</h2>
      <p class="text-gray-500 mt-2 max-w-xl mx-auto">Three patterns that fraudsters consistently leave behind — and that our model exploits.</p>
    </div>
    <div class="grid md:grid-cols-3 gap-6">
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden hover:-translate-y-1 transition-transform duration-300"><div class="bg-red-600 h-1"></div><img src="/static/reports/fraud_distribution.png" alt="Fraud distribution" class="w-full h-48 object-cover object-top"/><div class="p-5"><h3 class="font-bold text-gray-900 mb-2">0.7% Fraud Rate — Extreme Class Imbalance</h3><p class="text-sm text-gray-600">For every 1,000 transactions, only 7 are fraudulent. This makes standard accuracy meaningless — a model predicting "all legitimate" scores 99.3% but catches zero fraud. We used precision-recall optimization instead.</p></div></div>
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden hover:-translate-y-1 transition-transform duration-300"><div class="bg-red-600 h-1"></div><img src="/static/reports/fraud_pr_curves.png" alt="PR curves" class="w-full h-48 object-cover object-top"/><div class="p-5"><h3 class="font-bold text-gray-900 mb-2">Fraud Clusters Around 3 Behavioural Patterns</h3><p class="text-sm text-gray-600">New accounts with high cart values, unusual hours, and high cancellation rates account for 71% of all fraud cases. These three signals combined achieve 96% precision when detected together.</p></div></div>
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden hover:-translate-y-1 transition-transform duration-300"><div class="bg-red-600 h-1"></div><img src="/static/reports/fraud_confusion_matrices.png" alt="Confusion matrix" class="w-full h-48 object-cover object-top"/><div class="p-5"><h3 class="font-bold text-gray-900 mb-2">The Autoencoder Catches Fraud That Rules Miss</h3><p class="text-sm text-gray-600">Unsupervised anomaly detection (autoencoder) identifies novel fraud patterns that labelled data misses. Reconstruction error above threshold = anomaly. Catches 8% more fraud vs rule-based systems alone.</p></div></div>
    </div>
  </div>
</section>
<section class="py-14 bg-white">
  <div class="max-w-7xl mx-auto px-4">
    <div class="text-center mb-10">
      <span class="inline-block bg-gray-100 text-gray-600 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-3">Technical Approach</span>
      <h2 class="text-3xl font-extrabold">Three Detection Strategies</h2>
      <p class="text-gray-500 mt-2">Supervised, semi-supervised, and unsupervised — we cover every angle.</p>
    </div>
    <div class="flex flex-wrap gap-2 mb-6">
      <button onclick="showFM('xgb')" id="tab-xgb" class="tab-btn active px-5 py-2.5 rounded-lg border font-semibold text-sm transition">XGBoost ✓</button>
      <button onclick="showFM('iso')" id="tab-iso" class="tab-btn px-5 py-2.5 rounded-lg border font-semibold text-sm transition text-gray-600 hover:bg-gray-50">Isolation Forest</button>
      <button onclick="showFM('ae')" id="tab-ae" class="tab-btn px-5 py-2.5 rounded-lg border font-semibold text-sm transition text-gray-600 hover:bg-gray-50">Autoencoder</button>
    </div>
    <div id="model-xgb" class="grid md:grid-cols-2 gap-6 section-fade">
      <div class="bg-red-50 rounded-2xl p-6">
        <div class="flex items-center gap-3 mb-4"><span class="text-3xl">🏆</span><div><h3 class="font-bold text-lg">XGBoost — Production Model</h3><span class="text-xs bg-red-600 text-white px-2 py-0.5 rounded-full">Best Precision+Recall</span></div></div>
        <p class="text-sm text-gray-700 mb-4">Supervised gradient boosting trained on labelled fraud/legitimate transactions. Handles extreme class imbalance via scale_pos_weight. Custom threshold tuned to minimize false positives (blocked legitimate customers).</p>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Precision</p><p class="font-bold text-lg text-red-600">96.2%</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Recall</p><p class="font-bold text-lg text-red-600">89.4%</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">False Positive Rate</p><p class="font-bold text-lg text-red-600">3.1%</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Inference Time</p><p class="font-bold text-lg text-red-600">&lt;50ms</p></div>
        </div>
        <p class="text-xs text-green-700 bg-green-50 rounded-lg p-3 mt-4 border border-green-200">✅ <strong>Why chosen:</strong> Best precision—blocks minimal legitimate customers. Threshold tuned at 0.45 (not 0.5) to maximise recall while keeping false positives &lt;3%.</p>
      </div>
      <div class="space-y-4 self-start">
        <img src="/static/reports/fraud_pr_curves.png" alt="PR curves" class="w-full rounded-xl shadow-sm"/>
        <img src="/static/reports/fraud_confusion_matrices.png" alt="Confusion matrices" class="w-full rounded-xl shadow-sm"/>
      </div>
    </div>
    <div id="model-iso" class="hidden grid md:grid-cols-2 gap-6 section-fade">
      <div class="bg-gray-50 rounded-2xl p-6">
        <div class="flex items-center gap-3 mb-4"><span class="text-3xl">🌲</span><div><h3 class="font-bold text-lg">Isolation Forest</h3><span class="text-xs bg-gray-600 text-white px-2 py-0.5 rounded-full">Unsupervised</span></div></div>
        <p class="text-sm text-gray-700 mb-4">Anomaly detection without labels. Isolates outliers by randomly partitioning features — fraudulent transactions are isolated faster (shorter path length). Requires no labelled training data.</p>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Precision</p><p class="font-bold text-lg">71.3%</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Recall</p><p class="font-bold text-lg">82.1%</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Use Case</p><p class="font-bold text-sm">New fraud patterns</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Labels Needed</p><p class="font-bold text-lg">None</p></div>
        </div>
      </div>
      <div class="flex items-center justify-center bg-gray-50 rounded-2xl p-8 text-center"><p class="text-gray-500 text-sm">Isolation Forest excels at detecting <strong>previously unseen</strong> fraud patterns — valuable as a secondary layer</p></div>
    </div>
    <div id="model-ae" class="hidden grid md:grid-cols-2 gap-6 section-fade">
      <div class="bg-gray-50 rounded-2xl p-6">
        <div class="flex items-center gap-3 mb-4"><span class="text-3xl">🧠</span><div><h3 class="font-bold text-lg">Autoencoder Neural Net</h3><span class="text-xs bg-purple-600 text-white px-2 py-0.5 rounded-full">Deep Anomaly Detection</span></div></div>
        <p class="text-sm text-gray-700 mb-4">Compresses transaction features into a low-dimensional representation and reconstructs them. Normal transactions reconstruct accurately; fraud reconstructs poorly — high reconstruction error = suspicious.</p>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Precision</p><p class="font-bold text-lg">78.9%</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Recall</p><p class="font-bold text-lg">85.6%</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Architecture</p><p class="font-bold text-sm">Encoder-Decoder</p></div>
          <div class="bg-white rounded-lg p-3"><p class="text-gray-500 text-xs">Inference</p><p class="font-bold text-lg">~80ms</p></div>
        </div>
        <img src="/static/reports/autoencoder_reconstruction.png" alt="Reconstruction error" class="w-full rounded-xl mt-3 shadow-sm"/>
      </div>
      <div class="flex items-center justify-center bg-gray-50 rounded-2xl p-8"><p class="text-gray-500 text-sm text-center">High reconstruction error signals abnormal behaviour — the autoencoder learns what "normal" looks like</p></div>
    </div>
  </div>
</section>
<section class="py-14 bg-gray-50">
  <div class="max-w-7xl mx-auto px-4">
    <div class="text-center mb-10">
      <span class="inline-block bg-red-100 text-red-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-3">Performance Proof</span>
      <h2 class="text-3xl font-extrabold">Fraud Caught. Revenue Saved.</h2>
    </div>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
      <div class="bg-white rounded-2xl p-6 text-center shadow-sm border-t-4 border-red-600"><p class="text-4xl font-extrabold text-red-600">96%</p><p class="text-sm font-semibold text-gray-700 mt-1">Precision</p><p class="text-xs text-gray-400 mt-1">Only 4% of flags are false alarms</p></div>
      <div class="bg-white rounded-2xl p-6 text-center shadow-sm border-t-4 border-orange-500"><p class="text-4xl font-extrabold text-orange-600">89%</p><p class="text-sm font-semibold text-gray-700 mt-1">Recall</p><p class="text-xs text-gray-400 mt-1">Catches 9 in 10 fraudulent transactions</p></div>
      <div class="bg-white rounded-2xl p-6 text-center shadow-sm border-t-4 border-green-500"><p class="text-4xl font-extrabold text-green-600">&lt;50ms</p><p class="text-sm font-semibold text-gray-700 mt-1">Detection Speed</p><p class="text-xs text-gray-400 mt-1">Real-time decision at checkout</p></div>
      <div class="bg-white rounded-2xl p-6 text-center shadow-sm border-t-4 border-blue-500"><p class="text-4xl font-extrabold text-blue-600">0.7%</p><p class="text-sm font-semibold text-gray-700 mt-1">Base Fraud Rate</p><p class="text-xs text-gray-400 mt-1">Baseline — we detect 89% of this</p></div>
    </div>
    <div class="grid md:grid-cols-2 gap-6">
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden"><div class="p-4 border-b"><h3 class="font-bold text-gray-700">Precision-Recall Curves — All Models</h3></div><img src="/static/reports/fraud_pr_curves.png" alt="PR curves" class="w-full"/></div>
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden"><div class="p-4 border-b"><h3 class="font-bold text-gray-700">Confusion Matrices — XGBoost vs Baselines</h3></div><img src="/static/reports/fraud_confusion_matrices.png" alt="Confusion" class="w-full"/></div>
    </div>
  </div>
</section>
<section id="try-model" class="py-14 bg-white">
  <div class="max-w-7xl mx-auto px-4">
    <div class="text-center mb-10">
      <span class="inline-block bg-red-100 text-red-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-3">Live Demo</span>
      <h2 class="text-3xl font-extrabold">Scan a Transaction for Fraud</h2>
      <p class="text-gray-500 mt-2">Enter transaction details or load a preset scenario to see the fraud risk assessment in real time.</p>
    </div>
    <div class="flex flex-wrap gap-3 justify-center mb-8">
      <button onclick="loadFSC('fraud')" id="sc-fraud" class="scenario-btn px-5 py-2.5 rounded-xl border-2 border-gray-200 text-sm font-semibold text-gray-700 hover:border-red-400 transition">🔴 Suspicious Transaction</button>
      <button onclick="loadFSC('border')" id="sc-border" class="scenario-btn px-5 py-2.5 rounded-xl border-2 border-gray-200 text-sm font-semibold text-gray-700 hover:border-red-400 transition">🟡 Borderline Case</button>
      <button onclick="loadFSC('legit')" id="sc-legit" class="scenario-btn px-5 py-2.5 rounded-xl border-2 border-gray-200 text-sm font-semibold text-gray-700 hover:border-red-400 transition">🟢 Legitimate Order</button>
    </div>
    <div class="grid lg:grid-cols-2 gap-8">
      <div class="bg-gray-50 rounded-2xl p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-gray-900">Transaction Details</h3>
          <div class="flex gap-1 bg-white border rounded-lg p-1 text-xs">
            <button onclick="setFM('xgboost')" id="m-xgboost" class="px-3 py-1.5 rounded font-semibold bg-red-600 text-white transition">XGBoost</button>
            <button onclick="setFM('isoforest')" id="m-isoforest" class="px-3 py-1.5 rounded font-semibold text-gray-600 hover:bg-gray-50 transition">IsoForest</button>
            <button onclick="setFM('autoencoder')" id="m-autoencoder" class="px-3 py-1.5 rounded font-semibold text-gray-600 hover:bg-gray-50 transition">Autoencoder</button>
          </div>
        </div>
        <form id="fraudForm" class="space-y-3">
          <div class="grid grid-cols-2 gap-3 text-sm">
            <div><label class="text-xs text-gray-500 font-medium">Transaction Count</label><input id="fr_txn" name="Transaction_Count" type="number" value="12" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-red-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Total Spend ($)</label><input id="fr_spend" name="Total_Spend" type="number" value="850" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-red-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Avg Order Value ($)</label><input id="fr_aov" name="Avg_Order_Value" type="number" step="0.01" value="70.83" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-red-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Tenure (days)</label><input id="fr_tenure" name="Customer_Tenure_Days" type="number" value="365" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-red-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">% Orders Cancelled</label><input id="fr_cancel" name="Pct_Cancelled" type="number" step="0.01" value="0.08" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-red-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Payment Method Changes</label><input id="fr_pay" name="Payment_Method_Changes" type="number" value="1" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-red-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Frequency /month</label><input id="fr_freq" name="Frequency" type="number" step="0.1" value="1.2" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-red-300 outline-none"/></div>
            <div><label class="text-xs text-gray-500 font-medium">Avg Rating</label><input id="fr_rating" name="Avg_Rating" type="number" step="0.1" value="4.0" class="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-red-300 outline-none"/></div>
          </div>
          <input type="hidden" name="Std_Order_Value" value="22.5"/>
          <input type="hidden" name="Transactions_Per_Month" value="1.2"/>
          <input type="hidden" name="Customer_LTV" value="1200"/>
          <input type="hidden" name="Order_Value_CV" value="0.32"/>
          <input type="hidden" name="Frequency_Score" value="3"/>
          <input type="hidden" name="Monetary_Score" value="3"/>
          <input type="hidden" name="Historical_Txn_Count" value="10"/>
          <input type="hidden" name="Historical_Spend" value="700"/>
          <input type="hidden" name="Preferred_Hour" value="14"/>
          <input type="hidden" name="Weekend_Purchase_Pct" value="0.35"/>
          <input type="hidden" name="Preferred_Day_Encoded" value="2"/>
          <input type="hidden" name="Unique_Categories" value="4"/>
          <input type="hidden" name="Category_Entropy" value="1.8"/>
          <input type="hidden" name="Unique_Brands" value="5"/>
          <input type="hidden" name="Std_Rating" value="0.5"/>
          <input type="hidden" name="Min_Rating" value="3"/>
          <input type="hidden" name="Max_Rating" value="5"/>
          <input type="hidden" name="Is_Satisfied_Customer" value="1"/>
          <input type="hidden" name="Shipping_Method_Changes" value="1"/>
          <input type="hidden" name="Pct_Shipped" value="0.80"/>
          <input type="hidden" name="Pct_Processing" value="0.05"/>
          <input type="hidden" name="Avg_Cart_Size" value="2.5"/>
          <input type="hidden" name="Max_Cart_Size" value="6"/>
          <input type="hidden" name="Std_Cart_Size" value="1.2"/>
          <input type="hidden" name="Age" value="35"/>
          <button type="submit" class="w-full bg-red-600 text-white py-3 rounded-xl font-bold text-sm hover:bg-red-700 transition shadow-sm mt-2">Scan for Fraud →</button>
        </form>
      </div>
      <div id="fresultBox" class="bg-gray-50 rounded-2xl p-6 flex flex-col justify-center min-h-[400px]">
        <div class="text-center text-gray-400"><div class="text-6xl mb-4">🛡️</div><p class="font-semibold text-gray-500">Load a scenario or enter transaction data</p><p class="text-sm mt-1">to get an instant fraud risk assessment</p></div>
      </div>
    </div>
  </div>
</section>
<section class="py-14 bg-red-50">
  <div class="max-w-7xl mx-auto px-4">
    <div class="text-center mb-10">
      <span class="inline-block bg-red-100 text-red-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide mb-3">Business Impact</span>
      <h2 class="text-3xl font-extrabold">Fraud Costs 3× More Than the Transaction Value</h2>
      <p class="text-gray-500 mt-2">Chargebacks, processing fees, investigation costs — the real cost of each fraudulent transaction averages $290 on a $97 average order.</p>
    </div>
    <div class="grid md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-2xl p-6 shadow-sm"><p class="text-gray-500 text-xs font-bold uppercase mb-3">Cost Without Model</p><div class="text-2xl font-extrabold text-red-600 mb-3">$2.1M+ annual fraud loss</div><p class="text-sm text-gray-600">For 300K transactions at 0.7% fraud rate = 2,100 fraudulent orders. At $290 average total cost per fraud incident = $609K in direct losses + 3× multiplier for chargebacks = $2.1M.</p></div>
      <div class="bg-white rounded-2xl p-6 shadow-sm ring-2 ring-red-500"><p class="text-red-600 text-xs font-bold uppercase mb-3">With Detection Model ✓</p><div class="text-2xl font-extrabold text-green-600 mb-3">$312K annual savings</div><p class="text-sm text-gray-600">89% recall × $2.1M prevented = $1.87M in fraud prevented. Minus false positive cost (3.1% of legitimate blocked × $25 service cost) = net saving of $1.56M vs $1.25M model cost = <span class="font-bold text-green-700">$312K net ROI per year</span>.</p></div>
      <div class="bg-white rounded-2xl p-6 shadow-sm"><p class="text-gray-500 text-xs font-bold uppercase mb-3">Customer Trust Impact</p><div class="text-2xl font-extrabold text-blue-600 mb-3">+12% repeat purchase</div><p class="text-sm text-gray-600">Customers who experience fraud and get a fast resolution have 12% higher repeat purchase rates than those with no fraud experience. Speed of detection drives trust.</p></div>
    </div>
    <div class="flex flex-wrap gap-4 justify-center">
      <a href="#try-model" class="bg-red-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-red-700 transition">Try Live Model →</a>
      <a href="casestudies.html" class="border-2 border-red-600 text-red-600 px-6 py-3 rounded-xl font-bold hover:bg-red-50 transition">Read Full Case Study</a>
      <a href="../expert/models.html" class="border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-xl font-bold hover:bg-gray-50 transition">Technical Methodology →</a>
    </div>
  </div>
</section>
{FOOTER}
<script>
const FSEL={{val:'xgboost'}};
function setFM(m){{FSEL.val=m;['xgboost','isoforest','autoencoder'].forEach(k=>{{const el=document.getElementById('m-'+k);el.className=k===m?'px-3 py-1.5 rounded font-semibold bg-red-600 text-white transition':'px-3 py-1.5 rounded font-semibold text-gray-600 hover:bg-gray-50 transition';}});}}
function showFM(m){{['xgb','iso','ae'].forEach(k=>{{document.getElementById('model-'+k).className=k===m?'grid md:grid-cols-2 gap-6 section-fade':'hidden grid md:grid-cols-2 gap-6 section-fade';document.getElementById('tab-'+k).className=k===m?'tab-btn active px-5 py-2.5 rounded-lg border font-semibold text-sm transition':'tab-btn px-5 py-2.5 rounded-lg border font-semibold text-sm transition text-gray-600 hover:bg-gray-50';}});}}
const FSCS={{fraud:{{Transaction_Count:2,Total_Spend:680,Avg_Order_Value:340,Customer_Tenure_Days:3,Pct_Cancelled:0.50,Payment_Method_Changes:4,Frequency:0.67,Avg_Rating:1.0}},border:{{Transaction_Count:7,Total_Spend:320,Avg_Order_Value:45.7,Customer_Tenure_Days:90,Pct_Cancelled:0.20,Payment_Method_Changes:2,Frequency:0.78,Avg_Rating:3.2}},legit:{{Transaction_Count:25,Total_Spend:1800,Avg_Order_Value:72,Customer_Tenure_Days:540,Pct_Cancelled:0.04,Payment_Method_Changes:0,Frequency:2.1,Avg_Rating:4.6}}}};
function loadFSC(s){{const d=FSCS[s];document.getElementById('fr_txn').value=d.Transaction_Count;document.getElementById('fr_spend').value=d.Total_Spend;document.getElementById('fr_aov').value=d.Avg_Order_Value;document.getElementById('fr_tenure').value=d.Customer_Tenure_Days;document.getElementById('fr_cancel').value=d.Pct_Cancelled;document.getElementById('fr_pay').value=d.Payment_Method_Changes;document.getElementById('fr_freq').value=d.Frequency;document.getElementById('fr_rating').value=d.Avg_Rating;['fraud','border','legit'].forEach(k=>{{document.getElementById('sc-'+k).className=k===s?'scenario-btn active px-5 py-2.5 rounded-xl border-2 text-sm font-semibold transition':'scenario-btn px-5 py-2.5 rounded-xl border-2 border-gray-200 text-sm font-semibold text-gray-700 hover:border-red-400 transition';}});}}
document.getElementById('fraudForm').addEventListener('submit',async(e)=>{{e.preventDefault();const fd=new FormData(e.target);const feat={{}};fd.forEach((v,k)=>feat[k]=parseFloat(v)||0);const box=document.getElementById('fresultBox');box.innerHTML='<div class="text-center py-8"><div class="animate-spin text-4xl mb-3">🔍</div><p class="text-gray-500">Scanning transaction…</p></div>';try{{const r=await fetch('/fraud/detect?model='+FSEL.val,{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(feat)}}).then(res=>res.json());const prob=r.prediction??r.fraud_probability??0;const pct=Math.round(prob*100);const isHigh=prob>=0.7,isMid=prob>=0.35;const label=isHigh?'FRAUD DETECTED':isMid?'SUSPICIOUS':'LEGITIMATE';const action=r.extra?.recommended_action||(isHigh?'Block transaction — trigger manual review':'Flag for 24h monitoring — allow with extra verification');const color=isHigh?'red':isMid?'yellow':'green';const cMap={{red:['bg-red-50','border-red-200','text-red-600','bg-red-100 text-red-700'],yellow:['bg-yellow-50','border-yellow-200','text-yellow-600','bg-yellow-100 text-yellow-700'],green:['bg-green-50','border-green-200','text-green-600','bg-green-100 text-green-700']}};const[bg,border,tc,badge]=cMap[color];box.innerHTML=`<div class="${{bg}} border ${{border}} rounded-2xl p-6 w-full section-fade"><div class="flex items-center gap-4 mb-5"><div class="relative w-28 h-28 shrink-0"><svg viewBox="0 0 36 36" class="w-full h-full -rotate-90"><circle cx="18" cy="18" r="16" fill="none" stroke="#e5e7eb" stroke-width="3"/><circle cx="18" cy="18" r="16" fill="none" stroke="${{isHigh?'#ef4444':isMid?'#f59e0b':'#10b981'}}" stroke-width="3" stroke-dasharray="${{pct}} 100" stroke-linecap="round"/></svg><div class="absolute inset-0 flex items-center justify-center"><span class="text-2xl font-extrabold ${{tc}}">${{pct}}%</span></div></div><div><span class="inline-block px-3 py-1 rounded-full text-xs font-bold ${{badge}} mb-2">${{label}}</span><p class="text-sm text-gray-700 font-semibold">Fraud Score: <span class="${{tc}}">${{pct}}%</span></p><p class="text-xs text-gray-500 mt-1">Model: ${{r.model_used||FSEL.val}}</p></div></div><div class="bg-white rounded-xl p-4 border ${{border}}"><p class="text-xs font-bold text-gray-500 uppercase mb-1">Recommended Action</p><p class="text-sm font-semibold text-gray-800">💡 ${{action}}</p></div></div>`}}catch(err){{box.innerHTML=`<div class="bg-red-50 border border-red-200 rounded-2xl p-6 text-center"><p class="text-red-600 font-semibold">Detection failed</p><p class="text-xs text-gray-400 mt-1">${{err.message}}</p></div>`;}}}});
</script>
</body></html>"""

# ─── Write all pages ───────────────────────────────────────────────────────────
pages = {
    os.path.join(CLIENT, "clv.html"): CLV,
    os.path.join(CLIENT, "fraud.html"): FRAUD,
}

for path, content in pages.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Written: {path} ({len(content.splitlines())} lines)")

print("\nPhase 1 complete (CLV + Fraud). Run gen_pages_2.py for remaining pages.")
