"""
GOLD-X 3.0 — المنصة الاستثمارية المتكاملة
يتضمن: النموذج + الأخبار + دليل المؤشرات
"""
import streamlit as st
import plotly.graph_objects as go
from data_fetcher import fetch_all_data
from model import gold_x_model
from news_fetcher import get_news, is_live, FEEDS


# ═══════════════════════════════════════════════════
# إعدادات الصفحة
# ═══════════════════════════════════════════════════
st.set_page_config(
    page_title="GOLD-X 3.0 | منصة توقع الذهب",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ═══════════════════════════════════════════════════
# CSS احترافي
# ═══════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', 'Segoe UI', sans-serif;
        direction: rtl;
    }
    
    .main-title {
        font-size: 3rem; font-weight: 900;
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
    .metric-label { color: #8892B0; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem; }
    .metric-value { color: #FFFFFF; font-size: 2rem; font-weight: 900; }
    .metric-delta-pos { color: #00E676; font-size: 1rem; font-weight: 700; }
    .metric-delta-neg { color: #FF5252; font-size: 1rem; font-weight: 700; }
    
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
    
    .regime-normal { background: linear-gradient(90deg, #00C853 0%, #00E676 100%);
        padding: 0.8rem 1.5rem; border-radius: 50px; color: #000; font-weight: 900; display: inline-block; }
    .regime-stress { background: linear-gradient(90deg, #FF9800 0%, #FFC107 100%);
        padding: 0.8rem 1.5rem; border-radius: 50px; color: #000; font-weight: 900; display: inline-block; }
    .regime-crisis { background: linear-gradient(90deg, #D32F2F 0%, #FF5252 100%);
        padding: 0.8rem 1.5rem; border-radius: 50px; color: #FFF; font-weight: 900; display: inline-block; }
    
    .news-card {
        background: linear-gradient(135deg, #151A3A 0%, #1E2545 100%);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        border-right: 4px solid #FFD700;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .news-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #FFD700;
        margin-bottom: 0.5rem;
    }
    .news-summary { color: #B0B8D4; font-size: 0.95rem; line-height: 1.6; }
    .news-date { color: #6B7BA8; font-size: 0.8rem; margin-top: 0.5rem; }
    
    .explainer-box {
        background: rgba(30, 37, 69, 0.6);
        border-right: 4px solid #2196F3;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        color: #B0B8D4;
        line-height: 1.7;
    }
    .explainer-box strong { color: #FFD700; }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
        margin: 2rem 0;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0E27 0%, #151A3A 100%);
    }
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        width: 85vw !important;
        min-width: 85vw !important;
    }
    section[data-testid="stSidebar"] * {
        writing-mode: horizontal-tb !important; /* لإصلاح النص العمودي */
        text-orientation: mixed !important;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# العنوان الرئيسي
# ═══════════════════════════════════════════════════
st.markdown('<h1 class="main-title">🥇 GOLD-X 3.0</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">منصة متكاملة لتوقع أسعار الذهب | نموذج + أخبار + تحليل</p>',
            unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# جلب البيانات
# ═══════════════════════════════════════════════════
with st.spinner("⏳ جاري جلب البيانات والأخبار..."):
    try:
        data = fetch_all_data()
    except Exception as e:
        st.error(f"❌ فشل جلب البيانات: {e}")
        st.stop()

result = gold_x_model(data)


# ═══════════════════════════════════════════════════
# التبويبات الرئيسية
# ═══════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 النموذج والتوقع",
    "🏛️ الفيدرالي",
    "🥇 مجلس الذهب العالمي",
    "📊 المحللون",
    "📈 أخبار الأسواق"
])


# ═════════════════════════════════════════════════════
# TAB 1: النموذج والتوقع
# ═════════════════════════════════════════════════════
with tab1:
    # ─── البطاقات الأربع ───
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 السعر الحالي</div>
            <div class="metric-value">${data['current_price']:,.0f}</div>
            <div class="{'metric-delta-pos' if data['price_change'] >= 0 else 'metric-delta-neg'}">
                {data['price_change']*100:+.2f}%
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        dc = 'metric-delta-pos' if result['change_pct'] >= 0 else 'metric-delta-neg'
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🎯 السعر المتوقع</div>
            <div class="metric-value">${result['predicted_price']:,.0f}</div>
            <div class="{dc}">{result['change_pct']:+.2f}%</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        conf = result['confidence']
        color = "#00E676" if conf > 6 else "#FFC107" if conf > 3 else "#FF5252"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💪 درجة الثقة</div>
            <div class="metric-value" style="color:{color}">{conf:.1f}/10</div>
            <div style="color:#8892B0;font-size:0.85rem">حسب النموذج</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        stag = result['stagflation_probability']
        color = "#00E676" if stag < 40 else "#FFC107" if stag < 70 else "#FF5252"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 الركود التضخمي</div>
            <div class="metric-value" style="color:{color}">{stag}%</div>
            <div style="color:#8892B0;font-size:0.85rem">احتمالية</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ─── حالة السوق والتوصية ───
    col_left, col_right = st.columns([1, 2])

    with col_left:
        regime_map = {
            'normal': ('regime-normal', '🟢 NORMAL', 'السوق طبيعي'),
            'stress': ('regime-stress', '🟠 STRESS', 'توتر - حذر'),
            'crisis': ('regime-crisis', '🔴 CRISIS', 'أزمة - بيع قسري')
        }
        css, label, desc = regime_map[result['regime']]
        st.markdown(f"""
        <div style="text-align:center;padding:1rem 0;">
            <div style="color:#8892B0;font-size:0.9rem;margin-bottom:0.5rem">حالة السوق</div>
            <div class="{css}">{label}</div>
            <div style="color:#B0B8D4;margin-top:0.5rem;font-size:0.9rem">{desc}</div>
        </div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
        <div style="color:#8892B0;font-size:0.9rem;margin-bottom:0.5rem">التوصية النموذجية</div>
        <div class="recommendation-card">{result['recommendation']}</div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ─── رادار + إنذارات ───
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

    # ─── مخطط العوامل ───
    st.markdown("### 🔍 تفصيل العوامل المؤثرة")
    bd = result['breakdown']
    fig = go.Figure(data=[go.Bar(
        x=['اقتصادي', 'تدفقات', 'ذكاء اصطناعي'],
        y=[bd['economic']*100, bd['flow']*100, bd['ai']*100],
        marker=dict(color=['#00E676', '#FF9800', '#2196F3'],
                    line=dict(color='#FFFFFF', width=1)),
        text=[f"{bd['economic']*100:.2f}%", f"{bd['flow']*100:.2f}%", f"{bd['ai']*100:.2f}%"],
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

    st.markdown("<hr>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════
    # دليل المؤشرات (التوضيحات)
    # ═══════════════════════════════════════════════════
    st.markdown("## 📚 دليل المؤشرات (ماذا تعني؟)")
    st.markdown("<p style='color:#B0B8D4;'>اضغط على أي مؤشر لقراءة شرحه</p>", unsafe_allow_html=True)

    # 1. عائد السندات
    with st.expander("🏛️ عائد السندات (10 سنوات) — القيمة الحالية: " + f"{data['treasury_yield']:.2f}%"):
        st.markdown(f"""
        <div class="explainer-box">
        <strong>ما هو؟</strong> هو العائد الذي تدفعه الحكومة الأمريكية لحاملي سنداتها لأجل 10 سنوات.<br><br>
        <strong>لماذا يهم الذهب؟</strong> الذهب لا يدر عائداً. عندما يرتفع عائد السندات، يصبح الاستثمار في السندات أكثر جاذبية، فيبيع المستثمرون الذهب لشراء السندات.<br><br>
        <strong>العلاقة:</strong> عكسية. كلما ارتفع العائد، انخفض الذهب (عادةً).<br><br>
        <strong>القيمة الحالية ({data['treasury_yield']:.2f}%):</strong> 
        {'⚠️ أعلى من 5% — منطقة ضغط شديد على الذهب' if data['treasury_yield'] > 5.0 else 
         '✅ أقل من 5% — ضغط معتدل' if data['treasury_yield'] > 4.0 else 
         '🟢 منخفض — داعم للذهب'}
        </div>
        """, unsafe_allow_html=True)

    # 2. الدولار
    with st.expander("💵 مؤشر الدولار (DXY) — القيمة الحالية: " + f"{data['dxy_value']:.2f}"):
        st.markdown(f"""
        <div class="explainer-box">
        <strong>ما هو؟</strong> مؤشر يقيس قوة الدولار الأمريكي مقابل سلة من العملات الرئيسية (يورو، ين، جنيه، إلخ).<br><br>
        <strong>لماذا يهم الذهب؟</strong> الذهب مسعّر بالدولار. عندما يقوى الدولار، يصبح الذهب أكثر تكلفة لحاملي العملات الأخرى، فينخفض الطلب.<br><br>
        <strong>العلاقة:</strong> عكسية. ارتفاع الدولار = ضغط على الذهب.<br><br>
        <strong>التغير في 5 أيام:</strong> {data['dxy_change']*100:+.2f}% 
        {'⚠️ الدولار يقوى — ضغط على الذهب' if data['dxy_change'] > 0 else '🟢 الدولار يضعف — داعم للذهب'}
        </div>
        """, unsafe_allow_html=True)

    # 3. VIX
    with st.expander("📊 مؤشر الخوف (VIX) — القيمة الحالية: " + f"{data['vix']:.2f}"):
        st.markdown(f"""
        <div class="explainer-box">
        <strong>ما هو؟</strong> مؤشر يقيس تقلبات السوق المتوقعة. كلما ارتفع، زاد الخوف في الأسواق.<br><br>
        <strong>لماذا يهم الذهب؟</strong> عادةً، ارتفاع VIX يدعم الذهب كملاذ آمن. لكن إذا ارتفع بشدة (فوق 35)، فقد يبيع المستثمرون كل شيء (بما فيه الذهب) لتوفير سيولة.<br><br>
        <strong>القيم:</strong><br>
        • 0-15: هدوء شديد (قد يكون مؤقتاً)<br>
        • 15-25: طبيعي<br>
        • 25-35: توتر<br>
        • 35+: ذعر (خطر بيع قسري)<br><br>
        <strong>القيمة الحالية ({data['vix']:.2f}):</strong> 
        {'🔴 ذعر — خطر بيع قسري' if data['vix'] > 35 else 
         '🟠 توتر — حذر' if data['vix'] > 25 else 
         '🟢 طبيعي'}
        </div>
        """, unsafe_allow_html=True)

    # 4. الارتباط بالأسهم
    with st.expander("🔗 ارتباط الذهب بالأسهم — القيمة الحالية: " + f"{data['gold_equity_corr']:.2f}"):
        st.markdown(f"""
        <div class="explainer-box">
        <strong>ما هو؟</strong> يقيس كيف يتحرك الذهب مع أسهم التكنولوجيا (ناسداك). يتراوح بين -1 و +1.<br><br>
        <strong>لماذا يهم؟</strong><br>
        • <strong>ارتباط منخفض (&lt; 0.2):</strong> الذهب يتحرك مستقلاً — هذا هو الوضع الطبيعي (ملاذ آمن حقيقي).<br>
        • <strong>ارتباط مرتفع (&gt; 0.5):</strong> الذهب يتحرك مع الأسهم — خطر! يعني أن البيع القسري للأسهم سيسحب الذهب للأسفل معه.<br><br>
        <strong>العلاقة:</strong> كلما زاد الارتباط، قلّت حصانة الذهب أمام انهيار الأسهم.<br><br>
        <strong>القيمة الحالية ({data['gold_equity_corr']:.2f}):</strong> 
        {'🔴 مرتفع جداً — الذهب رهينة للأسهم' if data['gold_equity_corr'] > 0.5 else 
         '🟠 مرتفع — حذر' if data['gold_equity_corr'] > 0.3 else 
         '🟢 منخفض — الذهب ملاذ آمن حقيقي'}
        </div>
        """, unsafe_allow_html=True)

    # 5. رادار البيع القسري
    with st.expander("📡 رادار البيع القسري — الدرجة الحالية: " + f"{result['radar']['score']}/10"):
        st.markdown(f"""
        <div class="explainer-box">
        <strong>ما هو؟</strong> مؤشر يخبرك إذا كان الهبوط الحالي بسبب "بيع قسري" (مضاربون مُجبرون على البيع) أو "بيع اختياري" (قرار استثماري).<br><br>
        <strong>كيف يُحسب؟</strong> يعتمد على:<br>
        • حجم التداول (إذا كان 2x+ من المتوسط)<br>
        • تغير السعر (إذا كان هبوطاً حاداً)<br>
        • انهيار الأسهم (مصدر الضغط)<br>
        • المراكز المفتوحة (الوقود)<br><br>
        <strong>المستويات:</strong><br>
        • <strong>0-3 (CLEAR):</strong> السوق مستقر — يمكن التفكير في الشراء.<br>
        • <strong>4-6 (WARNING):</strong> ضغط بيع محتمل — راقب.<br>
        • <strong>7-10 (CRITICAL):</strong> بيع قسري نشط — لا تشترِ، انتظر 48-72 ساعة.<br><br>
        <strong>الدرجة الحالية ({result['radar']['score']}/10):</strong> 
        {'🔴 حرج — لا تشترِ' if result['radar']['score'] >= 7 else 
         '🟠 تحذير — راقب' if result['radar']['score'] >= 4 else 
         '🟢 آمن'}
        </div>
        """, unsafe_allow_html=True)

    # 6. درجة الثقة
    with st.expander("💪 درجة الثقة — القيمة الحالية: " + f"{result['confidence']:.1f}/10"):
        st.markdown(f"""
        <div class="explainer-box">
        <strong>ما هي؟</strong> مدى ثقة النموذج في توقعه. كلما زادت، زادت موثوقية التوقع.<br><br>
        <strong>لماذا تنخفض؟</strong><br>
        • في حالة CRISIS، تنخفض الثقة تلقائياً لأن السوق غير عقلاني.<br>
        • إذا كان التغير المتوقع صغيراً (مثلاً 0.5%)، تنخفض الثقة.<br><br>
        <strong>المستويات:</strong><br>
        • <strong>0-3:</strong> ثقة منخفضة — لا تعتمد على التوقع.<br>
        • <strong>4-6:</strong> ثقة متوسطة — استخدمه كإشارة مساعدة.<br>
        • <strong>7-10:</strong> ثقة عالية — إشارة قوية.<br><br>
        <strong>القيمة الحالية ({result['confidence']:.1f}/10):</strong> 
        {'🟢 عالية' if result['confidence'] > 6 else 
         '🟡 متوسطة' if result['confidence'] > 3 else 
         '🔴 منخفضة'}
        </div>
        """, unsafe_allow_html=True)

    # 7. الركود التضخمي
    with st.expander("📊 احتمالية الركود التضخمي — القيمة الحالية: " + f"{result['stagflation_probability']}%"):
        st.markdown(f"""
        <div class="explainer-box">
        <strong>ما هو؟</strong> الركود التضخمي هو أسوأ سيناريو اقتصادي: تضخم مرتفع + نمو بطيء + بطالة مرتفعة.<br><br>
        <strong>كيف يُحسب؟</strong> يعتمد على 5 عوامل:<br>
        • التضخم الأساسي (فوق 3%؟)<br>
        • نمو GDP (تحت 1%؟)<br>
        • قاعدة ساهم للبطالة (0.5%+)<br>
        • الفائدة الحقيقية (فوق 1.5%؟)<br>
        • صدمة النفط (فوق 120$؟)<br><br>
        <strong>المستويات:</strong><br>
        • <strong>0-40%:</strong> منخفض — الاقتصاد ينمو.<br>
        • <strong>40-70%:</strong> متوسط — بدأت علامات التباطؤ.<br>
        • <strong>70-100%:</strong> مرتفع — ركود تضخمي وشيك.<br><br>
        <strong>القيمة الحالية ({result['stagflation_probability']}%):</strong> 
        {'🔴 مرتفع — استعد لسيناريو الأزمة' if result['stagflation_probability'] > 70 else 
         '🟠 متوسط — راقب البيانات' if result['stagflation_probability'] > 40 else 
         '🟢 منخفض — الاقتصاد متماسك'}
        </div>
        """, unsafe_allow_html=True)

    # 8. حالة السوق
    with st.expander("🚦 حالة السوق (Regime) — الحالية: " + result['regime'].upper()):
        st.markdown(f"""
        <div class="explainer-box">
        <strong>ما هو؟</strong> تصنيف السوق حسب درجة الخطر: NORMAL أو STRESS أو CRISIS.<br><br>
        <strong>كيف يُحدد؟</strong> من خلال 5 مؤشرات: VIX، تغير ناسداك، الارتباط، كثافة الخوارزميات، والمراكز المفتوحة.<br><br>
        <strong>كل حالة تعني:</strong><br>
        • <strong>NORMAL (طبيعي):</strong> الأساسيات تحكم السوق. النموذج الاقتصادي هو الأهم (60%).<br>
        • <strong>STRESS (توتر):</strong> الارتباطات تتغير. نعطي وزناً أكبر للتدفقات (35%).<br>
        • <strong>CRISIS (أزمة):</strong> البيع القسري يحكم. التدفقات هي الأهم (60%).<br><br>
        <strong>حالتك الحالية: {result['regime'].upper()}</strong>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════
# TAB 2-5: الأخبار
# ═════════════════════════════════════════════════════
def render_news_tab(category):
    """دالة مساعدة لعرض تبويب أخبار"""
    news = get_news(category)
    live = is_live(category)
    
    if live:
        st.success("🟢 الأخبار محدثة مباشرة من المصدر")
    else:
        st.info("📌 المصادر الحية غير متاحة حالياً — يتم عرض محتوى احتياطي محدث")
    
    if not news:
        st.warning("⚠️ لا توجد أخبار متاحة حالياً")
        return
    
    for item in news:
        date_str = item.get('date', '')[:10] if item.get('date') else ''
        summary = item.get('summary', '')
        # تنظيف HTML من summary
        import re
        summary = re.sub(r'<[^>]+>', '', summary)[:300]
        
        st.markdown(f"""
        <div class="news-card">
            <div class="news-title">{item['title']}</div>
            <div class="news-summary">{summary}...</div>
            <div class="news-date">📅 {date_str}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if item.get('link') and item['link'] != '#':
            st.markdown(f"[🔗 اقرأ المزيد]({item['link']})")
        st.markdown("")


with tab2:
    st.markdown("## 🏛️ الاحتياطي الفيدرالي")
    st.markdown("<p style='color:#B0B8D4;'>آخر تصريحات وقرارات الفيدرالي الأمريكي</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    render_news_tab("fed")

with tab3:
    st.markdown("## 🥇 مجلس الذهب العالمي")
    st.markdown("<p style='color:#B0B8D4;'>أحدث تقارير وإحصائيات مجلس الذهب العالمي</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    render_news_tab("gold")

with tab4:
    st.markdown("## 📊 آراء المحللين الاقتصاديين")
    st.markdown("<p style='color:#B0B8D4;'>توقعات وآراء كبار المحللين والبنوك الاستثمارية</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    render_news_tab("analysts")

with tab5:
    st.markdown("## 📈 آخر أخبار الأسواق")
    st.markdown("<p style='color:#B0B8D4;'>تطورات الأسهم والسندات والنفط والعملات</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    render_news_tab("markets")


# ═══════════════════════════════════════════════════
# الشريط الجانبي
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
    if st.button("🔄 تحديث البيانات والأخبار", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.caption("⏱️ البيانات: 5 دقائق | الأخبار: 30 دقيقة")


# ═══════════════════════════════════════════════════
# التذييل
# ═══════════════════════════════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#8892B0;font-size:0.85rem;padding:1rem;">
    ⚠️ <strong>تنبيه:</strong> هذه المنصة أداة مساعدة للتفكير وليست نصيحة استثمارية.<br>
    المحتوى الإخباري مُجمّع من مصادر عامة، يُرجى التحقق من المصادر الأصلية.<br>
    GOLD-X 3.0 © 2026
</div>
""", unsafe_allow_html=True)
