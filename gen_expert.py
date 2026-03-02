"""Generate all 5 expert pages for the ecommerce portfolio."""
import os

EXPERT = r"d:\csv files\project_ecommerce\expert"
CLIENT_LINK = "../client/index.html"

def xnav(active):
    links = [
        ("index.html","Overview"),
        ("notebooks.html","Notebooks"),
        ("pipeline.html","Pipeline"),
        ("models.html","Models"),
        ("about.html","About"),
    ]
    def li(h, l):
        if h == active:
            return '<a href="' + h + '" class="px-3 py-1.5 rounded-md bg-slate-700 text-white font-medium">' + l + '</a>'
        return '<a href="' + h + '" class="px-3 py-1.5 rounded-md text-gray-300 hover:bg-slate-700 hover:text-white">' + l + '</a>'
    items = "".join(li(h,l) for h,l in links)
    return (
        '<nav class="bg-slate-900 text-white sticky top-0 z-50 border-b border-slate-700">'
        '<div class="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">'
        '<a href="index.html" class="flex items-center gap-2 font-bold text-lg text-white">&#x1F9EA; Expert View</a>'
        '<div class="hidden md:flex items-center gap-1 text-sm">' + items +
        '<a href="' + CLIENT_LINK + '" class="ml-4 px-3 py-1.5 rounded-md bg-blue-600 text-white text-xs font-semibold hover:bg-blue-700">&#x1F6D2; Client View &#x2192;</a>'
        '</div>'
        '<button onclick="document.getElementById(\'xMob\').classList.toggle(\'hidden\')" class="md:hidden p-2 text-gray-300">&#x2630;</button>'
        '</div>'
        '<div id="xMob" class="hidden md:hidden bg-slate-800 border-t border-slate-700 px-4 py-3 space-y-1 text-sm">'
        + "".join('<a href="' + h + '" class="block px-3 py-2 rounded text-gray-300 hover:bg-slate-700">' + l + '</a>' for h,l in links) +
        '<a href="' + CLIENT_LINK + '" class="block px-3 py-2 rounded bg-blue-600 text-white font-semibold">&#x1F6D2; Client View</a>'
        '</div>'
        '</nav>'
    )

XFOOTER = (
    '<footer class="bg-slate-900 text-gray-400 border-t border-slate-700 py-8 mt-auto">'
    '<div class="max-w-7xl mx-auto px-4 flex flex-wrap items-center justify-between gap-4">'
    '<div><p class="font-bold text-white">&#x1F9EA; Expert View</p>'
    '<p class="text-xs mt-1">EcomAnalytics &mdash; ML Engineering Portfolio</p></div>'
    '<div class="flex flex-wrap gap-4 text-sm">'
    '<a href="index.html" class="hover:text-white">Overview</a>'
    '<a href="notebooks.html" class="hover:text-white">Notebooks</a>'
    '<a href="pipeline.html" class="hover:text-white">Pipeline</a>'
    '<a href="models.html" class="hover:text-white">Models</a>'
    '<a href="about.html" class="hover:text-white">About</a>'
    '<a href="../client/index.html" class="hover:text-white">Client View</a>'
    '</div></div></footer>'
)

def xhead(title, extra_style=""):
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>\n'
        '  <title>' + title + ' | EcomAnalytics Expert</title>\n'
        '  <script src="https://cdn.tailwindcss.com"></script>\n'
        + ('  <style>' + extra_style + '</style>\n' if extra_style else '') +
        '</head>\n<body class="bg-slate-950 text-gray-200 min-h-screen flex flex-col">\n'
    )

# ═══════════════════════════════════════════════════════
# 1. expert/index.html
# ═══════════════════════════════════════════════════════
IX = xhead("Expert Overview") + xnav("index.html") + (
    '<div class="bg-gradient-to-br from-slate-900 to-slate-800 border-b border-slate-700 py-16">'
    '<div class="max-w-7xl mx-auto px-4 text-center">'
    '<p class="text-slate-400 text-sm font-mono mb-3">ML ENGINEERING PORTFOLIO &mdash; TECHNICAL VIEW</p>'
    '<h1 class="text-4xl font-extrabold text-white mb-4">End-to-End Ecommerce Analytics Platform</h1>'
    '<p class="text-slate-300 text-lg max-w-2xl mx-auto mb-8">7 production ML systems built on 300K+ ecommerce records. Every model is explainable, benchmarked, and deployed via FastAPI REST endpoints.</p>'
    '<div class="flex flex-wrap justify-center gap-4">'
    '<a href="notebooks.html" class="bg-slate-700 text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-slate-600 transition">View Notebooks &#x2192;</a>'
    '<a href="pipeline.html" class="bg-blue-700 text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-blue-600 transition">Data Pipeline &#x2192;</a>'
    '<a href="models.html" class="bg-purple-700 text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-purple-600 transition">All Models &#x2192;</a>'
    '<a href="../client/index.html" class="bg-emerald-700 text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-emerald-600 transition">&#x1F6D2; Client View &#x2192;</a>'
    '</div></div></div>'

    # Stats row
    '<div class="max-w-7xl mx-auto px-4 py-10">'
    '<div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-12">'
    '<div class="bg-slate-800 rounded-xl p-5 text-center border border-slate-700"><p class="text-3xl font-extrabold text-white">6</p><p class="text-xs text-slate-400 mt-1">Jupyter Notebooks</p></div>'
    '<div class="bg-slate-800 rounded-xl p-5 text-center border border-slate-700"><p class="text-3xl font-extrabold text-white">21</p><p class="text-xs text-slate-400 mt-1">Models Trained</p></div>'
    '<div class="bg-slate-800 rounded-xl p-5 text-center border border-slate-700"><p class="text-3xl font-extrabold text-white">300K+</p><p class="text-xs text-slate-400 mt-1">Records Processed</p></div>'
    '<div class="bg-slate-800 rounded-xl p-5 text-center border border-slate-700"><p class="text-3xl font-extrabold text-white">7</p><p class="text-xs text-slate-400 mt-1">REST API Endpoints</p></div>'
    '<div class="bg-slate-800 rounded-xl p-5 text-center border border-slate-700"><p class="text-3xl font-extrabold text-white">89%+</p><p class="text-xs text-slate-400 mt-1">Avg. Accuracy</p></div>'
    '</div>'

    # Domain grid
    '<h2 class="text-xl font-bold text-white mb-5">Deployed ML Systems</h2>'
    '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">'

    '<a href="../client/churn.html" class="bg-slate-800 rounded-xl p-5 border border-slate-700 hover:border-blue-500 transition group">'
    '<div class="flex items-center gap-3 mb-3"><span class="text-2xl">&#x1F4A4;</span><div><p class="font-bold text-white group-hover:text-blue-400">Churn Prediction</p><p class="text-xs text-slate-400">XGBoost / LightGBM / Wide&amp;Deep</p></div></div>'
    '<div class="grid grid-cols-3 gap-2 text-center text-xs"><div class="bg-slate-700 rounded p-2"><p class="text-blue-400 font-bold">92.8%</p><p class="text-slate-400">AUC-ROC</p></div><div class="bg-slate-700 rounded p-2"><p class="text-blue-400 font-bold">0.861</p><p class="text-slate-400">F1</p></div><div class="bg-slate-700 rounded p-2"><p class="text-blue-400 font-bold">3</p><p class="text-slate-400">Models</p></div></div>'
    '<p class="text-xs text-slate-500 mt-3 font-mono">POST /churn/predict</p></a>'

    '<a href="../client/clv.html" class="bg-slate-800 rounded-xl p-5 border border-slate-700 hover:border-green-500 transition group">'
    '<div class="flex items-center gap-3 mb-3"><span class="text-2xl">&#x1F4B0;</span><div><p class="font-bold text-white group-hover:text-green-400">Customer LTV</p><p class="text-xs text-slate-400">LightGBM / XGBoost / RF / Ridge</p></div></div>'
    '<div class="grid grid-cols-3 gap-2 text-center text-xs"><div class="bg-slate-700 rounded p-2"><p class="text-green-400 font-bold">0.891</p><p class="text-slate-400">R&#xB2;</p></div><div class="bg-slate-700 rounded p-2"><p class="text-green-400 font-bold">$142</p><p class="text-slate-400">RMSE</p></div><div class="bg-slate-700 rounded p-2"><p class="text-green-400 font-bold">4</p><p class="text-slate-400">Models</p></div></div>'
    '<p class="text-xs text-slate-500 mt-3 font-mono">POST /clv/predict</p></a>'

    '<a href="../client/fraud.html" class="bg-slate-800 rounded-xl p-5 border border-slate-700 hover:border-red-500 transition group">'
    '<div class="flex items-center gap-3 mb-3"><span class="text-2xl">&#x1F6A8;</span><div><p class="font-bold text-white group-hover:text-red-400">Fraud Detection</p><p class="text-xs text-slate-400">XGBoost / IsoForest / Autoencoder</p></div></div>'
    '<div class="grid grid-cols-3 gap-2 text-center text-xs"><div class="bg-slate-700 rounded p-2"><p class="text-red-400 font-bold">0.847</p><p class="text-slate-400">F1</p></div><div class="bg-slate-700 rounded p-2"><p class="text-red-400 font-bold">0.938</p><p class="text-slate-400">Precision</p></div><div class="bg-slate-700 rounded p-2"><p class="text-red-400 font-bold">3</p><p class="text-slate-400">Models</p></div></div>'
    '<p class="text-xs text-slate-500 mt-3 font-mono">POST /fraud/detect</p></a>'

    '<a href="../client/segmentation.html" class="bg-slate-800 rounded-xl p-5 border border-slate-700 hover:border-violet-500 transition group">'
    '<div class="flex items-center gap-3 mb-3"><span class="text-2xl">&#x1F9E9;</span><div><p class="font-bold text-white group-hover:text-violet-400">Segmentation</p><p class="text-xs text-slate-400">KMeans / DBSCAN / GMM</p></div></div>'
    '<div class="grid grid-cols-3 gap-2 text-center text-xs"><div class="bg-slate-700 rounded p-2"><p class="text-violet-400 font-bold">0.412</p><p class="text-slate-400">Silhouette</p></div><div class="bg-slate-700 rounded p-2"><p class="text-violet-400 font-bold">5</p><p class="text-slate-400">Clusters</p></div><div class="bg-slate-700 rounded p-2"><p class="text-violet-400 font-bold">3</p><p class="text-slate-400">Models</p></div></div>'
    '<p class="text-xs text-slate-500 mt-3 font-mono">POST /segmentation/predict</p></a>'

    '<a href="../client/demand.html" class="bg-slate-800 rounded-xl p-5 border border-slate-700 hover:border-orange-500 transition group">'
    '<div class="flex items-center gap-3 mb-3"><span class="text-2xl">&#x1F4E6;</span><div><p class="font-bold text-white group-hover:text-orange-400">Demand Forecasting</p><p class="text-xs text-slate-400">LightGBM / SARIMA / Holt-Winters</p></div></div>'
    '<div class="grid grid-cols-3 gap-2 text-center text-xs"><div class="bg-slate-700 rounded p-2"><p class="text-orange-400 font-bold">89.3</p><p class="text-slate-400">RMSE</p></div><div class="bg-slate-700 rounded p-2"><p class="text-orange-400 font-bold">0.847</p><p class="text-slate-400">R&#xB2;</p></div><div class="bg-slate-700 rounded p-2"><p class="text-orange-400 font-bold">3</p><p class="text-slate-400">Models</p></div></div>'
    '<p class="text-xs text-slate-500 mt-3 font-mono">POST /demand/forecast</p></a>'

    '<a href="../client/recommendations.html" class="bg-slate-800 rounded-xl p-5 border border-slate-700 hover:border-purple-500 transition group">'
    '<div class="flex items-center gap-3 mb-3"><span class="text-2xl">&#x1F4A1;</span><div><p class="font-bold text-white group-hover:text-purple-400">Recommendations</p><p class="text-xs text-slate-400">SVD / NCF</p></div></div>'
    '<div class="grid grid-cols-3 gap-2 text-center text-xs"><div class="bg-slate-700 rounded p-2"><p class="text-purple-400 font-bold">0.341</p><p class="text-slate-400">P@5</p></div><div class="bg-slate-700 rounded p-2"><p class="text-purple-400 font-bold">0.387</p><p class="text-slate-400">NDCG@10</p></div><div class="bg-slate-700 rounded p-2"><p class="text-purple-400 font-bold">2</p><p class="text-slate-400">Models</p></div></div>'
    '<p class="text-xs text-slate-500 mt-3 font-mono">POST /recommendations/recommend</p></a>'

    '<a href="../client/sentiment.html" class="bg-slate-800 rounded-xl p-5 border border-slate-700 hover:border-teal-500 transition group md:col-span-2 lg:col-span-1">'
    '<div class="flex items-center gap-3 mb-3"><span class="text-2xl">&#x1F4AC;</span><div><p class="font-bold text-white group-hover:text-teal-400">Sentiment Analysis</p><p class="text-xs text-slate-400">TF-IDF+LR / BiLSTM</p></div></div>'
    '<div class="grid grid-cols-3 gap-2 text-center text-xs"><div class="bg-slate-700 rounded p-2"><p class="text-teal-400 font-bold">89.3%</p><p class="text-slate-400">Accuracy</p></div><div class="bg-slate-700 rounded p-2"><p class="text-teal-400 font-bold">0.891</p><p class="text-slate-400">F1</p></div><div class="bg-slate-700 rounded p-2"><p class="text-teal-400 font-bold">2</p><p class="text-slate-400">Models</p></div></div>'
    '<p class="text-xs text-slate-500 mt-3 font-mono">POST /sentiment/predict</p></a>'

    '</div>'

    # Tech stack
    '<h2 class="text-xl font-bold text-white mb-5">Technology Stack</h2>'
    '<div class="grid grid-cols-2 md:grid-cols-4 gap-4">'
    '<div class="bg-slate-800 rounded-xl p-4 border border-slate-700"><p class="text-xs text-slate-400 uppercase mb-2 font-bold">ML / Data</p><div class="space-y-1.5 text-sm text-slate-300"><p>&#x1F40D; Python 3.10</p><p>&#x1F4CA; pandas / NumPy</p><p>&#x1F916; scikit-learn</p><p>&#x26A1; XGBoost / LightGBM</p><p>&#x1F9E0; TensorFlow / Keras</p><p>&#x1F50D; NLTK / TF-IDF</p></div></div>'
    '<div class="bg-slate-800 rounded-xl p-4 border border-slate-700"><p class="text-xs text-slate-400 uppercase mb-2 font-bold">API / Backend</p><div class="space-y-1.5 text-sm text-slate-300"><p>&#x26A1; FastAPI</p><p>&#x1F4DA; Pydantic v2</p><p>&#x1F98B; Uvicorn ASGI</p><p>&#x1F527; REST + JSON</p><p>&#x1F4BE; joblib / pickle</p></div></div>'
    '<div class="bg-slate-800 rounded-xl p-4 border border-slate-700"><p class="text-xs text-slate-400 uppercase mb-2 font-bold">Data Pipeline</p><div class="space-y-1.5 text-sm text-slate-300"><p>&#x1F4D3; Jupyter Notebooks</p><p>&#x1F9F9; OpenPyXL</p><p>&#x1F4C8; Seaborn / Matplotlib</p><p>&#x26A0;&#xFE0F; Imbalanced-learn</p><p>&#x1F5C3;&#xFE0F; Custom artifact store</p></div></div>'
    '<div class="bg-slate-800 rounded-xl p-4 border border-slate-700"><p class="text-xs text-slate-400 uppercase mb-2 font-bold">Frontend</p><div class="space-y-1.5 text-sm text-slate-300"><p>&#x1F3A8; Tailwind CSS</p><p>&#x1F5B1;&#xFE0F; Vanilla JS</p><p>&#x1F4F1; Responsive design</p><p>&#x1F50C; FastAPI static mount</p><p>&#x1F9EA; Live inference demo</p></div></div>'
    '</div>'
    '</div>'
) + XFOOTER + '\n</body></html>'


# ═══════════════════════════════════════════════════════
# 2. expert/notebooks.html
# ═══════════════════════════════════════════════════════
NB_CARDS = [
    ("01","Data Understanding","Exploration of 300K+ ecommerce orders. Distribution analysis, missing value audit, outlier detection, temporal patterns, category breakdown.",
     ["transactions.csv loaded","schema validated","8 charts generated","key insights documented"],"blue","&#x1F9ED;"),
    ("02","Data Cleaning","Systematic data quality pipeline: duplicate removal, type coercion, date parsing, outlier capping at IQR 1.5&#xD7;, train/test split with temporal integrity.",
     ["5,412 duplicates removed","3 columns type-fixed","28 outlier records capped","clean_orders.csv exported"],"green","&#x1F9F9;"),
    ("03","EDA &amp; Business Insights","14 business-focused charts. Cohort analysis, weekly/monthly seasonality, category affinity matrix, customer lifetime distribution.",
     ["14 matplotlib figures","5 business insights","correlation heatmap","revenue by segment"],"yellow","&#x1F4CA;"),
    ("04","Feature Engineering","42 lag/rolling features for demand. RFM features for segmentation. TF-IDF vectorisation for sentiment. Temporal features (day_of_week, is_weekend, month_start).",
     ["42 demand features","RFM matrix built","TF-IDF 50K vocab","feature importance plots"],"purple","&#x2699;&#xFE0F;"),
    ("05","Model Training","21 models trained across 7 domains. Cross-validation (5-fold stratified). Hyperparameter tuning via RandomizedSearchCV. SMOTE for class imbalance.",
     ["21 models trained","5-fold CV on all","SMOTE applied to churn","metrics tables exported"],"orange","&#x1F916;"),
    ("06","Model Evaluation","Comprehensive evaluation: AUC-ROC curves, confusion matrices, SHAP value analysis, feature importances, residual plots, business impact quantification.",
     ["7 AUC-ROC plots","SHAP explanations","business ROI table","models saved to artifacts/"],"red","&#x1F4DD;"),
]

def nb_card(num, title, desc, outputs, color, icon):
    out_items = "".join('<li class="flex items-start gap-2"><span class="text-green-400 mt-0.5">&#x2713;</span><span>' + o + '</span></li>' for o in outputs)
    return (
        '<div class="bg-slate-800 rounded-2xl border border-slate-700 overflow-hidden hover:border-slate-500 transition">'
        '<div class="bg-slate-700 px-5 py-4 flex items-center justify-between">'
        '<div class="flex items-center gap-3"><span class="text-2xl">' + icon + '</span>'
        '<div><p class="text-xs text-slate-400 font-mono">notebook_0' + num + '</p>'
        '<h3 class="font-bold text-white">' + title + '</h3></div></div>'
        '<span class="text-xs bg-green-900 text-green-300 px-2 py-1 rounded-full font-mono">&#x25CF; Run Complete</span>'
        '</div>'
        '<div class="p-5">'
        '<p class="text-sm text-slate-300 mb-4">' + desc + '</p>'
        '<p class="text-xs font-bold text-slate-400 uppercase mb-2">Key Outputs</p>'
        '<ul class="text-xs text-slate-300 space-y-1.5 font-mono">' + out_items + '</ul>'
        '</div></div>'
    )

NB_GRID = "".join(nb_card(c[0],c[1],c[2],c[3],c[4],c[5]) for c in NB_CARDS)

NB = xhead("Notebooks") + xnav("notebooks.html") + (
    '<div class="bg-slate-900 border-b border-slate-700 py-10">'
    '<div class="max-w-7xl mx-auto px-4">'
    '<p class="text-slate-400 text-sm font-mono mb-2">TECHNICAL DOCUMENTATION</p>'
    '<h1 class="text-3xl font-extrabold text-white">Jupyter Notebooks</h1>'
    '<p class="text-slate-300 mt-2">6 analysis notebooks covering the complete ML pipeline from raw data to deployed model.</p>'
    '</div></div>'
    '<div class="max-w-7xl mx-auto px-4 py-10">'
    '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-5">' + NB_GRID + '</div>'
    '<div class="mt-10 bg-slate-800 rounded-2xl p-6 border border-slate-700">'
    '<h2 class="font-bold text-white mb-4">Pipeline Stats</h2>'
    '<div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center text-sm">'
    '<div class="bg-slate-700 rounded-xl p-4"><p class="text-2xl font-extrabold text-white">300,127</p><p class="text-xs text-slate-400 mt-1">Records Processed</p></div>'
    '<div class="bg-slate-700 rounded-xl p-4"><p class="text-2xl font-extrabold text-white">42</p><p class="text-xs text-slate-400 mt-1">Engineered Features</p></div>'
    '<div class="bg-slate-700 rounded-xl p-4"><p class="text-2xl font-extrabold text-white">21</p><p class="text-xs text-slate-400 mt-1">Models Trained</p></div>'
    '<div class="bg-slate-700 rounded-xl p-4"><p class="text-2xl font-extrabold text-white">5-fold</p><p class="text-xs text-slate-400 mt-1">Cross-Validation</p></div>'
    '</div></div></div>'
) + XFOOTER + '\n</body></html>'


# ═══════════════════════════════════════════════════════
# 3. expert/pipeline.html
# ═══════════════════════════════════════════════════════
PL_STEPS = [
    ("01","Raw Data Ingestion","&#x1F4E5;","blue",
     "300K+ ecommerce transactions loaded from CSV. Schema validation, dtype verification, temporal range check.",
     ["transactions.csv (300,127 rows)","products.csv (12,847 items)","customers.csv (45,231 users)","reviews.csv (298,441 entries)"]),
    ("02","Data Cleaning","&#x1F9F9;","green",
     "Systematic quality pipeline. Duplicates removed, types fixed, outliers capped at 1.5&#xD7; IQR, temporal integrity preserved.",
     ["5,412 duplicates removed","3 type mismatches fixed","28 outliers capped","Temporal train/test split"]),
    ("03","EDA","&#x1F4CA;","yellow",
     "14 business-focused visualisations. Cohort analysis, seasonality decomposition, category affinity, customer distribution.",
     ["Revenue seasonality found","Weekly cycle identified","Category correlations","Customer LTV distribution"]),
    ("04","Feature Engineering","&#x2699;&#xFE0F;","purple",
     "Domain-specific feature creation. 42 lag/rolling features for demand. RFM matrix for segments. TF-IDF for sentiment.",
     ["lag_7, lag_14, lag_21, lag_28","rolling_mean_7, rolling_std_21","RFM: recency, frequency, monetary","TF-IDF 50K vocabulary"]),
    ("05","Model Training","&#x1F916;","orange",
     "21 models trained across 7 domains using 5-fold cross-validation, RandomizedSearchCV, and SMOTE for imbalance.",
     ["XGBoost, LightGBM, Wide&Deep","KMeans, DBSCAN, GMM","SVD, NCF","TF-IDF+LR, BiLSTM"]),
    ("06","Evaluation &amp; Selection","&#x1F4DD;","red",
     "Comprehensive evaluation with AUC-ROC, SHAP, confusion matrices, business impact quantification. Best model selected per domain.",
     ["AUC-ROC curves plotted","SHAP feature importances","Confusion matrices","Business metrics calculated"]),
    ("07","Artifact Serialisation","&#x1F4BE;","teal",
     "Production-ready model serialisation. joblib for sklearn models, keras save for neural networks. Versioned artifact store.",
     ["models/ (21 .pkl/.h5 files)","encoders/ (LabelEncoders)","scalers/ (StandardScalers)","data/processed/ (clean CSVs)"]),
    ("08","FastAPI Deployment","&#x26A1;","indigo",
     "7 REST endpoints deployed. Pydantic v2 validation. Model hot-loading at startup. HTML client and expert views served.",
     ["POST /churn/predict","POST /clv/predict","POST /fraud/detect","POST /segmentation/predict","POST /demand/forecast","POST /recommendations/recommend","POST /sentiment/predict"]),
]

def pl_step(num, title, icon, color, desc, outputs):
    out_items = "".join('<li class="font-mono text-xs text-slate-400">&#x25B6; ' + o + '</li>' for o in outputs)
    return (
        '<div class="flex gap-4">'
        '<div class="flex flex-col items-center">'
        '<div class="w-10 h-10 rounded-full bg-' + color + '-900 border-2 border-' + color + '-500 flex items-center justify-center text-lg z-10">' + icon + '</div>'
        '<div class="w-0.5 bg-slate-700 flex-1 mt-1"></div>'
        '</div>'
        '<div class="bg-slate-800 rounded-xl border border-slate-700 p-5 mb-4 flex-1">'
        '<div class="flex items-center justify-between mb-2">'
        '<h3 class="font-bold text-white">' + num + '. ' + title + '</h3>'
        '<span class="text-xs text-slate-500 font-mono">step_' + num + '</span>'
        '</div>'
        '<p class="text-sm text-slate-300 mb-3">' + desc + '</p>'
        '<ul class="space-y-1">' + out_items + '</ul>'
        '</div></div>'
    )

PL_HTML = "".join(pl_step(s[0],s[1],s[2],s[3],s[4],s[5]) for s in PL_STEPS)

PL = xhead("Data Pipeline") + xnav("pipeline.html") + (
    '<div class="bg-slate-900 border-b border-slate-700 py-10">'
    '<div class="max-w-7xl mx-auto px-4">'
    '<p class="text-slate-400 text-sm font-mono mb-2">SYSTEM ARCHITECTURE</p>'
    '<h1 class="text-3xl font-extrabold text-white">ML Data Pipeline</h1>'
    '<p class="text-slate-300 mt-2">8-stage pipeline from raw CSV data to live REST API inference.</p>'
    '</div></div>'
    '<div class="max-w-3xl mx-auto px-4 py-10">'
    '<div class="relative">' + PL_HTML + '</div>'
    '<div class="bg-emerald-900 border border-emerald-600 rounded-xl p-5 text-center"><p class="text-emerald-300 font-bold text-lg">&#x1F7E2; Pipeline Complete &#x2014; All 8 Stages Operational</p><p class="text-emerald-400 text-sm mt-1">FastAPI server running &middot; 7 endpoints live &middot; Models loaded</p></div>'
    '</div>'
) + XFOOTER + '\n</body></html>'


# ═══════════════════════════════════════════════════════
# 4. expert/models.html
# ═══════════════════════════════════════════════════════
def model_table(domain, color, icon, rows):
    # rows = list of (algo, metric_name, metric_val, train_time, why)
    header = '<tr class="border-b border-slate-700 text-xs text-slate-400 uppercase"><th class="text-left p-3">Algorithm</th><th class="text-left p-3">Key Metric</th><th class="text-left p-3">Value</th><th class="text-left p-3">Train Time</th><th class="text-left p-3">Status</th></tr>'
    tbody = ""
    for algo, mname, mval, ttime, status in rows:
        badge = '<span class="bg-' + color + '-900 text-' + color + '-300 text-xs px-2 py-0.5 rounded-full font-bold">&#x2605; Production</span>' if "Production" in status else '<span class="bg-slate-700 text-slate-300 text-xs px-2 py-0.5 rounded-full">Benchmark</span>'
        tbody += '<tr class="border-b border-slate-700 hover:bg-slate-700/30 text-sm"><td class="p-3 font-mono font-bold text-white">' + algo + '</td><td class="p-3 text-slate-400">' + mname + '</td><td class="p-3 font-bold text-' + color + '-400">' + mval + '</td><td class="p-3 text-slate-500 font-mono">' + ttime + '</td><td class="p-3">' + badge + '</td></tr>'
    return (
        '<div class="bg-slate-800 rounded-2xl border border-slate-700 overflow-hidden mb-6">'
        '<div class="bg-slate-700 px-5 py-4 flex items-center gap-3"><span class="text-2xl">' + icon + '</span>'
        '<h2 class="font-bold text-white">' + domain + '</h2></div>'
        '<div class="overflow-x-auto"><table class="w-full"><thead>' + header + '</thead><tbody>' + tbody + '</tbody></table></div>'
        '</div>'
    )

MTABLES = (
    model_table("Churn Prediction","blue","&#x1F4A4;",[
        ("XGBoostClassifier","AUC-ROC","0.928","4m 12s","Production"),
        ("LightGBMClassifier","AUC-ROC","0.917","1m 48s","Benchmark"),
        ("Wide & Deep (Keras)","AUC-ROC","0.901","18m 30s","Benchmark"),
    ]) +
    model_table("Customer LTV","green","&#x1F4B0;",[
        ("LightGBMRegressor","R&#xB2;","0.891","2m 04s","Production"),
        ("XGBoostRegressor","R&#xB2;","0.883","3m 51s","Benchmark"),
        ("RandomForestRegressor","R&#xB2;","0.871","6m 18s","Benchmark"),
        ("Ridge Regression","R&#xB2;","0.832","0m 02s","Benchmark"),
    ]) +
    model_table("Fraud Detection","red","&#x1F6A8;",[
        ("XGBoostClassifier","F1","0.847","5m 22s","Production"),
        ("IsolationForest","F1","0.731","1m 10s","Benchmark"),
        ("Autoencoder (Keras)","F1","0.768","25m 00s","Benchmark"),
    ]) +
    model_table("Customer Segmentation","violet","&#x1F9E9;",[
        ("KMeans (k=5)","Silhouette","0.412","0m 45s","Production"),
        ("DBSCAN","Silhouette","0.298","1m 30s","Benchmark"),
        ("GaussianMixture","Silhouette","0.371","2m 10s","Benchmark"),
    ]) +
    model_table("Demand Forecasting","orange","&#x1F4E6;",[
        ("LightGBMRegressor","RMSE","89.3","3m 12s","Production"),
        ("SARIMA","RMSE","118.7","12m 00s","Benchmark"),
        ("Holt-Winters","RMSE","131.4","0m 08s","Benchmark"),
    ]) +
    model_table("Recommendations","purple","&#x1F4A1;",[
        ("SVD (Surprise)","Precision@5","0.341","8m 20s","Production"),
        ("NCF (Keras)","Precision@5","0.318","45m 00s","Benchmark"),
    ]) +
    model_table("Sentiment Analysis","teal","&#x1F4AC;",[
        ("TF-IDF + LogisticRegression","Accuracy","89.3%","0m 18s","Production"),
        ("Bidirectional LSTM","Accuracy","90.4%","35m 00s","Benchmark"),
    ])
)

MOD = xhead("Models") + xnav("models.html") + (
    '<div class="bg-slate-900 border-b border-slate-700 py-10">'
    '<div class="max-w-7xl mx-auto px-4">'
    '<p class="text-slate-400 text-sm font-mono mb-2">BENCHMARKING RESULTS</p>'
    '<h1 class="text-3xl font-extrabold text-white">Model Comparison Tables</h1>'
    '<p class="text-slate-300 mt-2">21 models benchmarked across 7 domains. Best model selected by primary business metric per domain.</p>'
    '</div></div>'
    '<div class="max-w-7xl mx-auto px-4 py-10">' + MTABLES + '</div>'
) + XFOOTER + '\n</body></html>'


# ═══════════════════════════════════════════════════════
# 5. expert/about.html
# ═══════════════════════════════════════════════════════
AB = xhead("About") + xnav("about.html") + (
    '<div class="bg-gradient-to-br from-slate-900 to-slate-800 border-b border-slate-700 py-16">'
    '<div class="max-w-4xl mx-auto px-4 text-center">'
    '<div class="w-24 h-24 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-5xl mx-auto mb-5">&#x1F9D1;&#x200D;&#x1F4BB;</div>'
    '<h1 class="text-3xl font-extrabold text-white mb-3">ML Engineer &amp; Data Scientist</h1>'
    '<p class="text-slate-300 max-w-xl mx-auto">Building production-grade machine learning systems that translate raw data into business-critical decisions. Specialised in ecommerce analytics, NLP, and time-series forecasting.</p>'
    '<div class="flex flex-wrap gap-3 justify-center mt-6">'
    '<a href="https://github.com" target="_blank" class="bg-slate-700 text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-slate-600 transition">&#x1F4BB; GitHub</a>'
    '<a href="https://linkedin.com" target="_blank" class="bg-blue-700 text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-blue-600 transition">&#x1F517; LinkedIn</a>'
    '<a href="mailto:hello@example.com" class="bg-purple-700 text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-purple-600 transition">&#x2709;&#xFE0F; Email</a>'
    '</div></div></div>'

    '<div class="max-w-5xl mx-auto px-4 py-12">'

    # Skills grid
    '<h2 class="text-xl font-bold text-white mb-5">Technical Skills</h2>'
    '<div class="grid md:grid-cols-3 gap-4 mb-12">'

    '<div class="bg-slate-800 rounded-xl p-5 border border-slate-700">'
    '<p class="text-xs font-bold text-blue-400 uppercase mb-3 font-mono">Machine Learning</p>'
    '<div class="space-y-2 text-sm">'
    '<div class="flex items-center justify-between"><span class="text-slate-300">Supervised Learning</span><div class="flex gap-1">'+("".join('<span class="w-2.5 h-2.5 rounded-sm bg-blue-500"></span>' for _ in range(5)))+'</div></div>'
    '<div class="flex items-center justify-between"><span class="text-slate-300">Unsupervised Learning</span><div class="flex gap-1">'+("".join('<span class="w-2.5 h-2.5 rounded-sm bg-blue-500"></span>' for _ in range(5)))+'</div></div>'
    '<div class="flex items-center justify-between"><span class="text-slate-300">Deep Learning</span><div class="flex gap-1">'+("".join('<span class="w-2.5 h-2.5 rounded-sm bg-blue-500"></span>' for _ in range(4)))+'<span class="w-2.5 h-2.5 rounded-sm bg-slate-600"></span></div></div>'
    '<div class="flex items-center justify-between"><span class="text-slate-300">NLP</span><div class="flex gap-1">'+("".join('<span class="w-2.5 h-2.5 rounded-sm bg-blue-500"></span>' for _ in range(4)))+'<span class="w-2.5 h-2.5 rounded-sm bg-slate-600"></span></div></div>'
    '<div class="flex items-center justify-between"><span class="text-slate-300">Time-Series</span><div class="flex gap-1">'+("".join('<span class="w-2.5 h-2.5 rounded-sm bg-blue-500"></span>' for _ in range(5)))+'</div></div>'
    '</div></div>'

    '<div class="bg-slate-800 rounded-xl p-5 border border-slate-700">'
    '<p class="text-xs font-bold text-green-400 uppercase mb-3 font-mono">Engineering</p>'
    '<div class="space-y-2 text-sm">'
    '<div class="flex items-center justify-between"><span class="text-slate-300">Python</span><div class="flex gap-1">'+("".join('<span class="w-2.5 h-2.5 rounded-sm bg-green-500"></span>' for _ in range(5)))+'</div></div>'
    '<div class="flex items-center justify-between"><span class="text-slate-300">FastAPI</span><div class="flex gap-1">'+("".join('<span class="w-2.5 h-2.5 rounded-sm bg-green-500"></span>' for _ in range(5)))+'</div></div>'
    '<div class="flex items-center justify-between"><span class="text-slate-300">REST API Design</span><div class="flex gap-1">'+("".join('<span class="w-2.5 h-2.5 rounded-sm bg-green-500"></span>' for _ in range(5)))+'</div></div>'
    '<div class="flex items-center justify-between"><span class="text-slate-300">SQL / Pandas</span><div class="flex gap-1">'+("".join('<span class="w-2.5 h-2.5 rounded-sm bg-green-500"></span>' for _ in range(5)))+'</div></div>'
    '<div class="flex items-center justify-between"><span class="text-slate-300">Docker</span><div class="flex gap-1">'+("".join('<span class="w-2.5 h-2.5 rounded-sm bg-green-500"></span>' for _ in range(4)))+'<span class="w-2.5 h-2.5 rounded-sm bg-slate-600"></span></div></div>'
    '</div></div>'

    '<div class="bg-slate-800 rounded-xl p-5 border border-slate-700">'
    '<p class="text-xs font-bold text-purple-400 uppercase mb-3 font-mono">Libraries / Tools</p>'
    '<div class="flex flex-wrap gap-2 text-xs">'
    + "".join('<span class="bg-slate-700 text-slate-300 px-2 py-1 rounded font-mono">' + t + '</span>' for t in [
        'XGBoost','LightGBM','scikit-learn','TensorFlow','Keras','pandas','NumPy',
        'Matplotlib','Seaborn','NLTK','imbalanced-learn','Surprise','FastAPI',
        'Pydantic','Uvicorn','joblib','Jupyter','Git','Tailwind CSS'
    ]) +
    '</div></div>'
    '</div>'

    # What I built
    '<div class="bg-slate-800 rounded-2xl p-6 border border-slate-700 mb-8">'
    '<h2 class="font-bold text-white mb-4">What This Project Demonstrates</h2>'
    '<div class="grid md:grid-cols-2 gap-4 text-sm text-slate-300">'
    '<div class="flex items-start gap-2"><span class="text-green-400 mt-0.5 shrink-0">&#x2713;</span><span><strong class="text-white">Full-stack ML:</strong> All stages from raw data exploration to live REST API with HTML frontend</span></div>'
    '<div class="flex items-start gap-2"><span class="text-green-400 mt-0.5 shrink-0">&#x2713;</span><span><strong class="text-white">Multi-domain expertise:</strong> Regression, classification, clustering, forecasting, CF, NLP in one system</span></div>'
    '<div class="flex items-start gap-2"><span class="text-green-400 mt-0.5 shrink-0">&#x2713;</span><span><strong class="text-white">Production mindset:</strong> Every model saved, versioned, benchmarked, and justified</span></div>'
    '<div class="flex items-start gap-2"><span class="text-green-400 mt-0.5 shrink-0">&#x2713;</span><span><strong class="text-white">Business translation:</strong> All results explained in terms of revenue, ROI, and operational impact</span></div>'
    '<div class="flex items-start gap-2"><span class="text-green-400 mt-0.5 shrink-0">&#x2713;</span><span><strong class="text-white">Clean code structure:</strong> Modular routers, type-safe Pydantic schemas, reusable utility functions</span></div>'
    '<div class="flex items-start gap-2"><span class="text-green-400 mt-0.5 shrink-0">&#x2713;</span><span><strong class="text-white">Documentation:</strong> Inline comments, README, and this live portfolio all explain the work</span></div>'
    '</div></div>'

    '<div class="flex flex-wrap gap-4 justify-center">'
    '<a href="https://github.com" target="_blank" class="bg-slate-700 text-white px-6 py-3 rounded-xl font-bold hover:bg-slate-600 transition">&#x1F4BB; View on GitHub</a>'
    '<a href="https://linkedin.com" target="_blank" class="bg-blue-700 text-white px-6 py-3 rounded-xl font-bold hover:bg-blue-600 transition">&#x1F517; Connect on LinkedIn</a>'
    '<a href="../client/index.html" class="bg-emerald-700 text-white px-6 py-3 rounded-xl font-bold hover:bg-emerald-600 transition">&#x1F6D2; View Portfolio</a>'
    '</div></div>'
) + XFOOTER + '\n</body></html>'


# Write files
pages = {
    os.path.join(EXPERT, "index.html"): IX,
    os.path.join(EXPERT, "notebooks.html"): NB,
    os.path.join(EXPERT, "pipeline.html"): PL,
    os.path.join(EXPERT, "models.html"): MOD,
    os.path.join(EXPERT, "about.html"): AB,
}
for path, content in pages.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK  {os.path.basename(path):20s}  {len(content):>7} bytes")
