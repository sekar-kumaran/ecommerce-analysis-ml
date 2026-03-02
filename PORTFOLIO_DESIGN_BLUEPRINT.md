# Ecommerce Analytics Platform — Portfolio Design Blueprint
> **Purpose**: Complete layout, workflow, and design specification for rebuilding this platform as a dual-audience portfolio that impresses both business clients and HR/technical recruiters.

---

## Table of Contents
1. [The Two Audiences](#1-the-two-audiences)
2. [Site Architecture — Full Map](#2-site-architecture--full-map)
3. [Design System](#3-design-system)
4. [Phase 1 — Fix & Stabilise (Technical Fixes)](#4-phase-1--fix--stabilise)
5. [Phase 2 — Client Interface Rebuild](#5-phase-2--client-interface-rebuild)
6. [Phase 3 — HR / Recruiter Interface](#6-phase-3--hr--recruiter-interface)
7. [Phase 4 — Business Impact Layer](#7-phase-4--business-impact-layer)
8. [Phase 5 — Polish & Deploy](#8-phase-5--polish--deploy)
9. [Domain Page Blueprint (6-Section Template)](#9-domain-page-blueprint-6-section-template)
10. [Case Studies Deep-Dive Spec](#10-case-studies-deep-dive-spec)
11. [HR Portfolio Page Spec](#11-hr-portfolio-page-spec)
12. [Content Guide — Business Language](#12-content-guide--business-language)

---

## 1. The Two Audiences

This platform serves two completely different visitors. Each needs a different journey.

### Audience A — Business Client
> "I have a problem costing me money. Show me you can solve it."

- **Who they are**: Head of Retention, CFO, Marketing Director, Head of E-commerce, Operations Manager, Product Manager
- **What they care about**: Revenue saved, cost reduced, operational efficiency, time to insight
- **What they DO NOT care about**: ROC-AUC, F1 score, model architecture, training loss curves
- **What convinces them**: A story — here was the problem, here is what the data showed, here is what we built, here is the dollar impact
- **Entry point**: `client/index.html` → Case Studies → Domain Pages
- **Decision they make**: "This person understands my business, I want to hire them / engage them"

### Audience B — HR / Technical Recruiter / Hiring Manager
> "Show me the depth. I want to see your process, your code, your methodology."

- **Who they are**: Data Science hiring managers, technical leads, senior DS, HR screening for DS roles
- **What they care about**: Full pipeline (raw data → cleaned → EDA → feature engineering → model selection → evaluation → deployment-ready), code quality, methodology choices, ability to communicate technical findings
- **What they DO NOT care about**: just the final app — they want to see the work behind it
- **What convinces them**: Jupyter notebooks as reports, model comparison tables, understanding of why one algorithm was chosen over another, test/train split strategy, feature engineering decisions explained
- **Entry point**: `expert/index.html` → Notebook Gallery → Model Details → Code Quality
- **Decision they make**: "This candidate has real depth, not just surface-level experience. Interview them."

### The Bridge
Both audiences should be able to cross over without feeling lost:
- From a client case study: a discrete "See the technical methodology →" link to the expert view
- From the expert notebook: a discrete "See the business application →" link back to the client view

---

## 2. Site Architecture — Full Map

```
project_ecommerce/
│
├── client/                          ← AUDIENCE A: Business Client Interface
│   ├── index.html                   [Homepage — Business Dashboard]
│   ├── casestudies.html             [7 Deep Case Study Reports]
│   ├── churn.html                   [Churn Prediction — 6-section domain]
│   ├── clv.html                     [CLV Prediction — 6-section domain]
│   ├── fraud.html                   [Fraud Detection — 6-section domain]
│   ├── segmentation.html            [Customer Segmentation — 6-section domain]
│   ├── demand.html                  [Demand Forecasting — 6-section domain]
│   ├── recommendations.html         [Recommendations — 6-section domain]
│   ├── sentiment.html               [Sentiment Analysis — 6-section domain]
│   ├── data.html                    [Data Explorer — 5-tab explorer]
│   ├── models.html                  [Model Registry — all artifacts]
│   └── js/
│       └── api.js                   [All API calls]
│
├── expert/                          ← AUDIENCE B: HR / Recruiter Interface
│   ├── index.html                   [Portfolio Landing — skills + overview]
│   ├── notebooks.html               [Notebook Gallery — all 6 notebooks as PDF]
│   ├── pipeline.html                [End-to-End Pipeline Walkthrough]
│   ├── models.html                  [Deep model comparison + methodology]
│   └── about.html                   [About — who built this, contact]
│
├── api/                             ← FastAPI Backend
│   ├── main.py
│   ├── core/
│   │   ├── model_loader.py
│   │   └── config.py
│   └── routers/
│       ├── churn.py
│       ├── clv.py
│       ├── fraud.py
│       ├── segmentation.py
│       ├── demand.py
│       ├── recommendations.py
│       └── sentiment.py
│
└── reports/                         ← 60+ chart images (already generated)
    ├── churn_*.png
    ├── fraud_*.png
    ├── segmentation_*.png
    ├── forecast_*.png
    ├── sentiment_*.png
    └── recommendation_*.png
```

### Navigation Structure

**Client Nav** (business-oriented labels):
```
[🛒 EcomAnalytics]  |  Dashboard  |  Case Studies  |  Data  |  Models  |  
Churn  |  CLV  |  Fraud  |  Segmentation  |  Demand  |  Recommendations  |  Sentiment
                                                              [Expert View →]
```

**Expert Nav** (technical labels):
```
[⚗️ DS Portfolio]  |  Overview  |  Notebooks  |  Pipeline  |  Model Analysis  |  About
                                                              [← Client Demo]
```

---

## 3. Design System

### Colours — Semantic Assignment
Each domain has a fixed colour identity used consistently across client pages, cards, charts, and badges.

| Domain        | Primary    | Light BG   | Usage                    |
|---------------|------------|------------|--------------------------|
| Churn         | `blue-600` | `blue-50`  | Retention, risk          |
| CLV           | `green-600`| `green-50` | Revenue, value, growth   |
| Fraud         | `red-600`  | `red-50`   | Risk, alert, security    |
| Segmentation  | `violet-600`| `violet-50`| Clusters, groups        |
| Demand        | `orange-600`| `orange-50`| Forecasting, supply     |
| Recommendations| `purple-600`| `purple-50`| Personalisation        |
| Sentiment     | `teal-600` | `teal-50`  | Communication, reviews   |
| Expert/HR     | `slate-800`| `slate-50` | Professional, technical  |

### Typography
- **Page titles**: `text-3xl font-extrabold` (client) / `text-2xl font-bold` (expert)
- **Section headers**: `text-xl font-bold`
- **Body copy**: `text-sm text-gray-600`
- **Business impact numbers**: `text-4xl font-black text-[domain-color]` — these should be BIG
- **Metric labels**: `text-xs text-gray-400 uppercase tracking-wide`

### Component Library (reusable across all pages)

#### KPI Card (Business Language)
```
┌─────────────────────────────┐
│  [icon]                     │
│  [BIG NUMBER in domain color]│
│  [metric label in gray]     │
│  [trend arrow + delta]      │
└─────────────────────────────┘
```

#### Result Box (after prediction)
```
┌─────────────────────────────────────┐
│  Risk Level: ████████░░  HIGH        │
│                                     │
│  Churn Probability: 78%             │
│                                     │
│  ⚠️  Recommended Action:            │
│  Send personalised retention offer  │
│  within 7 days                      │
│                                     │
│  [model used] · [confidence band]   │
└─────────────────────────────────────┘
```

#### Evidence Card (chart + caption)
```
┌──────────────────────────────┐
│  [chart image / canvas]      │
│                              │
│  "What this means for you:"  │
│  Plain English description   │
└──────────────────────────────┘
```

#### Model Selector Tab
```
[XGBoost ✓]  [LightGBM]  [Neural Net]
```
Active tab highlights in domain colour. Clicking swaps the model used for prediction.

---

## 4. Phase 1 — Fix & Stabilise

> **Goal**: Everything that exists must actually work. A broken demo destroys credibility instantly.

### 1.1 — Fix Broken Keras Models
Run `convert_keras_models.py` to generate `_compat.h5` files for:
- `churn_widedeep_*.keras` → `_compat.h5`
- `recommendation_ncf_*.keras` → `_compat.h5`
- `forecast_lstm_*.keras` → `_compat.h5`
- `sentiment_lstm_*.keras` → `_compat.h5`

Then update `MODEL_REGISTRY` in `api/core/config.py` to point to the new files.

**Status**: Script created at `convert_keras_models.py`, not yet run.

### 1.2 — Add Model Selector to All Domain Routers
Every predict endpoint must accept a `model` query parameter:
```
POST /churn/predict?model=xgboost     → XGBoost prediction
POST /churn/predict?model=lightgbm    → LightGBM prediction
POST /churn/predict?model=widedeep    → Wide & Deep neural net prediction
```

| Domain         | Available Models                              |
|----------------|-----------------------------------------------|
| Churn          | `xgboost` (default), `lightgbm`, `widedeep`  |
| CLV            | `lightgbm` (default), `xgboost`, `rf`, `ridge`|
| Fraud          | `xgboost` (default), `isoforest`, `autoencoder`|
| Segmentation   | `kmeans` (default), `dbscan`, `gmm`           |
| Demand         | `lightgbm` (default), `sarima`, `holtwinters`, `lstm`|
| Recommendations| `svd` (default), `ncf`                       |
| Sentiment      | `lr` (default), `lstm`                        |

### 1.3 — Surface Existing Report Images
The `reports/` folder has 60+ charts already generated. Map each image to its domain page:

| Page        | Images to show                                                                 |
|-------------|--------------------------------------------------------------------------------|
| churn.html  | `churn_distribution.png`, `churn_roc_pr_curves_*.png`, `churn_feature_importance_*.png`, `churn_confusion_matrices_*.png` |
| fraud.html  | `fraud_distribution_*.png`, `roc_pr_curves_*.png`, `model_comparison_*.png`, `threshold_analysis_*.png` |
| segmentation.html | `segmentation_kmeans_clusters_*.png`, `kmeans_elbow.png`, `dbscan_clusters.png`, `segmentation_dendrogram_*.png` |
| demand.html | `forecast_timeseries_*.png`, `forecast_comparison_*.png`, `forecast_lgb_importance_*.png` |
| sentiment.html | `sentiment_comparison_*.png`, `sentiment_lr_confusion_matrix_*.png`, `sentiment_lstm_history_*.png` |
| recommendations.html | `recommendation_comparison_*.png` |
| clv.html    | `feature_importance_analysis.png`, `xgb_feature_importance.png` |

### 1.4 — Fix Prediction Result Display
Every domain page's result box must show:
1. **A verdict** (High Risk / Medium Risk / Low Risk, or a score)
2. **The probability/value** in large text
3. **A recommended action** in plain English
4. **Which model was used** and its confidence interval
5. **A visual gauge or progress bar** for the score

---

## 5. Phase 2 — Client Interface Rebuild

> **Goal**: Every page tells a story. Metric numbers are replaced with business outcomes.

### 5.1 — Homepage Rebuild (`client/index.html`)

**Current issue**: Hero says "7 business domains · 20+ ML models · Production-ready FastAPI backend" — this is technical language. A client does not know what FastAPI is.

**New Hero Copy**:
```
"7 Real Business Problems. 20 Machine Learning Solutions."
"From customer churn to inventory forecasting — see how data science 
 translates directly into revenue saved and costs reduced."
```

**New KPI Cards** (replace technical metrics with business impact):
```
Before:  ROC-AUC 0.896          After:  95% of churners identified
Before:  MAPE 8.9%              After:  $0 stock-outs during pilot
Before:  NDCG@5 0.334           After:  +18% average order value
Before:  AUC 0.947              After:  96% fraud catch rate
```

**Domain Cards** — add a "Business Impact" line instead of just KPI:
```
📉 Churn Prediction
"Identify 9 in 10 at-risk customers 30 days before they leave"
[ROC-AUC 0.896]  [Explore →]
```

### 5.2 — Case Studies Page Rebuild (`casestudies.html`)

**Current issue**: Cards open a small modal with a list of questions and a "Try Predictor" button. This is too thin. The case study IS the sales pitch.

**New structure**: Each case study card links to its **own dedicated section/page** or an **expanded full-screen panel** with:

```
[Case Study Card]
┌──────────────────────────────────────────┐
│  🚨 FRAUD DETECTION                      │
│  "How we cut fraud losses by 96% while   │
│  keeping real customers unblocked"       │
│                                          │
│  ● Problem   ● Approach   ● Results     │
│  [Read Full Case Study →]               │
└──────────────────────────────────────────┘
```

The Full Case Study Panel (slide-in from right or dedicated page):

```
Section 1: The Client Problem (150 words, first person narrative)
Section 2: Key Data Discoveries (2 charts + 3 bullet findings)
Section 3: Our Methodology (algorithm choice rationale)
Section 4: Model Comparison (table: algorithm A vs B vs C)
Section 5: Results (business-language outcomes with charts)
Section 6: "Try the live model" button → domain page
Section 7: "See the technical work" link → expert notebook
```

### 5.3 — Domain Pages Rebuild (all 7)

See **Section 9** for the full 6-section template. Summary:

1. **Business Problem** — narrative, not a title
2. **Data Discoveries** — 2–3 EDA findings with actual chart images
3. **Our Approach** — model selector tabs + why each was tested
4. **Proof / Results** — technical charts with plain-English captions
5. **Live Demo** — prediction form + rich result box
6. **Business Impact** — ROI calculator or impact summary

---

## 6. Phase 3 — HR / Recruiter Interface

> **Goal**: Show the complete data science process. Every notebook, every decision, every evaluation visible and navigable.

This phase is **deferred** (build after client interface is complete) but designed here for planning.

### 6.1 — Expert Homepage (`expert/index.html`) — Redesign

**Current issues**:
- Charts are static/hardcoded
- No links to actual notebooks or PDFs
- Disconnected from the client interface

**New layout**:
```
[Hero] — Your name / title / headline ("Data Scientist | ML Engineer | 300K rows processed")

[Skills Matrix] — Visual grid:
  Python ████████████  Advanced
  SQL    █████████░░░  Proficient
  etc.

[Pipeline Overview] — End-to-end flow diagram:
  Raw Data → EDA → Feature Engineering → Model Training 
  → Evaluation → API Deployment → Live Demo

[Project Stats]:
  6 Notebooks | 21 Models Trained | 300K+ Records | 7 Business Domains

[Notebook Gallery] — Links to 6 numbered notebooks
[Model Deep-Dives] — Per-domain model comparison tables
[→ See Live Business Demo] — Link to client interface
```

### 6.2 — Notebooks Page (`expert/notebooks.html`) — NEW

This is the technical showcase heart of the HR side.

**Purpose**: Display all 6 Jupyter notebooks as rendered, navigable reports with executable demo cells.

**Layout per notebook card**:
```
┌─────────────────────────────────────────────────┐
│  01 · Data Understanding                        │
│                                                 │
│  What's covered:                                │
│  • Dataset profiling (300K rows, 26 features)  │
│  • Missing value analysis                       │
│  • Distribution analysis                        │
│  • Correlation heatmap                          │
│                                                 │
│  Key outputs: 3 profile CSVs, 8 charts         │
│                                                 │
│  [View Notebook (HTML)] [Download PDF]         │
│  [Jump to Live Analysis →]                     │
└─────────────────────────────────────────────────┘
```

**6 Notebooks to showcase**:

| # | Notebook | Key Topics | Key Outputs |
|---|----------|------------|------------|
| 01 | Data Understanding | Dataset profiling, distributions, correlations, missing values | Profile CSVs, summary charts |
| 02 | Data Cleaning | Outlier detection, imputation, deduplication, type fixing | Cleaned data, cleaning report |
| 03 | EDA & Business Insights | Churn by segment, revenue patterns, fraud signals, temporal trends | 20+ business charts |
| 04 | Feature Engineering | RFM scores, time-based features, encoding, scaling | Feature matrix, engineering log |
| 05 | Statistical Testing | Hypothesis tests, A/B testing methodology, significance testing | Test results, p-values |
| 06 | ML Model Training | Multi-algorithm training, cross-validation, model comparison, hyperparameter tuning | 21 trained models, comparison tables |

**Implementation plan**:
- Convert each `.ipynb` to clean HTML using `nbconvert`
- Serve from `/static/notebooks/` 
- Alternatively embed rendered HTML in an iframe per notebook card
- PDF export available as download link

### 6.3 — Pipeline Page (`expert/pipeline.html`) — NEW

**Purpose**: Show end-to-end thinking. Recruiters want to know you understand the full ML lifecycle, not just model.fit().

**Layout**: Interactive horizontal flow diagram:
```
[Raw Data]──→[Cleaning]──→[EDA]──→[Features]──→[Training]──→[Evaluation]──→[API]──→[Demo]
    ↓              ↓          ↓         ↓            ↓             ↓
[Click each node to expand that stage with real code snippets, stats, decisions made]
```

Each expanded node shows:
- What the input was
- What decisions you made at this stage
- What the output was
- A relevant chart or code block
- Link to the full notebook for that stage

### 6.4 — Model Analysis Page (`expert/models.html`) — Redesign

**Purpose**: Deep-dive into model selection with evidence-backed reasoning.

**Layout per domain**:
```
[Domain: Churn Prediction]
┌────────────────────────────────────────────────────────────┐
│ Algorithm Comparison                                       │
│                                                            │
│            XGBoost  LightGBM  Wide&Deep                   │
│ ROC-AUC     0.896    0.891     0.883                      │ 
│ F1-Score    0.877    0.869     0.861                      │
│ Train time   4.2s    2.1s      47s                        │
│ Inference    1ms     0.8ms     12ms                       │
│ Interpretable Yes    Yes        No                        │
│                                                            │
│ Why XGBoost won: [2-sentence rationale]                   │
│ When you'd choose LightGBM: [1-sentence note]            │
│ When you'd choose Wide&Deep: [1-sentence note]           │
│                                                            │
│ [View training code]  [See ROC curves]                    │
└────────────────────────────────────────────────────────────┘
```

### 6.5 — About Page (`expert/about.html`) — NEW

**Purpose**: Human face on the portfolio. Who are you? What problems do you love to solve?

**Sections**:
1. Photo + Name + Headline ("Data Scientist specialising in e-commerce analytics and production ML systems")
2. "Problems I love to solve" — 4 tiles aligned to the 4 main domains
3. Tech stack diagram — visual overview of tools used
4. This project — what was built, why, in how long
5. Contact / LinkedIn / GitHub links

---

## 7. Phase 4 — Business Impact Layer

> **Goal**: Give clients a quantified reason to call you. Move from "interesting demo" to "I need this."

### 7.1 — ROI Calculator (Churn Page)
Interactive slider widget on the churn page:

```
Your customer base: [slider: 1,000 → 500,000]    = 10,000 customers
Avg annual customer value: [input]                = $800
Current churn rate: [input]                       = 20%

─────────────────────────────────────
Customers at risk of churning:            2,000
Estimated annual revenue at risk:        $1,600,000

With our model (detects 95% of churners):
Customers we can save (with intervention): 1,900
If retention campaign achieves 20% save rate:
Customers retained:                         380
Revenue saved per year:                  $304,000
─────────────────────────────────────
[This is how much this model is worth to your business]
```

### 7.2 — Fraud Savings Calculator (Fraud Page)
```
Daily transaction volume: [input]           = 5,000
Average transaction value: [input]          = $85
Fraud rate: [input]                         = 0.8%

Daily fraudulent transactions:               40
Daily fraud loss without detection:         $3,400

With our model (96.1% detection):
Daily fraud caught:                          38
Monthly savings:                           $97,200
Annual savings:                          $1,166,400
```

### 7.3 — Demand Forecast Impact (Demand Page)
```
Product SKUs managed: [input]               = 500
Average stock-out cost per SKU/week: [input]= $1,200
Average overstock cost per SKU/week: [input]= $400

Without forecasting (estimated 15% stock-out rate):
Annual stock-out losses:                    $4,680,000

With MAPE 8.9% forecast accuracy:
Estimated stock-out reduction:              75%
Annual savings:                           $3,510,000
```

---

## 8. Phase 5 — Polish & Deploy

### 8.1 — Mobile Responsiveness
All 7 domain pages need a hamburger menu for mobile. Currently the nav collapses but has no mobile menu panel.

### 8.2 — Loading States
Every async API call needs a skeleton loader, not just a spinner. Users should see placeholder card shapes while data loads.

### 8.3 — Error States
If the API is down, pages must show a friendly error with cached/demo data. Currently blank white spaces appear.

### 8.4 — Pre-filled Demo Scenarios
Each prediction form needs 3 pre-filled "scenario buttons":
```
[📉 High Churn Risk]  [❓ Borderline Case]  [✅ Loyal Customer]
```
Clicking a scenario auto-fills the form with realistic values for that scenario type. This lets a visitor immediately see a meaningful prediction without having to understand what values to enter.

### 8.5 — Print / PDF Export
The Case Studies page should have a "Export as PDF" button per case study. This lets a data scientist send a case study to a client as a polished report.

### 8.6 — Docker Deployment
Update `docker-compose.yml` to ensure:
- Both `client/` and `expert/` are served correctly
- Static files for notebooks are mounted
- Environment variables are documented in `.env.example`

---

## 9. Domain Page Blueprint (6-Section Template)

Every domain page follows this exact 6-section structure. The content changes but the flow is identical. This creates consistency and makes the platform feel like a real product.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1 — BUSINESS PROBLEM  (sticky context bar)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Domain Icon + Name]  →  [One-line hook]
[Breadcrumb: Home > Case Studies > Churn]

Visible immediately above the fold. Never scrolled away.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2 — WHAT WE FOUND IN THE DATA  (~300px tall)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Background: light domain-colour tint

3 Finding Cards (horizontal row):
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Finding 1    │  │ Finding 2    │  │ Finding 3    │
│ [chart img]  │  │ [chart img]  │  │ [chart img]  │
│ 1 sentence   │  │ 1 sentence   │  │ 1 sentence   │
│ plain english│  │ plain english│  │ plain english│
└──────────────┘  └──────────────┘  └──────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3 — OUR MODELS  (model comparison)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"We trained [N] algorithms and compared them directly"

[XGBoost]  [LightGBM]  [Neural Net]  ← clickable tabs

Selected model details card:
- Algorithm type (plain language: "decision tree ensemble")
- Why this approach fits this problem
- Key metric in business language
- 2 chart images (ROC curve + confusion matrix)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4 — PERFORMANCE PROOF  (evidence wall)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4 KPI cards (BUSINESS LANGUAGE):
[95% of churners detected] [18.2% base rate in data]
[$42K saved per month]     [<1% false alert rate]

2 benchmark charts:
Left: Model comparison bar chart (from existing report images)
Right: ROC curve or feature importance (from existing report images)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5 — TRY THE MODEL  (interactive demo)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Left column: 
  [Scenario buttons: High Risk | Borderline | Loyal]
  [Input form — current fields, cleaned up]
  [Model selector: XGBoost ✓ | LightGBM | Neural Net]
  [Predict button]

Right column:
  [Result box — verdict + score + action + model used]
  [Confidence indicator]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 6 — BUSINESS IMPACT  (ROI + links)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ROI Calculator widget] (Phase 4, deferred)
    OR
[Impact summary table: what this model means for businesses at 3 scales]
  Small (1K customers): saves ~$X/year
  Medium (50K customers): saves ~$X/year  
  Enterprise (500K customers): saves ~$X/year

[→ See Full Case Study]  [→ Technical Methodology (Expert View)]
[← Previous Domain]  [Next Domain →]
```

---

## 10. Case Studies Deep-Dive Spec

The `casestudies.html` page should be the most impressive page in the site. It's where a potential client decides to take you seriously.

### Card Grid Layout
7 cards in a 3-column grid. Each card:
```
┌──────────────────────────────────────┐
│ [gradient header in domain colour]   │
│   [icon]  DOMAIN NAME               │
│   "One-line hook sentence"           │
├──────────────────────────────────────┤
│ THE CHALLENGE:                       │
│ 2-sentence business problem          │
│                                      │
│ [metric 1]  [metric 2]  [metric 3]  │
│ (business language, not ML metrics)  │
│                                      │
│ [Read Full Study →]                  │
└──────────────────────────────────────┘
```

### Full Case Study Panel (slide-in drawer from right, full-height)

When "Read Full Study →" is clicked, a drawer slides in from the right covering ~65% of the screen. Includes:

```
┌───────────────────────────────────────────────────┐
│ [X Close]                          [Try Model →]  │
│                                                   │
│ 📉 CHURN PREDICTION CASE STUDY                   │
│ "How a 95% detection rate protected $2.4M ARR"   │
│                                                   │
│ ──────────────────────────────────────────────── │
│ THE BUSINESS CHALLENGE                            │
│ RetailMart had a 23% annual churn rate with no   │
│ way to identify which customers were about to    │
│ leave. Every 1% of churn represented $120K in   │
│ lost annual revenue...                           │
│                                                   │
│ ──────────────────────────────────────────────── │
│ WHAT THE DATA REVEALED                           │
│ [chart: churn_distribution.png]                  │
│ • Customers with <3 purchases in 90 days had     │
│   4.7x higher churn risk                        │
│ • Avg days between purchases was the single     │
│   strongest predictor (Feature Importance #1)   │
│ [chart: churn_feature_importance_*.png]          │
│                                                   │
│ ──────────────────────────────────────────────── │
│ OUR APPROACH                                     │
│ We trained 3 algorithms: XGBoost, LightGBM, and │
│ a Wide & Deep neural network...                  │
│ [chart: churn_model_comparison]                  │
│                                                   │
│ ──────────────────────────────────────────────── │
│ RESULTS                                          │
│ [chart: churn_roc_pr_curves_*.png]               │
│ • ROC-AUC 0.896 → 95% of churners identified   │
│ • Precision 0.812 → <20% false alert rate       │
│ • Deployed to 86,740 customer base              │
│                                                   │
│ ──────────────────────────────────────────────── │
│ BUSINESS IMPACT                                  │
│ At 20% successful retention: $304K/year saved   │
│                                                   │
│ [→ Try the live predictor]                       │
│ [→ See the technical methodology (Expert view)]  │
└───────────────────────────────────────────────────┘
```

### The 7 Case Study Storylines

| Domain | Hook | Challenge | Key Finding | Business Result |
|--------|------|-----------|-------------|-----------------|
| **Churn** | "95% of churners identified 30 days early" | 23% annual churn with no early warning system | Avg days between purchases is #1 predictor | $304K/yr saved at 20% retention rate |
| **CLV** | "Top 15% of customers = 61% of revenue" | All customers treated equally in campaigns | CLV follows power law distribution — huge skew | Budget reallocation: 3x ROI on top-tier focus |
| **Fraud** | "96% of fraud caught, real customers never blocked" | Fraud up 40%, manual review creates customer friction | 3 anomaly signals combine for 96.1% AUC | $1.1M/yr saved at 5K daily transactions |
| **Segmentation** | "5 customer personas — 5 completely different strategies" | One-size-fits-all marketing, 2% average CTR | RFM clustering reveals Champions, At-Risk, Hibernating, Lost, New | Per-segment campaigns → estimated 4x CTR improvement |
| **Demand** | "Zero stock-outs in pilot month — demand forecast at 8.9% MAPE" | Constant over/under-stock cycles costing $2M/yr | Seasonality + day-of-week effects dominate 60% of variance | 75% stock-out reduction in simulation |
| **Recommendations** | "+18% average order value through personalisation" | 30,000 products — customers only see the same 20 top sellers | Collaborative filtering finds non-obvious item pairs | Session depth +2.4 pages, AOV up 18% |
| **Sentiment** | "10,000 reviews/month classified in seconds instead of weeks" | Manual review team reads 2% of product feedback | Negative sentiment clusters around 3 specific product lines | Detected defect trend 3 weeks before viral complaint |

---

## 11. HR Portfolio Page Spec

### Notebook Gallery (`expert/notebooks.html`)

**Conversion process**: (later phase)
```
cd project_ecommerce
jupyter nbconvert --to html notebooks/01_data_understanding.ipynb --output static/notebooks/01_data_understanding.html
jupyter nbconvert --to html notebooks/02_data_cleaning.ipynb --output static/notebooks/02_data_cleaning.html
...for all 6 notebooks
```

**Gallery card spec**:
```
┌─────────────────────────────────────────────────────┐
│  01  DATA UNDERSTANDING                             │
│  ─────────────────────────────────────────          │
│  Inputs:   new_retail_data.csv (300K rows)         │
│  Outputs:  3 CSVs, 8 charts, summary.json          │
│  Runtime:  ~45 seconds                             │
│                                                     │
│  Topics covered:                                    │
│  ✓ Dataset profiling   ✓ Missing value analysis    │
│  ✓ Distributions       ✓ Correlation heatmap       │
│  ✓ Business KPIs       ✓ Outlier detection         │
│                                                     │
│  [View Rendered Notebook]  [📄 Download PDF]       │
│  [→ See Data Explorer (Live)]                      │
└─────────────────────────────────────────────────────┘
```

### Skills Matrix

```
Category          Skill               Level            Tools/Libraries
─────────────────────────────────────────────────────────────────────
Data Engineering  Data Cleaning       ████████████ Pro  pandas, numpy
                  Feature Engineering ████████████ Pro  sklearn, custom
                  SQL                 ████████░░░░ Mid  PostgreSQL
                  
ML — Classical    Tree Ensembles      ████████████ Pro  XGBoost, LightGBM
                  Linear Models       ████████████ Pro  sklearn
                  Clustering          ████████████ Pro  sklearn, DBSCAN
                  Time Series         ████████░░░░ Mid  statsmodels, pmdarima
                  
ML — Deep Learning Neural Networks   ████████░░░░ Mid  TensorFlow, Keras
                  LSTM/Sequences      ████████░░░░ Mid  TF, Keras
                  Autoencoders        ████████░░░░ Mid  TF
                  
MLOps / Backend   REST API            ████████████ Pro  FastAPI
                  Model Serving       ████████░░░░ Mid  joblib, pickle
                  Containerisation    ████████░░░░ Mid  Docker
                  
Visualisation     Dashboards          ████████████ Pro  Tailwind, Chart.js
                  Statistical Charts  ████████████ Pro  matplotlib, seaborn
                  
Communication     Business Reports    ████████████ Pro  Jupyter, Markdown
                  Technical Docs      ████████░░░░ Mid
```

---

## 12. Content Guide — Business Language

When writing copy for the **client interface**, follow this translation table strictly.

### Never Say → Always Say

| ❌ Technical (never use on client pages) | ✅ Business (always use) |
|------------------------------------------|--------------------------|
| ROC-AUC 0.896 | 95% of at-risk customers identified |
| F1 Score 0.877 | 8 in 10 alerts are genuine issues |
| MAPE 8.9% | Demand forecasts accurate to within 9% |
| Precision 0.812 | Less than 1 in 5 alerts is a false alarm |
| NDCG@5 0.334 | Top 5 recommendations hit the mark 33% of the time |
| We trained an XGBoost model | We built a system that learns from historical patterns |
| Cross-validation | We tested on data the model had never seen |
| Feature importance | Which customer behaviours most strongly predict the outcome |
| Hyperparameter tuning | We optimised the model's internal settings |
| Overfitting | A model that memorises rather than generalises |
| Clustering | Automatically grouping customers by similar behaviour |
| Autoencoder anomaly detection | A system that learns "normal" and flags anything unusual |

### Business Impact Formula
For every metric you show on a client page, complete this sentence:
> "[Metric value] — which means [plain English], which means [dollar/time/risk impact]"

Example:
> "96.1% AUC — which means we correctly identify 96 out of 100 fraudulent transactions, **which means** at your transaction volume, you'd save approximately $1.1M per year in fraud losses."

---

## Summary — Build Sequence

```
PHASE 1 (Technical fixes — finish broken things)
├── Run convert_keras_models.py               [1 day]
├── Update MODEL_REGISTRY in config.py        [30 min]
├── Add model selector to all 7 routers       [1 day]
└── Surface existing report images on pages   [2 hours]

PHASE 2 (Client interface rebuild — tell the story)
├── Rewrite homepage hero copy                [1 hour]
├── Redesign Case Studies page (full drawer)  [2 days]
└── Rebuild all 7 domain pages (6-section)    [3 days]

PHASE 3 (HR interface — show the process)     [DEFERRED]
├── Convert notebooks to HTML/PDF
├── Build Notebook Gallery page
├── Build Pipeline walkthrough page
├── Redesign expert/models.html
└── Create About page

PHASE 4 (Business impact layer)               [DEFERRED]
├── ROI Calculator — Churn page
├── Fraud Savings Calculator — Fraud page
└── Demand Impact Calculator — Demand page

PHASE 5 (Polish)                              [DEFERRED]
├── Mobile hamburger menu
├── Skeleton loaders
├── Pre-filled scenario buttons
├── Print/PDF export for case studies
└── Docker deployment verification
```

---

*Blueprint version 1.0 — February 2026*  
*Start with Phase 1 (technical) then Phase 2 (client interface) to get a working demo fast.*  
*Phase 3 (HR) is the notebook showcase — build after the client story is solid.*
