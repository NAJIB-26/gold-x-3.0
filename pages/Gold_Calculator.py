"""Gold price and karat calculator Streamlit page."""

import streamlit as st


GRAMS_PER_TROY_OUNCE = 31.1034768
KARATS = (24, 22, 21, 18, 14)
CURRENCIES = {
    "USD": ("دولار أمريكي", 1.0),
    "SAR": ("ريال سعودي", 3.75),
    "AED": ("درهم إماراتي", 3.6725),
    "EGP": ("جنيه مصري", 50.5),
    "EUR": ("يورو", 0.92),
    "YER": ("ريال يمني", 1600.0),
}


def format_english_number(value, decimals=2):
    """Format numbers with Western digits and isolate them from RTL text."""
    formatted = f"{value:,.{decimals}f}"
    # Keep displayed price digits ASCII even if a browser applies Arabic numerals.
    formatted = formatted.translate(str.maketrans("01234567890123456789", "01234567890123456789"))
    return f"\u2066{formatted}\u2069"


st.set_page_config(page_title="أسعار الذهب حسب العيار", page_icon=".", layout="wide")
st.title(". أسعار الذهب حسب الجرام والعيار")
st.write("اختر العملة، ثم أدخل سعر الصرف والوزن لحساب قيمة الذهب.")

try:
    from data_fetcher import fetch_all_data

    data = fetch_all_data()
    default_ounce_price = float(data["current_price"])
except Exception:
    default_ounce_price = 3555.20
    st.warning("تعذر جلب سعر الذهب؛ يُستخدم سعر أونصة افتراضي ويمكنك تعديله يدويًا.")

st.session_state.setdefault("gold_ounce_price", default_ounce_price)
st.session_state.setdefault("gold_currency", "USD")
for currency_code, (_, default_rate) in CURRENCIES.items():
    st.session_state.setdefault(f"gold_fx_{currency_code}", default_rate)

settings_col1, settings_col2, settings_col3 = st.columns(3)
with settings_col1:
    currency_code = st.selectbox(
        "العملة",
        options=list(CURRENCIES),
        format_func=lambda code: f"{code} — {CURRENCIES[code][0]}",
        key="gold_currency",
    )
with settings_col2:
    exchange_rate = st.number_input(
        f"سعر الصرف: كم {currency_code} يساوي 1 USD؟",
        min_value=0.000001,
        value=float(st.session_state[f"gold_fx_{currency_code}"]),
        step=0.01,
        format="%.6f",
        key=f"gold_fx_input_{currency_code}",
        help="يمكن تعديل سعر الصرف يدويًا. القيمة الافتراضية تقريبية وليست تحديثًا مباشرًا. سعر الريال اليمني يختلف حسب المنطقة.",
    )
with settings_col3:
    ounce_price_usd = st.number_input(
        "سعر أونصة الذهب بالدولار الأمريكي",
        min_value=0.01,
        value=float(st.session_state.gold_ounce_price),
        step=1.0,
        format="%.2f",
        key="gold_ounce_price",
    )

st.session_state[f"gold_fx_{currency_code}"] = exchange_rate
ounce_price = ounce_price_usd * exchange_rate
currency_name = CURRENCIES[currency_code][0]

st.subheader(f"سعر الجرام حسب العيار — {currency_code}")
price_rows = [
    {
        "العيار": f"عيار {karat}",
        "نسبة النقاء": format_english_number(karat / 24 * 100) + "%",
        f"سعر الجرام ({currency_code})": format_english_number(
            (ounce_price / GRAMS_PER_TROY_OUNCE) * (karat / 24)
        ),
    }
    for karat in KARATS
]
st.table(price_rows)

st.subheader("احسب قيمة وزن محدد")
calc_col1, calc_col2 = st.columns(2)
with calc_col1:
    weight = st.number_input(
        "الوزن بالجرام", min_value=0.01, value=1.0, step=0.5, format="%.2f"
    )
with calc_col2:
    selected_karat = st.selectbox("العيار", KARATS, format_func=lambda karat: f"عيار {karat}")

gram_price = (ounce_price / GRAMS_PER_TROY_OUNCE) * (selected_karat / 24)
total_price = gram_price * weight

metric1, metric2, metric3 = st.columns(3)
metric1.metric(
    f"سعر الجرام — عيار {selected_karat}",
    f"{format_english_number(gram_price)} {currency_code}",
)
metric2.metric("الوزن", f"{format_english_number(weight)} جم")
metric3.metric(
    "القيمة الإجمالية",
    f"{format_english_number(total_price)} {currency_code}",
)

st.caption(
    f"العملة المحددة: {currency_name}. أسعار الصرف الافتراضية تقريبية وقابلة للتعديل، "
    "وسعر الذهب محسوب من سعر الأونصة المدخل دون إضافة المصنعية أو الضرائب."
)
