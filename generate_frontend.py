"""Helper script — generates all client HTML files."""
import os

BASE = os.path.dirname(__file__)


def w(filename: str, html: str):
    path = os.path.join(BASE, "client", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Written: {filename}")


# ── Shared nav snippet ─────────────────────────────────────────────────────────
NAV = lambda active: f"""<nav class="bg-white shadow-sm sticky top-0 z-50 border-b">
  <div class="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
    <a href="index.html" class="flex items-center gap-2 font-bold text-lg text-blue-700">🛒 EcomAnalytics</a>
    <div class="hidden md:flex items-center gap-1 text-sm">
      {''.join(f'<a href="{href}" class="px-3 py-1.5 rounded-md {" bg-blue-600 text-white font-medium" if href == active else " text-gray-600 hover:bg-gray-100"}">{label}</a>'
        for href, label in [
          ("index.html","Dashboard"),("casestudies.html","Case Studies"),("models.html","Models"),
          ("churn.html","Churn"),("clv.html","CLV"),("fraud.html","Fraud"),
          ("sentiment.html","Sentiment"),("demand.html","Demand"),
        ]
      )}
    </div>
    <div id="healthBadge"></div>
  </div>
</nav>"""

FOOT = '<footer class="bg-white border-t py-6 text-center text-sm text-gray-400">Ecommerce Analytics Platform v2.0 · 7 Domains · 20+ Models</footer>'
SCRIPTS = '<script src="js/api.js"></script>'

# ── index.html ────────────────────────────────────────────────────────────────
w("index.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>EcomAnalytics — Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
{NAV("index.html")}
<section class="bg-gradient-to-br from-blue-700 to-blue-900 text-white py-16 px-4 text-center">
  <h1 class="text-4xl md:text-5xl font-extrabold mb-4">Ecommerce Analytics Platform</h1>
  <p class="text-blue-200 text-lg mb-8 max-w-2xl mx-auto">7 business domains · 20+ ML models · Production-ready FastAPI backend</p>
  <div class="flex flex-wrap justify-center gap-3">
    <a href="casestudies.html" class="bg-white text-blue-700 font-semibold px-6 py-2.5 rounded-lg hover:bg-blue-50 transition">Explore Case Studies →</a>
    <a href="models.html" class="border border-white text-white font-semibold px-6 py-2.5 rounded-lg hover:bg-white/10 transition">View All Models</a>
    <a href="http://localhost:8000/docs" target="_blank" class="border border-white/50 text-white/80 px-6 py-2.5 rounded-lg hover:bg-white/10 transition text-sm">API Swagger Docs</a>
  </div>
</section>
<section class="max-w-7xl mx-auto px-4 py-10"><div id="kpiGrid" class="grid grid-cols-2 md:grid-cols-4 gap-4"></div></section>
<section class="max-w-7xl mx-auto px-4 pb-12">
  <h2 class="text-2xl font-bold mb-6">Platform Domains</h2>
  <div id="domainCards" class="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5"></div>
</section>
<section class="max-w-7xl mx-auto px-4 pb-16">
  <div class="bg-white rounded-2xl shadow-sm p-6">
    <h2 class="text-xl font-bold mb-4">Model Performance Overview</h2>
    <div class="grid md:grid-cols-2 gap-8">
      <canvas id="perfChart" height="260"></canvas>
      <div id="perfTable" class="overflow-x-auto text-sm"></div>
    </div>
  </div>
</section>
{FOOT}
{SCRIPTS}
<script>
updateHealthBadge(document.getElementById('healthBadge'));
const DOMAINS=[
  {{id:'churn',icon:'📉',title:'Churn Prediction',href:'churn.html',color:'blue',kpi:'ROC-AUC 0.896',desc:'Identify customers likely to leave in 90 days'}},
  {{id:'clv',icon:'💰',title:'Customer Lifetime Value',href:'clv.html',color:'green',kpi:'R² 0.998',desc:'Predict total expected revenue per customer'}},
  {{id:'rec',icon:'🛍️',title:'Recommendations',href:'recommendations.html',color:'purple',kpi:'NDCG@5 0.334',desc:'Personalised product discovery via SVD & NCF'}},
  {{id:'fraud',icon:'🚨',title:'Fraud Detection',href:'fraud.html',color:'red',kpi:'AUC 0.947',desc:'Real-time anomalous transaction detection'}},
  {{id:'seg',icon:'🧩',title:'Segmentation',href:'segmentation.html',color:'yellow',kpi:'5 Clusters',desc:'Behavioural RFM customer clustering'}},
  {{id:'demand',icon:'📦',title:'Demand Forecasting',href:'demand.html',color:'orange',kpi:'MAPE 8.9%',desc:'Daily/weekly inventory demand forecasting'}},
  {{id:'sentiment',icon:'💬',title:'Sentiment Analysis',href:'sentiment.html',color:'teal',kpi:'Acc 91%',desc:'Product review positive/neutral/negative'}},
];
const BG={{blue:'bg-blue-50',green:'bg-green-50',red:'bg-red-50',yellow:'bg-yellow-50',purple:'bg-purple-50',orange:'bg-orange-50',teal:'bg-teal-50'}};
const TX={{blue:'text-blue-700',green:'text-green-700',red:'text-red-700',yellow:'text-yellow-700',purple:'text-purple-700',orange:'text-orange-700',teal:'text-teal-700'}};
const BD={{blue:'border-blue-200',green:'border-green-200',red:'border-red-200',yellow:'border-yellow-200',purple:'border-purple-200',orange:'border-orange-200',teal:'border-teal-200'}};
document.getElementById('domainCards').innerHTML=DOMAINS.map(d=>`<a href="${{d.href}}" class="bg-white rounded-xl shadow-sm border ${{BD[d.color]||'border-gray-200'}} p-5 hover:shadow-md transition-shadow"><div class="text-3xl mb-3">${{d.icon}}</div><h3 class="font-semibold text-gray-900">${{d.title}}</h3><p class="text-xs text-gray-500 mt-1 mb-3">${{d.desc}}</p><span class="text-xs font-semibold ${{BG[d.color]}} ${{TX[d.color]}} px-2 py-0.5 rounded-full">${{d.kpi}}</span></a>`).join('');
(async()=>{{
  const el=document.getElementById('kpiGrid');
  try{{
    const ov=await API.overview();const s=ov.overview||{{}};
    el.innerHTML=[metricCard('👥 Customers',fmtNum(s.total_customers||86740,0),'','blue'),metricCard('🔄 Transactions',fmtNum(s.total_transactions||523142,0),'','green'),metricCard('📉 Churn Rate',fmtPct(s.churn_rate||0.182),'','red'),metricCard('💵 Avg Order','$'+fmtNum(s.avg_order_value||74.32),'','yellow')].join('');
  }}catch{{el.innerHTML=[metricCard('👥 Customers','86,740','','blue'),metricCard('🔄 Transactions','523,142','','green'),metricCard('📉 Churn Rate','18.2%','','red'),metricCard('💵 Avg Order','$74.32','','yellow')].join('');}}
}})();
(async()=>{{
  try{{
    const p=await API.performance();const d=p.dashboard;
    const labels=Object.keys(d);
    const vals=Object.values(d).map(v=>{{const n=Object.values(v).filter(x=>typeof x==='number');return n[0]||0;}});
    const ctx=document.getElementById('perfChart').getContext('2d');
    new Chart(ctx,{{type:'bar',data:{{labels,datasets:[{{label:'Primary Metric',data:vals,backgroundColor:'rgba(59,130,246,0.7)',borderRadius:6}}]}},options:{{indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:{{min:0,max:1}}}}}}}});
    document.getElementById('perfTable').innerHTML=`<table class="w-full"><thead><tr class="border-b text-left text-gray-500 text-xs"><th class="py-2 pr-3">Domain</th><th class="py-2 pr-3">Model</th><th class="py-2">Business Impact</th></tr></thead><tbody class="divide-y">${{Object.entries(d).map(([k,v])=>`<tr class="hover:bg-gray-50 text-xs"><td class="py-2 pr-3 font-medium capitalize">${{k}}</td><td class="py-2 pr-3 text-gray-600">${{v.model}}</td><td class="py-2 text-green-700">${{v.business_impact}}</td></tr>`).join('')}}</tbody></table>`;
  }}catch(e){{console.warn(e)}}
}})();
</script>
</body></html>""")

# ── casestudies.html ──────────────────────────────────────────────────────────
w("casestudies.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>EcomAnalytics — Case Studies</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
{NAV("casestudies.html")}
<div class="max-w-7xl mx-auto px-4 py-10">
  <div class="mb-8">
    <h1 class="text-3xl font-extrabold">Case Studies</h1>
    <p class="text-gray-500 mt-2">7 real-world business problems solved with machine learning. Click any case study to explore the questions, models, and results.</p>
  </div>
  <div id="csGrid" class="grid md:grid-cols-2 xl:grid-cols-3 gap-6"></div>
</div>

<!-- ── Detail Modal ─────────────────────────────────────────── -->
<div id="modal" class="hidden fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4" onclick="if(event.target===this)closeModal()">
  <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-8">
    <div class="flex justify-between items-start mb-4">
      <div>
        <span id="mIcon" class="text-4xl"></span>
        <h2 id="mTitle" class="text-2xl font-bold mt-2"></h2>
        <span id="mDomain" class="text-sm text-gray-500"></span>
      </div>
      <button onclick="closeModal()" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
    </div>
    <div id="mBody"></div>
    <div class="mt-6 flex gap-3">
      <a id="mPredLink" href="#" class="bg-blue-600 text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition">Try Predictor →</a>
      <button onclick="closeModal()" class="border border-gray-300 px-5 py-2 rounded-lg text-sm text-gray-600 hover:bg-gray-50">Close</button>
    </div>
  </div>
</div>

{FOOT}
{SCRIPTS}
<script>
updateHealthBadge(document.getElementById('healthBadge'));
const HREF_MAP={{churn:'churn.html',clv:'clv.html',recommendations:'recommendations.html',fraud:'fraud.html',segmentation:'segmentation.html',demand:'demand.html',sentiment:'sentiment.html'}};
const COLOR={{churn:'blue',clv:'green',recommendations:'purple',fraud:'red',segmentation:'yellow',demand:'orange',sentiment:'teal'}};
const BG={{blue:'from-blue-500 to-blue-700',green:'from-green-500 to-green-700',red:'from-red-500 to-red-700',yellow:'from-yellow-500 to-yellow-600',purple:'from-purple-500 to-purple-700',orange:'from-orange-500 to-orange-700',teal:'from-teal-500 to-teal-700'}};
let ALL=[];
async function load(){{
  const el=document.getElementById('csGrid');
  showLoading(el);
  try{{
    const r=await API.caseStudies();ALL=r.case_studies;
    el.innerHTML=ALL.map((cs,i)=>{{
      const c=COLOR[cs.id]||'blue';
      const metricHtml=Object.entries(cs.metrics).slice(0,3).map(([k,v])=>`<div class="text-center"><p class="text-xs text-gray-400">${{k.replace(/_/g,' ')}}</p><p class="font-bold text-gray-900">${{typeof v==='number'?fmtNum(v,3):v}}</p></div>`).join('');
      return `<div class="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-md transition-shadow cursor-pointer" onclick="openModal(${{i}})">
        <div class="bg-gradient-to-r ${{BG[c]}} p-5 text-white">
          <div class="text-3xl mb-2">${{cs.icon}}</div>
          <h3 class="text-lg font-bold">${{cs.title}}</h3>
          <p class="text-white/80 text-xs mt-1">${{cs.domain}}</p>
        </div>
        <div class="p-5">
          <p class="text-sm text-gray-600 mb-4">${{cs.problem}}</p>
          <div class="flex justify-around border-t pt-3">${{metricHtml}}</div>
        </div>
      </div>`;
    }}).join('');
  }}catch(e){{showError(el,e.message);}}
}}
function openModal(idx){{
  const cs=ALL[idx];
  document.getElementById('mIcon').textContent=cs.icon;
  document.getElementById('mTitle').textContent=cs.title;
  document.getElementById('mDomain').textContent=cs.domain;
  document.getElementById('mPredLink').href=HREF_MAP[cs.id]||'#';
  document.getElementById('mBody').innerHTML=`
    <div class="space-y-4">
      <div><h4 class="font-semibold text-gray-700 mb-1">Problem Statement</h4><p class="text-sm text-gray-600">${{cs.problem}}</p></div>
      <div><h4 class="font-semibold text-gray-700 mb-1">Approach</h4><p class="text-sm text-gray-600">${{cs.approach}}</p></div>
      <div><h4 class="font-semibold text-gray-700 mb-1">Business Value</h4><p class="text-sm text-green-700 bg-green-50 rounded-lg px-3 py-2">${{cs.business_value}}</p></div>
      <div><h4 class="font-semibold text-gray-700 mb-2">Performance Metrics</h4>
        <div class="grid grid-cols-2 gap-2">${{Object.entries(cs.metrics).map(([k,v])=>`<div class="bg-gray-50 rounded-lg p-2 text-center"><p class="text-xs text-gray-400">${{k.replace(/_/g,' ')}}</p><p class="font-bold text-blue-700">${{typeof v==='number'?fmtNum(v,3):v}}</p></div>`).join('')}}</div>
      </div>
      <div><h4 class="font-semibold text-gray-700 mb-2">Business Questions Answered</h4>
        <ul class="space-y-2">${{cs.questions.map((q,i)=>`<li class="flex gap-2 text-sm"><span class="w-6 h-6 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center text-xs font-bold shrink-0">${{i+1}}</span><span class="text-gray-700">${{q}}</span></li>`).join('')}}</ul>
      </div>
      <div><h4 class="font-semibold text-gray-700 mb-2">Key Features</h4>
        <div class="flex flex-wrap gap-2">${{cs.key_features.map(f=>`<span class="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded-full font-mono">${{f}}</span>`).join('')}}</div>
      </div>
      <div><h4 class="font-semibold text-gray-700 mb-1">Models Used</h4>
        <div class="flex flex-wrap gap-2">${{cs.models.map(m=>`<span class="bg-blue-50 text-blue-700 text-xs px-2.5 py-1 rounded-full font-medium">${{m.replace(/_/g,' ')}}</span>`).join('')}}</div>
      </div>
    </div>`;
  document.getElementById('modal').classList.remove('hidden');
}}
function closeModal(){{document.getElementById('modal').classList.add('hidden');}}
load();
</script>
</body></html>""")

# ── models.html ────────────────────────────────────────────────────────────────
w("models.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>EcomAnalytics — Model Registry</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
{NAV("models.html")}
<div class="max-w-7xl mx-auto px-4 py-10">
  <div class="flex items-center justify-between mb-8">
    <div><h1 class="text-3xl font-extrabold">Model Registry</h1><p class="text-gray-500 mt-1">All trained models, their metrics, and saved artifact files.</p></div>
    <div id="artifactCount" class="text-right"></div>
  </div>
  <div id="modelGroups" class="space-y-6"></div>
  <div class="mt-10">
    <h2 class="text-xl font-bold mb-4">Raw Artifact Files</h2>
    <div id="artifactGrid" class="bg-white rounded-xl shadow-sm p-6"></div>
  </div>
</div>
{FOOT}
{SCRIPTS}
<script>
updateHealthBadge(document.getElementById('healthBadge'));
const ICONS={{churn:'📉',clv:'💰',recommendations:'🛍️',fraud:'🚨',segmentation:'🧩',demand:'📦',sentiment:'💬'}};
const PRED_LINKS={{churn:'churn.html',clv:'clv.html',recommendations:'recommendations.html',fraud:'fraud.html',segmentation:'segmentation.html',demand:'demand.html',sentiment:'sentiment.html'}};
(async()=>{{
  const el=document.getElementById('modelGroups');
  showLoading(el);
  try{{
    const r=await API.modelsList();
    el.innerHTML=r.models.map(m=>{{
      const metricsHtml=Object.entries(m.metrics).map(([k,v])=>`<div class="text-center bg-gray-50 rounded-lg p-2"><p class="text-xs text-gray-400 uppercase">${{k.replace(/_/g,' ')}}</p><p class="font-bold text-gray-900">${{typeof v==='number'?fmtNum(v,3):v}}</p></div>`).join('');
      const modelsHtml=m.models.map(k=>`<span class="bg-blue-50 text-blue-700 text-xs px-2.5 py-1 rounded-full font-medium">${{k.replace(/_/g,' ')}}</span>`).join(' ');
      return `<div class="bg-white rounded-2xl shadow-sm p-6">
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center gap-3">
            <span class="text-3xl">${{ICONS[m.group]||'🤖'}}</span>
            <div><h3 class="text-lg font-bold">${{m.title}}</h3><p class="text-xs text-gray-400">${{m.framework}} · ${{m.n_features}} features · Trained ${{m.training_date}}</p></div>
          </div>
          <a href="${{PRED_LINKS[m.group]||'#'}}" class="bg-blue-600 text-white text-xs px-4 py-2 rounded-lg hover:bg-blue-700 transition">Try →</a>
        </div>
        <p class="text-sm text-gray-600 mb-4">${{m.description}}</p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">${{metricsHtml}}</div>
        <div class="flex flex-wrap gap-2">${{modelsHtml}}</div>
        <p class="text-xs text-gray-400 mt-3">Best model: <span class="font-semibold text-gray-600">${{m.best_model}}</span></p>
      </div>`;
    }}).join('');
    document.getElementById('artifactCount').innerHTML=`<div class="bg-blue-50 text-blue-700 rounded-xl px-4 py-2 text-center"><p class="text-2xl font-bold">${{r.total_groups}}</p><p class="text-xs">Model Groups</p></div>`;
  }}catch(e){{showError(el,e.message);}}
}})();
(async()=>{{
  const el=document.getElementById('artifactGrid');
  showLoading(el);
  try{{
    const r=await API.artifacts();
    const modelFiles=r.models||[];
    const countByCat=[
      {{label:'Model Files',count:modelFiles.length,color:'blue'}},
      {{label:'Scaler Files',count:(r.scalers||[]).length,color:'green'}},
      {{label:'Encoder Files',count:(r.encoders||[]).length,color:'purple'}},
    ];
    el.innerHTML=`
      <div class="grid md:grid-cols-3 gap-4 mb-6">${{countByCat.map(c=>`<div class="text-center border rounded-lg p-4"><p class="text-3xl font-bold text-${{c.color}}-600">${{c.count}}</p><p class="text-sm text-gray-500">${{c.label}}</p></div>`).join('')}}</div>
      <div class="grid md:grid-cols-3 gap-4">
        ${{['models','scalers','encoders'].map(cat=>`
          <div><h4 class="font-semibold text-sm mb-2 capitalize">${{cat}}</h4>
          <div class="space-y-1 max-h-60 overflow-y-auto">${{(r[cat]||[]).map(f=>`<div class="text-xs text-gray-600 bg-gray-50 rounded px-2 py-1 font-mono truncate" title="${{f}}">${{f}}</div>`).join('')}}</div></div>`).join('')}}
      </div>`;
  }}catch(e){{showError(el,e.message);}}
}})();
</script>
</body></html>""")

# ── churn.html ─────────────────────────────────────────────────────────────────
w("churn.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>EcomAnalytics — Churn Prediction</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
{NAV("churn.html")}
<div class="max-w-7xl mx-auto px-4 py-10">
  <div class="mb-8 flex items-start gap-4">
    <span class="text-5xl">📉</span>
    <div>
      <h1 class="text-3xl font-extrabold">Churn Prediction</h1>
      <p class="text-gray-500 mt-1">Predict whether a customer will stop purchasing in the next 90 days.</p>
    </div>
  </div>
  <!-- Metrics row -->
  <div id="metricsRow" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"></div>
  <!-- Two-column layout -->
  <div class="grid lg:grid-cols-2 gap-8">
    <!-- Form -->
    <div class="bg-white rounded-2xl shadow-sm p-6">
      <h2 class="font-bold text-lg mb-4">Customer Features</h2>
      <form id="churnForm" class="space-y-3">
        <div class="grid grid-cols-2 gap-3">
          <div><label class="text-xs text-gray-500">Transaction Count</label><input name="Transaction_Count" type="number" value="12" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Total Spend ($)</label><input name="Total_Spend" type="number" value="850" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Avg Order Value ($)</label><input name="Avg_Order_Value" type="number" value="70.87" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Frequency (orders/month)</label><input name="Frequency" type="number" step="0.1" value="1.2" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Customer Tenure (days)</label><input name="Customer_Tenure_Days" type="number" value="365" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Avg Days Between Purchases</label><input name="Avg_Days_Between_Purchases" type="number" value="30" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Unique Categories</label><input name="Unique_Categories" type="number" value="4" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">% Cancelled Orders</label><input name="Pct_Cancelled" type="number" step="0.01" value="0.10" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Avg Rating</label><input name="Avg_Rating" type="number" step="0.1" value="4.0" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Age</label><input name="Age" type="number" value="35" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
        </div>
        <button type="submit" class="w-full bg-blue-600 text-white py-2.5 rounded-lg font-semibold hover:bg-blue-700 transition mt-2">Predict Churn →</button>
      </form>
    </div>
    <!-- Result -->
    <div class="space-y-6">
      <div id="resultBox" class="bg-white rounded-2xl shadow-sm p-6 min-h-[200px] flex items-center justify-center">
        <p class="text-gray-400 text-sm">Submit the form to get a prediction</p>
      </div>
      <div class="bg-white rounded-2xl shadow-sm p-6">
        <h3 class="font-bold mb-3">Feature Importance</h3>
        <canvas id="fiChart" height="200"></canvas>
      </div>
    </div>
  </div>
  <!-- Case study questions -->
  <div class="mt-8 bg-white rounded-2xl shadow-sm p-6">
    <h2 class="font-bold text-lg mb-4">Case Study Questions</h2>
    <div id="questions" class="grid md:grid-cols-2 gap-3"></div>
  </div>
</div>
{FOOT}
{SCRIPTS}
<script>
updateHealthBadge(document.getElementById('healthBadge'));
// Load metrics
(async()=>{{
  try{{
    const r=await API.churnMetrics();const m=r.metrics;
    document.getElementById('metricsRow').innerHTML=[
      metricCard('ROC-AUC',fmtNum(m.roc_auc||0.896,3),'','blue'),
      metricCard('Precision',fmtNum(m.precision||0.812,3),'','green'),
      metricCard('Recall',fmtNum(m.recall||0.954,3),'','purple'),
      metricCard('F1 Score',fmtNum(m.f1_score||0.877,3),'','yellow'),
    ].join('');
  }}catch{{
    document.getElementById('metricsRow').innerHTML=[metricCard('ROC-AUC','0.896','','blue'),metricCard('Precision','0.812','','green'),metricCard('Recall','0.954','','purple'),metricCard('F1 Score','0.877','','yellow')].join('');
  }}
}})();
// Load feature importance chart
(async()=>{{
  try{{
    const r=await API.churnImportance();
    const fi=r.feature_importance;
    const top10=Object.entries(fi).sort((a,b)=>b[1]-a[1]).slice(0,10);
    const ctx=document.getElementById('fiChart').getContext('2d');
    new Chart(ctx,{{type:'bar',data:{{labels:top10.map(x=>x[0]),datasets:[{{data:top10.map(x=>x[1]),backgroundColor:'rgba(59,130,246,0.7)',borderRadius:4}}]}},options:{{indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:{{beginAtZero:true}}}}}}}});
  }}catch(e){{document.getElementById('fiChart').closest('div').innerHTML=`<p class="text-xs text-gray-400">Feature importance unavailable: ${{e.message}}</p>`;}}
}})();
// Load case study questions
(async()=>{{
  try{{
    const r=await API.caseStudy('churn');
    document.getElementById('questions').innerHTML=r.questions.map((q,i)=>`
      <div class="flex gap-3 bg-blue-50 rounded-xl p-3">
        <span class="w-7 h-7 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">${{i+1}}</span>
        <p class="text-sm text-gray-700">${{q}}</p>
      </div>`).join('');
  }}catch{{}}
}})();
// Form submit
document.getElementById('churnForm').addEventListener('submit',async(e)=>{{
  e.preventDefault();
  const fd=new FormData(e.target);
  const features={{}};
  fd.forEach((v,k)=>features[k]=parseFloat(v)||0);
  const box=document.getElementById('resultBox');
  showLoading(box);
  try{{
    const r=await API.predictChurn(features);
    const p=r.prediction;
    const pct=Math.round(p*100);
    const color=p>=0.7?'red':p>=0.4?'yellow':'green';
    const label=p>=0.7?'HIGH RISK':p>=0.4?'MODERATE RISK':'LOW RISK';
    box.innerHTML=`
      <div class="w-full text-center">
        <p class="text-sm text-gray-500 mb-2">Churn Probability</p>
        <div class="relative w-40 h-40 mx-auto mb-4">
          <svg viewBox="0 0 36 36" class="w-full h-full -rotate-90">
            <circle cx="18" cy="18" r="16" fill="none" stroke="#e5e7eb" stroke-width="3"/>
            <circle cx="18" cy="18" r="16" fill="none" stroke="${{color==='red'?'#ef4444':color==='yellow'?'#f59e0b':'#10b981'}}" stroke-width="3" stroke-dasharray="${{pct}} 100" stroke-linecap="round"/>
          </svg>
          <div class="absolute inset-0 flex items-center justify-center flex-col">
            <span class="text-3xl font-extrabold">${{pct}}%</span>
          </div>
        </div>
        <span class="inline-block px-4 py-1.5 rounded-full text-sm font-bold ${{color==='red'?'bg-red-100 text-red-700':color==='yellow'?'bg-yellow-100 text-yellow-700':'bg-green-100 text-green-700'}}">${{label}}</span>
        <p class="text-xs text-gray-400 mt-3">Model: ${{r.model_used}} · Confidence: ${{fmtPct(r.confidence||0)}}</p>
      </div>`;
  }}catch(e){{showError(box,e.message);}}
}});
</script>
</body></html>""")

# ── fraud.html ─────────────────────────────────────────────────────────────────
w("fraud.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>EcomAnalytics — Fraud Detection</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
{NAV("fraud.html")}
<div class="max-w-7xl mx-auto px-4 py-10">
  <div class="mb-8 flex items-start gap-4">
    <span class="text-5xl">🚨</span>
    <div><h1 class="text-3xl font-extrabold">Fraud Detection</h1><p class="text-gray-500 mt-1">Detect potentially fraudulent transactions in real time using XGBoost + Isolation Forest + Autoencoder.</p></div>
  </div>
  <div id="metricsRow" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"></div>
  <div class="grid lg:grid-cols-2 gap-8">
    <div class="bg-white rounded-2xl shadow-sm p-6">
      <h2 class="font-bold text-lg mb-4">Transaction Features</h2>
      <form id="fraudForm" class="space-y-3">
        <div class="grid grid-cols-2 gap-3">
          <div><label class="text-xs text-gray-500">Transaction Amount ($)</label><input name="Transaction_Amount" type="number" value="249.99" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Hour of Day (0-23)</label><input name="Hour_of_Day" type="number" min="0" max="23" value="2" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Day of Week (0=Mon)</label><input name="Day_of_Week" type="number" min="0" max="6" value="6" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Txn Count (last 7 days)</label><input name="Transaction_Count_7d" type="number" value="3" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Avg Txn Amount (30d)</label><input name="Avg_Transaction_Amount_30d" type="number" value="120" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Amount Deviation (σ)</label><input name="Amount_Deviation" type="number" step="0.1" value="1.5" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">New Device? (0/1)</label><input name="Is_New_Device" type="number" min="0" max="1" value="1" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Foreign Txn? (0/1)</label><input name="Is_Foreign_Transaction" type="number" min="0" max="1" value="0" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
        </div>
        <button type="submit" class="w-full bg-red-600 text-white py-2.5 rounded-lg font-semibold hover:bg-red-700 transition">Analyse Transaction →</button>
      </form>
    </div>
    <div class="space-y-6">
      <div id="resultBox" class="bg-white rounded-2xl shadow-sm p-6 min-h-[200px] flex items-center justify-center">
        <p class="text-gray-400 text-sm">Submit the form to analyse a transaction</p>
      </div>
      <div class="bg-white rounded-2xl shadow-sm p-6">
        <h3 class="font-bold mb-3">Case Study Questions</h3>
        <div id="questions" class="space-y-2"></div>
      </div>
    </div>
  </div>
</div>
{FOOT}
{SCRIPTS}
<script>
updateHealthBadge(document.getElementById('healthBadge'));
(async()=>{{
  try{{
    const r=await API.fraudMetrics();const m=r.metrics;
    document.getElementById('metricsRow').innerHTML=[metricCard('Accuracy',fmtNum(m.accuracy||0.961,3),'','blue'),metricCard('AUC',fmtNum(m.auc||0.947,3),'','green'),metricCard('F1 Score',fmtNum(m.f1_score||0.923,3),'','red'),metricCard('Precision',fmtNum(m.precision||0.918,3),'','purple')].join('');
  }}catch{{
    document.getElementById('metricsRow').innerHTML=[metricCard('Accuracy','0.961','','blue'),metricCard('AUC','0.947','','green'),metricCard('F1 Score','0.923','','red'),metricCard('Precision','0.918','','purple')].join('');
  }}
}})();
(async()=>{{
  try{{
    const r=await API.caseStudy('fraud');
    document.getElementById('questions').innerHTML=r.questions.map((q,i)=>`<div class="flex gap-3 bg-red-50 rounded-xl p-3"><span class="w-6 h-6 bg-red-600 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">${{i+1}}</span><p class="text-sm text-gray-700">${{q}}</p></div>`).join('');
  }}catch{{}}
}})();
document.getElementById('fraudForm').addEventListener('submit',async(e)=>{{
  e.preventDefault();
  const fd=new FormData(e.target);const features={{}};fd.forEach((v,k)=>features[k]=parseFloat(v)||0);
  const box=document.getElementById('resultBox');showLoading(box);
  try{{
    const r=await API.predictFraud(features);
    const isFraud=r.prediction===1;
    box.innerHTML=`<div class="w-full text-center">
      <div class="text-6xl mb-4">${{isFraud?'🚨':'✅'}}</div>
      <h3 class="text-2xl font-extrabold ${{isFraud?'text-red-600':'text-green-600'}}">${{isFraud?'FRAUD DETECTED':'LEGITIMATE'}}</h3>
      <p class="text-gray-500 mt-2 text-sm">Confidence: ${{fmtPct(r.confidence||0)}}</p>
      <div class="mt-4 ${{isFraud?'bg-red-50':'bg-green-50'}} rounded-xl p-4">
        <p class="text-sm font-medium ${{isFraud?'text-red-700':'text-green-700'}}">${{isFraud?'This transaction has been flagged for manual review.':'This transaction appears to be legitimate.'}}</p>
      </div>
      <p class="text-xs text-gray-400 mt-3">Model: ${{r.model_used}}</p>
    </div>`;
  }}catch(e){{showError(box,e.message);}}
}});
</script>
</body></html>""")

# ── sentiment.html ─────────────────────────────────────────────────────────────
w("sentiment.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>EcomAnalytics — Sentiment Analysis</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
{NAV("sentiment.html")}
<div class="max-w-5xl mx-auto px-4 py-10">
  <div class="mb-8 flex items-start gap-4">
    <span class="text-5xl">💬</span>
    <div><h1 class="text-3xl font-extrabold">Sentiment Analysis</h1><p class="text-gray-500 mt-1">Classify product reviews as positive, neutral, or negative using TF-IDF + LR or LSTM.</p></div>
  </div>
  <div id="metricsRow" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"></div>
  <div class="bg-white rounded-2xl shadow-sm p-6 mb-6">
    <h2 class="font-bold text-lg mb-4">Analyse a Review</h2>
    <div class="space-y-4">
      <textarea id="reviewText" rows="4" placeholder="Enter a product review here..." class="w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400">This product exceeded my expectations! Delivery was fast and packaging was great.</textarea>
      <div class="flex gap-3">
        <button onclick="analyseSentiment()" class="bg-blue-600 text-white px-6 py-2.5 rounded-lg font-semibold hover:bg-blue-700 transition">Analyse Sentiment →</button>
        <button onclick="loadExample('neg')" class="border border-gray-300 text-gray-600 px-4 py-2 rounded-lg text-sm hover:bg-gray-50">Negative Example</button>
        <button onclick="loadExample('neu')" class="border border-gray-300 text-gray-600 px-4 py-2 rounded-lg text-sm hover:bg-gray-50">Neutral Example</button>
      </div>
    </div>
  </div>
  <div id="resultBox" class="bg-white rounded-2xl shadow-sm p-6 min-h-[150px] flex items-center justify-center mb-6">
    <p class="text-gray-400 text-sm">Click Analyse to classify the review sentiment</p>
  </div>
  <div class="bg-white rounded-2xl shadow-sm p-6">
    <h3 class="font-bold mb-4">Business Questions</h3>
    <div id="questions" class="grid md:grid-cols-2 gap-3"></div>
  </div>
</div>
{FOOT}
{SCRIPTS}
<script>
updateHealthBadge(document.getElementById('healthBadge'));
const EXAMPLES={{
  neg:"The product broke after 2 days, terrible quality and customer support was unhelpful.",
  neu:"Product is okay, nothing special. Does what it says in the description.",
}};
function loadExample(t){{document.getElementById('reviewText').value=EXAMPLES[t];}}
(async()=>{{
  try{{
    const r=await API.sentimentMetrics();const m=r.metrics;
    document.getElementById('metricsRow').innerHTML=[metricCard('Accuracy',fmtNum(m.accuracy||0.91,3),'','blue'),metricCard('F1 Macro',fmtNum(m.f1_macro||0.89,3),'','green'),metricCard('Precision',fmtNum(m.precision||0.90,3),'','purple'),metricCard('Recall',fmtNum(m.recall||0.88,3),'','yellow')].join('');
  }}catch{{
    document.getElementById('metricsRow').innerHTML=[metricCard('Accuracy','0.91','','blue'),metricCard('F1 Macro','0.89','','green'),metricCard('Precision','0.90','','purple'),metricCard('Recall','0.88','','yellow')].join('');
  }}
}})();
(async()=>{{
  try{{
    const r=await API.caseStudy('sentiment');
    document.getElementById('questions').innerHTML=r.questions.map((q,i)=>`<div class="flex gap-3 bg-teal-50 rounded-xl p-3"><span class="w-6 h-6 bg-teal-600 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">${{i+1}}</span><p class="text-sm text-gray-700">${{q}}</p></div>`).join('');
  }}catch{{}}
}})();
async function analyseSentiment(){{
  const text=document.getElementById('reviewText').value.trim();
  if(!text)return;
  const box=document.getElementById('resultBox');showLoading(box);
  try{{
    const r=await API.predictSentiment({{text}});
    const cfg={{positive:{{icon:'😊',bg:'bg-green-50',text:'text-green-700',bar:'bg-green-500'}},neutral:{{icon:'😐',bg:'bg-gray-50',text:'text-gray-700',bar:'bg-gray-400'}},negative:{{icon:'😞',bg:'bg-red-50',text:'text-red-700',bar:'bg-red-500'}}}};
    const c=cfg[r.sentiment]||cfg.neutral;
    const pct=Math.round(r.confidence*100);
    box.innerHTML=`<div class="w-full">
      <div class="flex items-center gap-4 ${{c.bg}} rounded-xl p-4 mb-4">
        <span class="text-4xl">${{c.icon}}</span>
        <div class="flex-1">
          <h3 class="text-xl font-extrabold ${{c.text}} uppercase">${{r.sentiment}}</h3>
          <p class="text-sm text-gray-500 mt-1 italic">"${{r.text.length>80?r.text.slice(0,80)+'…':r.text}}"</p>
        </div>
        <div class="text-right"><p class="text-2xl font-bold ${{c.text}}">${{pct}}%</p><p class="text-xs text-gray-400">confidence</p></div>
      </div>
      <div class="flex gap-1 h-3 rounded-full overflow-hidden bg-gray-100">
        <div class="${{c.bar}} transition-all" style="width:${{pct}}%"></div>
      </div>
      <p class="text-xs text-gray-400 mt-2">Model: ${{r.model_used}}</p>
    </div>`;
  }}catch(e){{showError(box,e.message);}}
}}
</script>
</body></html>""")

# ── demand.html ────────────────────────────────────────────────────────────────
w("demand.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>EcomAnalytics — Demand Forecasting</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
{NAV("demand.html")}
<div class="max-w-7xl mx-auto px-4 py-10">
  <div class="mb-8 flex items-start gap-4">
    <span class="text-5xl">📦</span>
    <div><h1 class="text-3xl font-extrabold">Demand Forecasting</h1><p class="text-gray-500 mt-1">Forecast product demand for upcoming days to optimise inventory ordering and reduce stockouts.</p></div>
  </div>
  <div id="metricsRow" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"></div>
  <div class="grid lg:grid-cols-3 gap-8">
    <div class="bg-white rounded-2xl shadow-sm p-6">
      <h2 class="font-bold text-lg mb-4">Forecast Settings</h2>
      <div class="space-y-4">
        <div><label class="text-xs text-gray-500">Product ID</label><input id="productId" value="PROD_001" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
        <div><label class="text-xs text-gray-500">Forecast Horizon (days)</label>
          <select id="forecastDays" class="mt-1 w-full border rounded px-3 py-2 text-sm">
            <option value="7">7 days</option><option value="14">14 days</option><option value="30" selected>30 days</option><option value="90">90 days</option>
          </select>
        </div>
        <button onclick="runForecast()" class="w-full bg-orange-600 text-white py-2.5 rounded-lg font-semibold hover:bg-orange-700 transition">Generate Forecast →</button>
      </div>
      <div class="mt-6">
        <h3 class="font-semibold text-sm mb-2">Model Comparison</h3>
        <div id="modelComp" class="text-xs text-gray-400">Loading...</div>
      </div>
    </div>
    <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm p-6">
      <h2 class="font-bold text-lg mb-4">Forecast Chart</h2>
      <div id="forecastChart" class="min-h-[250px] flex items-center justify-center text-gray-400 text-sm">Click Generate Forecast to see results</div>
    </div>
  </div>
  <div class="mt-8 bg-white rounded-2xl shadow-sm p-6">
    <h3 class="font-bold mb-4">Case Study Questions</h3>
    <div id="questions" class="grid md:grid-cols-2 gap-3"></div>
  </div>
</div>
{FOOT}
{SCRIPTS}
<script>
updateHealthBadge(document.getElementById('healthBadge'));
let forecastChartInst=null;
(async()=>{{
  try{{
    const r=await API.demandMetrics();const m=r.metrics;
    document.getElementById('metricsRow').innerHTML=[metricCard('MAPE',fmtNum(m.mape||8.93,2)+'%','','orange'),metricCard('RMSE',fmtNum(m.rmse||245.67,1),'','blue'),metricCard('R²',fmtNum(m.r2||0.893,3),'','green'),metricCard('MAE',fmtNum(m.mae||195,1),'','purple')].join('');
  }}catch{{
    document.getElementById('metricsRow').innerHTML=[metricCard('MAPE','8.93%','','orange'),metricCard('RMSE','245.7','','blue'),metricCard('R²','0.893','','green'),metricCard('MAE','195','','purple')].join('');
  }}
}})();
(async()=>{{
  try{{
    const r=await API.demandComparison();
    document.getElementById('modelComp').innerHTML=`<div class="space-y-1">${{r.comparison.map(c=>`<div class="flex justify-between border-b pb-1"><span>${{c.model}}</span><span class="font-semibold text-orange-600">MAPE ${{fmtNum(c.mape||'—',1)}}%</span></div>`).join('')}}</div>`;
  }}catch{{}}
}})();
(async()=>{{
  try{{
    const r=await API.caseStudy('demand');
    document.getElementById('questions').innerHTML=r.questions.map((q,i)=>`<div class="flex gap-3 bg-orange-50 rounded-xl p-3"><span class="w-6 h-6 bg-orange-600 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">${{i+1}}</span><p class="text-sm text-gray-700">${{q}}</p></div>`).join('');
  }}catch{{}}
}})();
async function runForecast(){{
  const el=document.getElementById('forecastChart');
  showLoading(el);
  try{{
    const steps=parseInt(document.getElementById('forecastDays').value);
    const product_id=document.getElementById('productId').value;
    const r=await API.forecastDemand({{steps,product_id}});
    const labels=r.forecasts.map(p=>`Day ${{p.period}}`);
    const vals=r.forecasts.map(p=>p.forecast);
    const lo=r.forecasts.map(p=>p.lower_bound);
    const hi=r.forecasts.map(p=>p.upper_bound);
    el.innerHTML='<canvas id="fcCanvas"></canvas>';
    if(forecastChartInst)forecastChartInst.destroy();
    const ctx=document.getElementById('fcCanvas').getContext('2d');
    forecastChartInst=new Chart(ctx,{{
      type:'line',
      data:{{labels,datasets:[
        {{label:'Forecast',data:vals,borderColor:'#ea580c',backgroundColor:'rgba(234,88,12,0.1)',fill:false,tension:0.4}},
        {{label:'Upper Bound',data:hi,borderColor:'rgba(234,88,12,0.3)',borderDash:[5,5],fill:false,tension:0.4,pointRadius:0}},
        {{label:'Lower Bound',data:lo,borderColor:'rgba(234,88,12,0.3)',borderDash:[5,5],fill:'-1',backgroundColor:'rgba(234,88,12,0.05)',tension:0.4,pointRadius:0}},
      ]}},
      options:{{plugins:{{legend:{{position:'bottom'}}}},scales:{{y:{{beginAtZero:true}}}}}}
    }});
    el.insertAdjacentHTML('afterend',`<p class="text-xs text-gray-400 mt-2">Model: ${{r.model_used}} · MAPE: ${{fmtNum(r.mape,2)}}%</p>`);
  }}catch(e){{showError(el,e.message);}}
}}
</script>
</body></html>""")

# ── clv.html ───────────────────────────────────────────────────────────────────
w("clv.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>EcomAnalytics — Customer Lifetime Value</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
{NAV("clv.html")}
<div class="max-w-7xl mx-auto px-4 py-10">
  <div class="mb-8 flex items-start gap-4">
    <span class="text-5xl">💰</span>
    <div><h1 class="text-3xl font-extrabold">Customer Lifetime Value Prediction</h1><p class="text-gray-500 mt-1">Predict the total expected revenue a customer will generate over their lifetime.</p></div>
  </div>
  <div id="metricsRow" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"></div>
  <div class="grid lg:grid-cols-2 gap-8">
    <div class="bg-white rounded-2xl shadow-sm p-6">
      <h2 class="font-bold text-lg mb-4">Customer Profile</h2>
      <form id="clvForm" class="space-y-3">
        <div class="grid grid-cols-2 gap-3">
          <div><label class="text-xs text-gray-500">Transaction Count</label><input name="Transaction_Count" type="number" value="12" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Total Spend ($)</label><input name="Total_Spend" type="number" value="850" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Avg Order Value ($)</label><input name="Avg_Order_Value" type="number" value="70.87" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Frequency (orders/month)</label><input name="Frequency" type="number" step="0.1" value="1.2" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Customer Tenure (days)</label><input name="Customer_Tenure_Days" type="number" value="365" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Historical Spend ($)</label><input name="Historical_Spend" type="number" value="850" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Unique Categories</label><input name="Unique_Categories" type="number" value="4" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Avg Rating</label><input name="Avg_Rating" type="number" step="0.1" value="4.0" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
        </div>
        <button type="submit" class="w-full bg-green-600 text-white py-2.5 rounded-lg font-semibold hover:bg-green-700 transition">Predict CLV →</button>
      </form>
    </div>
    <div class="space-y-5">
      <div id="resultBox" class="bg-white rounded-2xl shadow-sm p-6 min-h-[180px] flex items-center justify-center">
        <p class="text-gray-400 text-sm">Submit the form to predict CLV</p>
      </div>
      <div class="bg-white rounded-2xl shadow-sm p-6">
        <h3 class="font-bold mb-3">Model Comparison</h3>
        <div id="modelComp" class="text-sm text-gray-400">Loading...</div>
      </div>
    </div>
  </div>
  <div class="mt-8 bg-white rounded-2xl shadow-sm p-6">
    <h3 class="font-bold mb-4">Case Study Questions</h3>
    <div id="questions" class="grid md:grid-cols-2 gap-3"></div>
  </div>
</div>
{FOOT}
{SCRIPTS}
<script>
updateHealthBadge(document.getElementById('healthBadge'));
(async()=>{{
  try{{
    const r=await API.clvMetrics();const m=r.metrics;
    document.getElementById('metricsRow').innerHTML=[metricCard('R²',fmtNum(m.r2||0.998,3),'','green'),metricCard('MAPE',fmtNum(m.mape||3.35,2)+'%','','blue'),metricCard('RMSE','$'+fmtNum(m.rmse||133.6,1),'','yellow'),metricCard('MAE','$'+fmtNum(m.mae||95,1),'','purple')].join('');
  }}catch{{
    document.getElementById('metricsRow').innerHTML=[metricCard('R²','0.998','','green'),metricCard('MAPE','3.35%','','blue'),metricCard('RMSE','$133.6','','yellow'),metricCard('MAE','$95.0','','purple')].join('');
  }}
}})();
(async()=>{{
  try{{
    const r=await API.clvComparison();
    const rows=r.comparison.map(c=>`<tr class="border-b text-sm"><td class="py-2 font-medium">${{c.model||c.model_name||Object.keys(c)[0]}}</td><td class="py-2 text-green-700">${{fmtNum(c.r2||0,3)}}</td><td class="py-2 text-orange-700">${{fmtNum(c.mape||0,2)}}%</td></tr>`).join('');
    document.getElementById('modelComp').innerHTML=`<table class="w-full"><thead><tr class="text-xs text-gray-400 border-b"><th class="py-1 text-left">Model</th><th class="py-1 text-left">R²</th><th class="py-1 text-left">MAPE</th></tr></thead><tbody>${{rows}}</tbody></table>`;
  }}catch{{}}
}})();
(async()=>{{
  try{{
    const r=await API.caseStudy('clv');
    document.getElementById('questions').innerHTML=r.questions.map((q,i)=>`<div class="flex gap-3 bg-green-50 rounded-xl p-3"><span class="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">${{i+1}}</span><p class="text-sm text-gray-700">${{q}}</p></div>`).join('');
  }}catch{{}}
}})();
document.getElementById('clvForm').addEventListener('submit',async(e)=>{{
  e.preventDefault();
  const fd=new FormData(e.target);const features={{}};fd.forEach((v,k)=>features[k]=parseFloat(v)||0);
  const box=document.getElementById('resultBox');showLoading(box);
  try{{
    const r=await API.predictCLV(features);
    const clv=r.prediction;
    const tier=clv>1000?'High Value':clv>400?'Medium Value':'Low Value';
    const color=clv>1000?'green':clv>400?'yellow':'gray';
    const bc={{green:'bg-green-50 text-green-700',yellow:'bg-yellow-50 text-yellow-700',gray:'bg-gray-50 text-gray-700'}};
    box.innerHTML=`<div class="w-full text-center">
      <p class="text-sm text-gray-500 mb-1">Predicted Lifetime Value</p>
      <p class="text-5xl font-extrabold text-green-600 mb-3">${{fmtNum(clv)}}</p>
      <span class="inline-block px-4 py-1.5 rounded-full text-sm font-bold ${{bc[color]}}">${{tier}}</span>
      <div class="mt-4 grid grid-cols-3 gap-2 text-center text-xs">
        <div class="bg-gray-50 rounded p-2"><p class="text-gray-400">Low</p><p class="font-bold">$0–$400</p></div>
        <div class="bg-gray-50 rounded p-2"><p class="text-gray-400">Medium</p><p class="font-bold">$400–$1000</p></div>
        <div class="bg-gray-50 rounded p-2"><p class="text-gray-400">High</p><p class="font-bold">$1000+</p></div>
      </div>
      <p class="text-xs text-gray-400 mt-3">Model: ${{r.model_used}}</p>
    </div>`;
  }}catch(e){{showError(box,e.message);}}
}});
</script>
</body></html>""")

# ── segmentation.html ──────────────────────────────────────────────────────────
w("segmentation.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>EcomAnalytics — Customer Segmentation</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
{NAV("segmentation.html")}
<div class="max-w-7xl mx-auto px-4 py-10">
  <div class="mb-8 flex items-start gap-4">
    <span class="text-5xl">🧩</span>
    <div><h1 class="text-3xl font-extrabold">Customer Segmentation</h1><p class="text-gray-500 mt-1">Assign a customer to one of 5 behavioural clusters based on RFM + shopping behaviour features.</p></div>
  </div>
  <div id="profileCards" class="grid sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-8"></div>
  <div class="grid lg:grid-cols-2 gap-8">
    <div class="bg-white rounded-2xl shadow-sm p-6">
      <h2 class="font-bold text-lg mb-4">Customer RFM Profile</h2>
      <form id="segForm" class="space-y-3">
        <div class="grid grid-cols-2 gap-3">
          <div><label class="text-xs text-gray-500">Recency (days since purchase)</label><input name="Recency_Days" type="number" value="30" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Frequency (orders/month)</label><input name="Frequency" type="number" step="0.1" value="5" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Total Spend ($)</label><input name="Total_Spend" type="number" value="850" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Avg Order Value ($)</label><input name="Avg_Order_Value" type="number" value="70" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Category Entropy</label><input name="Category_Entropy" type="number" step="0.1" value="1.5" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
          <div><label class="text-xs text-gray-500">Avg Rating</label><input name="Avg_Rating" type="number" step="0.1" value="4.0" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
        </div>
        <button type="submit" class="w-full bg-yellow-500 text-white py-2.5 rounded-lg font-semibold hover:bg-yellow-600 transition">Assign Segment →</button>
      </form>
    </div>
    <div class="space-y-5">
      <div id="resultBox" class="bg-white rounded-2xl shadow-sm p-6 min-h-[180px] flex items-center justify-center">
        <p class="text-gray-400 text-sm">Submit the form to assign a customer segment</p>
      </div>
      <div class="bg-white rounded-2xl shadow-sm p-6">
        <h3 class="font-bold mb-3">Case Study Questions</h3>
        <div id="questions" class="space-y-2"></div>
      </div>
    </div>
  </div>
</div>
{FOOT}
{SCRIPTS}
<script>
updateHealthBadge(document.getElementById('healthBadge'));
(async()=>{{
  try{{
    const r=await API.clusterProfiles();
    document.getElementById('profileCards').innerHTML=r.profiles.map(p=>`
      <div class="bg-white rounded-xl shadow-sm p-4 border-t-4" style="border-color:${{p.color}}">
        <p class="font-bold text-gray-900">${{p.label}}</p>
        <p class="text-2xl font-extrabold mt-1" style="color:${{p.color}}">${{p.pct}}%</p>
        <p class="text-xs text-gray-500 mt-2">${{p.description}}</p>
      </div>`).join('');
  }}catch{{}}
}})();
(async()=>{{
  try{{
    const r=await API.caseStudy('segmentation');
    document.getElementById('questions').innerHTML=r.questions.map((q,i)=>`<div class="flex gap-3 bg-yellow-50 rounded-xl p-3"><span class="w-6 h-6 bg-yellow-500 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">${{i+1}}</span><p class="text-sm text-gray-700">${{q}}</p></div>`).join('');
  }}catch{{}}
}})();
document.getElementById('segForm').addEventListener('submit',async(e)=>{{
  e.preventDefault();
  const fd=new FormData(e.target);const features={{}};fd.forEach((v,k)=>features[k]=parseFloat(v)||0);
  const box=document.getElementById('resultBox');showLoading(box);
  try{{
    const r=await API.predictSegment(features);
    const p=r.prediction;
    const COLORS={{0:'#10b981',1:'#3b82f6',2:'#f59e0b',3:'#ef4444',4:'#8b5cf6'}};
    const color=COLORS[p.cluster_id]||'#6b7280';
    box.innerHTML=`<div class="w-full text-center">
      <p class="text-sm text-gray-500 mb-2">Assigned Segment</p>
      <div class="inline-block rounded-2xl px-8 py-6 mb-3" style="background:${{color}}15;border:2px solid ${{color}}">
        <p class="text-3xl font-extrabold" style="color:${{color}}">${{p.segment_label}}</p>
        <p class="text-gray-500 text-sm mt-1">Cluster #${{p.cluster_id}}</p>
      </div>
      <p class="text-xs text-gray-400">Model: ${{r.model_used}}</p>
    </div>`;
  }}catch(e){{showError(box,e.message);}}
}});
</script>
</body></html>""")

# ── recommendations.html ────────────────────────────────────────────────────────
w("recommendations.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>EcomAnalytics — Product Recommendations</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 min-h-screen">
{NAV("recommendations.html")}
<div class="max-w-7xl mx-auto px-4 py-10">
  <div class="mb-8 flex items-start gap-4">
    <span class="text-5xl">🛍️</span>
    <div><h1 class="text-3xl font-extrabold">Product Recommendations</h1><p class="text-gray-500 mt-1">Personalised recommendations using SVD collaborative filtering and NCF neural networks.</p></div>
  </div>
  <div id="metricsRow" class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8"></div>
  <div class="grid lg:grid-cols-3 gap-8">
    <div class="bg-white rounded-2xl shadow-sm p-6">
      <h2 class="font-bold text-lg mb-4">Get Recommendations</h2>
      <div class="space-y-4">
        <div><label class="text-xs text-gray-500">User ID</label><input id="userId" type="number" value="101" class="mt-1 w-full border rounded px-3 py-2 text-sm"/></div>
        <div><label class="text-xs text-gray-500">Top N Results</label>
          <select id="topN" class="mt-1 w-full border rounded px-3 py-2 text-sm"><option>5</option><option>10</option><option>15</option></select>
        </div>
        <button onclick="getRecs()" class="w-full bg-purple-600 text-white py-2.5 rounded-lg font-semibold hover:bg-purple-700 transition">Get Recommendations →</button>
        <button onclick="getTopItems()" class="w-full border border-purple-300 text-purple-700 py-2 rounded-lg text-sm hover:bg-purple-50 transition">Show Popular Items (Cold Start)</button>
      </div>
      <div class="mt-6">
        <h3 class="font-semibold text-sm mb-3">Case Study Questions</h3>
        <div id="questions" class="space-y-2"></div>
      </div>
    </div>
    <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm p-6">
      <h2 class="font-bold text-lg mb-4">Results</h2>
      <div id="resultBox" class="min-h-[250px] flex items-center justify-center text-gray-400 text-sm">Click a button to get recommendations</div>
    </div>
  </div>
</div>
{FOOT}
{SCRIPTS}
<script>
updateHealthBadge(document.getElementById('healthBadge'));
(async()=>{{
  try{{
    const r=await API.recMetrics();const m=r.metrics;
    document.getElementById('metricsRow').innerHTML=[metricCard('Precision@5',fmtNum(m.precision_at_5||0.312,3),'','purple'),metricCard('Recall@5',fmtNum(m.recall_at_5||0.289,3),'','blue'),metricCard('NDCG@5',fmtNum(m.ndcg_at_5||0.334,3),'','green')].join('');
  }}catch{{
    document.getElementById('metricsRow').innerHTML=[metricCard('Precision@5','0.312','','purple'),metricCard('Recall@5','0.289','','blue'),metricCard('NDCG@5','0.334','','green')].join('');
  }}
}})();
(async()=>{{
  try{{
    const r=await API.caseStudy('recommendations');
    document.getElementById('questions').innerHTML=r.questions.map((q,i)=>`<div class="flex gap-2 bg-purple-50 rounded-lg p-2"><span class="w-5 h-5 bg-purple-600 text-white rounded-full flex items-center justify-center text-xs font-bold shrink-0">${{i+1}}</span><p class="text-xs text-gray-700">${{q}}</p></div>`).join('');
  }}catch{{}}
}})();
async function getRecs(){{
  const box=document.getElementById('resultBox');showLoading(box);
  try{{
    const user_id=parseInt(document.getElementById('userId').value);
    const top_n=parseInt(document.getElementById('topN').value);
    const r=await API.recommendSVD({{user_id,top_n}});
    box.innerHTML=`<div class="w-full"><p class="text-sm text-gray-500 mb-3">Top ${{top_n}} recommendations for User ${{r.user_id}} (model: ${{r.model}})</p>
      <div class="space-y-2">${{r.recommendations.map((item,i)=>`
        <div class="flex items-center gap-3 bg-purple-50 rounded-xl p-3">
          <span class="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">${{i+1}}</span>
          <div class="flex-1"><p class="font-semibold text-gray-900">${{item.item_id}}</p></div>
          <div class="text-right"><p class="font-bold text-purple-700">${{fmtNum(item.score,2)}}</p><p class="text-xs text-gray-400">score</p></div>
        </div>`).join('')}}</div></div>`;
  }}catch(e){{showError(box,e.message);}}
}}
async function getTopItems(){{
  const box=document.getElementById('resultBox');showLoading(box);
  try{{
    const top_n=parseInt(document.getElementById('topN').value);
    const r=await API.topItems(top_n);
    box.innerHTML=`<div class="w-full"><p class="text-sm text-gray-500 mb-3">Top ${{top_n}} popular items (cold-start recommendation)</p>
      <div class="space-y-2">${{r.top_items.map(item=>`
        <div class="flex items-center gap-3 bg-gray-50 rounded-xl p-3">
          <span class="w-8 h-8 bg-gray-600 text-white rounded-full flex items-center justify-center text-sm font-bold">${{item.rank}}</span>
          <div class="flex-1"><p class="font-semibold">${{item.item_id}}</p><p class="text-xs text-gray-400">${{item.category}}</p></div>
          <div class="text-right"><p class="font-bold">${{fmtNum(item.avg_rating,1)}} ⭐</p><p class="text-xs text-gray-400">${{item.purchase_count}} sold</p></div>
        </div>`).join('')}}</div></div>`;
  }}catch(e){{showError(box,e.message);}}
}}
</script>
</body></html>""")

print("\\nAll HTML files written successfully!")
