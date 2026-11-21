"""
GOLD-X 3.0 — واجهة المستخدم النهائية
تصميم بتدرجات لونية واضحة وخطوط مقروءة
"""
import streamlit as st
import plotly.graph_objects as go
from data_fetcher import fetch_all_data
from model import gold_x_model

# ═══════════════════════════════════════════════════
# إعدادات الصفحة والتنسيق
# ═══════════════════════════════════════════════════
st.set_page_config(
    page_title="GOLD-X 3.0 | نظام توقع الذهب",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص للتصميم الاحترافي
st.markdown("""
<style>
    /* الخط الأساسي */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', 'Segoe UI', sans-serif;
        direction: rtl;
    }
    
    /* العنوان الرئيسي بتدرج ذهبي */
    .main-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 50%, #FF8C00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .subtitle {
        text-align: center;
        color: #B0B8D4;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* بطاقات المؤشرات */
    .metric-card {
        background: linear-gradient(135deg, #151A3A 0%, #1E2545 100%);
        border: 1px solid #2A3463;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #FFD700;
    }
    .metric-label {
        color: #8892B0;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 900;
    }
    .metric-delta-pos { color: #00E676; font-size: 1rem; font-weight: 700; }
    .metric-delta-neg { color: #FF5252; font-size: 1rem; font-weight: 700; }
    
    /* بطاقة التوصية */
    .recommendation-card {
        background: linear-gradient(135deg, #1a1f3a 0%, #0f1429 100%);
        border-right: 6px solid #FFD700;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin: 1rem 0;
        font-size: 1.3rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    /* حالة السوق */
    .regime-normal { 
        background: linear-gradient(90deg, #00C853 0%, #00E676 100%);
        padding: 0.8rem 1.5rem; border-radius: 50px; 
        color: #000; font-weight: 900; display: inline-block;
    }
    .regime-stress { 
        background: linear-gradient(90deg, #FF9800 0%, #FFC107 100%);
        padding: 0.8rem 1.5rem; border-radius: 50px; 
        color: #000; font-weight: 900; display: inline-block;
    }
    .regime-crisis { 
        background: linear-gradient(90deg, #D32F2F 0%, #FF5252 100%);
        padding: 0.8rem 1.5rem; border-radius: 50px; 
        color: #FFF; font-weight: 900; display: inline-block;
    }
    
    /* الفواصل */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 2rem 0;
    }
    
    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0E27 0%, #151A3A 100%);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# العنوان
# ═══════════════════════════════════════════════════
st.markdown('<h1 class="main-title">🥇 GOLD-X 3.0</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">نظام متعدد الطبقات لتوقع أسعار الذهب | اقتصادي + تدفقات + AI + ركود تضخمي</p>', 
            unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# جلب البيانات
# ═══════════════════════════════════════════════════
with st.spinner("⏳ جاري جلب البيانات من المصادر..."):
    try:
        data = fetch_all_data()
    except Exception as e:
        st.error(f"❌ فشل جلب البيانات: {e}")
        st.stop()

# تشغيل النموذج
result = gold_x_model(data)

# ═══════════════════════════════════════════════════
# الصف الأول: المؤشرات الرئيسية
# ═══════════════════════════════════════════════════
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💰 السعر الحالي</div>
        <div class="metric-value">${data['current_price']:,.0f}</div>
        <div class="{'metric-delta-pos' if data['price_change'] >= 0 else 'metric-delta-neg'}">
            {data['price_change']*100:+.2f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    delta_class = 'metric-delta-pos' if result['change_pct'] >= 0 else 'metric-delta-neg'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🎯 السعر المتوقع</div>
        <div class="metric-value">${result['predicted_price']:,.0f}</div>
        <div class="{delta_class}">{result['change_pct']:+.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    conf = result['confidence']
    color = "#00E676" if conf > 6 else "#FFC107" if conf > 3 else "#FF5252"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💪 درجة الثقة</div>
        <div class="metric-value" style="color:{color}">{conf:.1f}/10</div>
        <div style="color:#8892B0;font-size:0.85rem">حسب النموذج</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    stag = result['stagflation_probability']
    color = "#00E676" if stag < 40 else "#FFC107" if stag < 70 else "#FF5252"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📊 الركود التضخمي</div>
        <div class="metric-value" style="color:{color}">{stag}%</div>
        <div style="color:#8892B0;font-size:0.85rem">احتمالية</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# الصف الثاني: حالة السوق والتوصية
# ═══════════════════════════════════════════════════
col_left, col_right = st.columns([1, 2])

with col_left:
    regime_map = {
        'normal': ('regime-normal', '🟢 NORMAL', 'السوق طبيعي'),
        'stress': ('regime-stress', '🟠 STRESS', 'توتر - حذر'),
        'crisis': ('regime-crisis', '🔴 CRISIS', 'أزمة - بيع قسري')
    }
    css_class, label, desc = regime_map[result['regime']]
    st.markdown(f"""
    <div style="text-align:center;padding:1rem 0;">
        <div style="color:#8892B0;font-size:0.9rem;margin-bottom:0.5rem">حالة السوق</div>
        <div class="{css_class}">{label}</div>
        <div style="color:#B0B8D4;margin-top:0.5rem;font-size:0.9rem">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown(f"""
    <div style="color:#8892B0;font-size:0.9rem;margin-bottom:0.5rem">التوصية النموذجية</div>
    <div class="recommendation-card">{result['recommendation']}</div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# الصف الثالث: رادار البيع القسري + الإنذارات
# ═══════════════════════════════════════════════════
col_radar, col_warn = st.columns(2)

with col_radar:
    st.markdown("### 📡 رادار البيع القسري")
    radar = result['radar']
    if radar['status'] == "CRITICAL":
        st.error(f"{radar['msg']}\n\n**الدرجة: {radar['score']}/10**")
    elif radar['status'] == "WARNING":
        st.warning(f"{radar['msg']}\n\n**الدرجة: {radar['score']}/10**")
    else:
        st.success(f"{radar['msg']}\n\n**الدرجة: {radar['score']}/10**")

with col_warn:
    st.markdown("### ⚠️ الإنذارات المبكرة")
    if result['warnings']:
        for w in result['warnings']:
            st.warning(w)
    else:
        st.success("✅ لا توجد إنذارات حالياً")

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# الصف الرابع: تفصيل العوامل (رسم بياني)
# ═══════════════════════════════════════════════════
st.markdown("### 🔍 تفصيل العوامل المؤثرة")

breakdown = result['breakdown']
fig = go.Figure(data=[go.Bar(
    x=['اقتصادي', 'تدفقات', 'ذكاء اصطناعي'],
    y=[breakdown['economic']*100, breakdown['flow']*100, breakdown['ai']*100],
    marker=dict(
        color=['#00E676', '#FF9800', '#2196F3'],
        line=dict(color='#FFFFFF', width=1)
    ),
    text=[f"{breakdown['economic']*100:.2f}%", 
          f"{breakdown['flow']*100:.2f}%", 
          f"{breakdown['ai']*100:.2f}%"],
    textposition='outside'
)])

fig.update_layout(
    template='plotly_dark',
    plot_bgcolor='rgba(10,14,39,0.9)',
    paper_bgcolor='rgba(10,14,39,0.9)',
    font=dict(family="Cairo", size=14, color='#FFFFFF'),
    yaxis_title="التأثير على السعر (%)",
    yaxis=dict(gridcolor='#2A3463'),
    xaxis=dict(gridcolor='#2A3463'),
    height=350,
    margin=dict(l=20, r=20, t=20, b=20)
)
st.plotly_chart(fig, use_container_width=True)

# أوزان النموذج
st.markdown("**⚖️ الأوزان الديناميكية حسب حالة السوق:**")
w = breakdown['weights']
st.markdown(f"""
- **النموذج الاقتصادي:** {w['economic']*100:.0f}%
- **نموذج التدفقات:** {w['flow']*100:.0f}%
- **نموذج الذكاء الاصطناعي:** {w['ai']*100:.0f}%
""")

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# الشريط الجانبي: مصادر البيانات + الإعدادات
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📚 مصادر البيانات")
    sources = data['sources']
    for key, label in [('gold','🥇 الذهب'), ('vix','📊 VIX'), 
                        ('dxy','💵 الدولار'), ('nasdaq','📈 ناسداك'),
                        ('treasury','🏛️ السندات')]:
        icon = "✅" if "احتياطي" not in sources[key] else "⚠️"
        st.markdown(f"{icon} **{label}:** {sources[key]}")
    
    st.markdown("---")
    st.markdown("## 📊 المؤشرات الحية")
    st.metric("VIX", f"{data['vix']:.2f}")
    st.metric("الدولار (DXY)", f"{data['dxy_value']:.2f}")
    st.metric("عائد 10 سنوات", f"{data['treasury_yield']:.2f}%")
    st.metric("ناسداك", f"{data['nasdaq_value']:,.0f}")
    st.metric("الارتباط بالأسهم", f"{data['gold_equity_corr']:.2f}")
    
    st.markdown("---")
    st.markdown("## 🔄 التحديث")
    if st.button("🔄 تحديث البيانات", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.caption("⏱️ يتم التحديث تلقائياً كل 5 دقائق")

# ═══════════════════════════════════════════════════
# التذييل
# ═══════════════════════════════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#8892B0;font-size:0.85rem;padding:1rem;">
    ⚠️ <strong>تنبيه:</strong> هذا النموذج أداة مساعدة للتفكير وليس نصيحة استثمارية.<br>
    GOLD-X 3.0 © 2026 | نموذج متعدد الطبقات
</div>
""", unsafe_allow_html=True)
