"""Gold price calculator Streamlit page."""

import streamlit as st


GRAMS_PER_OUNCE = 31.1034768


st.set_page_config(page_title="حاسبة أسعار الذهب", page_icon="🪙", layout="wide")
st.title("🪙 حاسبة أسعار الذهب")
st.write("احسب قيمة الذهب حسب العيار والوزن وسعر الأونصة.")

try:
    from data_fetcher import fetch_all_data

    data = fetch_all_data()
    default_ounce_price = float(data["current_price"])
except Exception:
    default_ounce_price = 3555.20

st.session_state.setdefault("gold_ounce_price", default_ounce_price)

col1, col2, col3 = st.columns(3)
with col1:
    ounce_price = st.number_input(
        "سعر الأونصة بالدولار",
        min_value=0.01,
        value=float(st.session_state.gold_ounce_price),
        step=1.0,
    )
with col2:
    weight = st.number_input("الوزن بالجرام", min_value=0.01, value=1.0, step=0.5)
with col3:
    purity = st.selectbox("عيار الذهب", (24, 22, 21, 18, 14), index=0)

gram_price = (ounce_price / GRAMS_PER_OUNCE) * (purity / 24)
total_price = gram_price * weight

st.divider()
metric1, metric2, metric3 = st.columns(3)
metric1.metric("سعر الجرام", f"${gram_price:,.2f}")
metric2.metric("الوزن", f"{weight:,.2f} جم")
metric3.metric("القيمة الإ��مالية", f"${total_price:,.2f}")

st.caption("الأسعار مبنية على سعر الأونصة للذهب الخالص، وتُحسب نسب العيارات المختلفة من عيار 24.")
