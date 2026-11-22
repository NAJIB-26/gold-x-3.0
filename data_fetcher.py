"""
جالب البيانات مع 3 مصادر بديلة لكل مؤشر.
المصادر: yfinance → Stooq → FRED → Investing.com → بيانات احتياطية
"""
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import streamlit as st

# ═══════════════════════════════════════════════════
# دوال مساعدة لكل مصدر
# ═══════════════════════════════════════════════════

@st.cache_data(ttl=300)  # تخزين مؤقت 5 دقائق
def _fetch_yfinance(ticker, period="1mo", interval="1d"):
    """المصدر الأساسي: Yahoo Finance"""
    try:
        data = yf.Ticker(ticker).history(period=period, interval=interval)
        if data.empty:
            return None
        return data
    except Exception:
        return None


@st.cache_data(ttl=300)
def _fetch_stooq(symbol):
    """المصدر البديل 1: Stooq (مجاني، بدون مفاتيح)"""
    try:
        url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
        df = pd.read_csv(url)
        if df.empty or 'Close' not in df.columns:
            return None
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        return df.tail(30)
    except Exception:
        return None


@st.cache_data(ttl=300)
def _fetch_fred(series_id):
    """المصدر البديل 2: FRED (الاحتياطي الفيدرالي)"""
    try:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        df = pd.read_csv(url, parse_dates=['DATE'])
        df.set_index('DATE', inplace=True)
        df.columns = ['Close']
        return df.tail(30)
    except Exception:
        return None


@st.cache_data(ttl=600)
def _fetch_investing_scrape():
    """المصدر البديل 3: Investing.com (كشط HTML)"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        url = "https://www.investing.com/currencies/xau-usd"
        r = requests.get(url, headers=headers, timeout=10)
        # البحث عن السعر في HTML
        import re
        match = re.search(r'"last":\s*([\d.]+)', r.text)
        if match:
            return float(match.group(1))
        return None
    except Exception:
        return None


# ═══════════════════════════════════════════════════
# الدالة الرئيسية لجلب سعر الذهب
# ═══════════════════════════════════════════════════

@st.cache_data(ttl=300)
def get_gold_price():
    """
    جلب سعر الذهب من 4 مصادر بالترتيب:
    1. yfinance (GC=F)
    2. Stooq (xauusd)
    3. Investing.com (كشط)
    4. قيمة احتياطية
    """
    sources_tried = []
    
    # المصدر 1: yfinance
    data = _fetch_yfinance("GC=F")
    if data is not None and not data.empty:
        return {
            'price': float(data['Close'].iloc[-1]),
            'change': float((data['Close'].iloc[-1] / data['Close'].iloc[-2] - 1)),
            'volume': int(data['Volume'].iloc[-1]) if 'Volume' in data else 0,
            'avg_volume': float(data['Volume'].mean()) if 'Volume' in data else 1,
            'history': data['Close'],
            'source': 'Yahoo Finance'
        }
    sources_tried.append("yfinance")
    
    # المصدر 2: Stooq
    data = _fetch_stooq("xauusd")
    if data is not None:
        return {
            'price': float(data['Close'].iloc[-1]),
            'change': float((data['Close'].iloc[-1] / data['Close'].iloc[-2] - 1)) if len(data) > 1 else 0,
            'volume': 1, 'avg_volume': 1,
            'history': data['Close'],
            'source': 'Stooq'
        }
    sources_tried.append("Stooq")
    
    # المصدر 3: Investing.com
    price = _fetch_investing_scrape()
    if price is not None:
        return {
            'price': price, 'change': 0, 'volume': 1, 'avg_volume': 1,
            'history': pd.Series([price]),
            'source': 'Investing.com'
        }
    sources_tried.append("Investing.com")
    
    # المصدر 4: قيمة احتياطية
    return {
        'price': 3585.0,  # آخر سعر معروف
        'change': 0, 'volume': 1, 'avg_volume': 1,
        'history': pd.Series([3585.0]),
        'source': f'⚠️ بيانات احتياطية (فشل: {sources_tried})'
    }


@st.cache_data(ttl=300)
def get_vix():
    """VIX: yfinance → FRED → Stooq"""
    data = _fetch_yfinance("^VIX", period="5d")
    if data is not None and not data.empty:
        return {'value': float(data['Close'].iloc[-1]), 'source': 'Yahoo Finance'}
    
    data = _fetch_fred("VIXCLS")
    if data is not None and not data.empty:
        return {'value': float(data['Close'].iloc[-1]), 'source': 'FRED'}
    
    data = _fetch_stooq("^vix")
    if data is not None and not data.empty:
        return {'value': float(data['Close'].iloc[-1]), 'source': 'Stooq'}
    
    return {'value': 20.0, 'source': '⚠️ احتياطي'}


@st.cache_data(ttl=300)
def get_dxy():
    """الدولار: yfinance → FRED → Stooq"""
    data = _fetch_yfinance("DX-Y.NYB", period="1mo")
    if data is not None and not data.empty:
        change = float(data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1) if len(data) >= 5 else 0
        return {'value': float(data['Close'].iloc[-1]), 'change_5d': change, 'source': 'Yahoo Finance'}
    
    data = _fetch_fred("DTWEXBGS")
    if data is not None and not data.empty:
        change = float(data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1) if len(data) >= 5 else 0
        return {'value': float(data['Close'].iloc[-1]), 'change_5d': change, 'source': 'FRED'}
    
    data = _fetch_stooq("dx.f")
    if data is not None and not data.empty:
        change = float(data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1) if len(data) >= 5 else 0
        return {'value': float(data['Close'].iloc[-1]), 'change_5d': change, 'source': 'Stooq'}
    
    return {'value': 103.0, 'change_5d': 0, 'source': '⚠️ احتياطي'}


@st.cache_data(ttl=300)
def get_nasdaq():
    """ناسداك: yfinance → FRED → Stooq"""
    data = _fetch_yfinance("^IXIC", period="1mo")
    if data is not None and not data.empty:
        change_5d = float(data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1) if len(data) >= 5 else 0
        return {'value': float(data['Close'].iloc[-1]), 'change_5d': change_5d, 
                'history': data['Close'], 'source': 'Yahoo Finance'}
    
    data = _fetch_fred("NASDAQCOM")
    if data is not None and not data.empty:
        change_5d = float(data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1) if len(data) >= 5 else 0
        return {'value': float(data['Close'].iloc[-1]), 'change_5d': change_5d,
                'history': data['Close'], 'source': 'FRED'}
    
    data = _fetch_stooq("^ndq")
    if data is not None and not data.empty:
        change_5d = float(data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1) if len(data) >= 5 else 0
        return {'value': float(data['Close'].iloc[-1]), 'change_5d': change_5d,
                'history': data['Close'], 'source': 'Stooq'}
    
    return {'value': 22000, 'change_5d': 0, 'history': pd.Series([22000]), 'source': '⚠️ احتياطي'}


@st.cache_data(ttl=300)
def get_treasury_yield():
    """عائد السندات: yfinance → FRED"""
    data = _fetch_yfinance("^TNX", period="5d")
    if data is not None and not data.empty:
        return {'value': float(data['Close'].iloc[-1]), 'source': 'Yahoo Finance'}
    
    data = _fetch_fred("DGS10")
    if data is not None and not data.empty:
        return {'value': float(data['Close'].iloc[-1]), 'source': 'FRED'}
    
    return {'value': 5.1, 'source': '⚠️ احتياطي'}


def calculate_correlation(gold_hist, nasdaq_hist):
    """حساب ارتباط الذهب بالأسهم (30 يوم)"""
    try:
        if len(gold_hist) < 10 or len(nasdaq_hist) < 10:
            return 0.5
        g = gold_hist.pct_change().dropna().tail(30)
        n = nasdaq_hist.pct_change().dropna().tail(30)
        min_len = min(len(g), len(n))
        if min_len < 5:
            return 0.5
        corr = np.corrcoef(g.tail(min_len), n.tail(min_len))[0, 1]
        return float(np.nan_to_num(corr, nan=0.5))
    except Exception:
        return 0.5


@st.cache_data(ttl=300)
def fetch_all_data():
    """
    الدالة الرئيسية: تجمع كل البيانات مع تسجيل المصادر.
    """
    gold = get_gold_price()
    vix = get_vix()
    dxy = get_dxy()
    nasdaq = get_nasdaq()
    treasury = get_treasury_yield()
    
    correlation = calculate_correlation(gold['history'], nasdaq['history'])
    
    volume_spike = (gold['volume'] / gold['avg_volume']) if gold['avg_volume'] > 0 else 1.0
    
    return {
        'current_price': gold['price'],
        'price_change': gold['change'],
        'volume_spike': min(volume_spike, 5.0),
        'dxy_change': dxy['change_5d'],
        'dxy_value': dxy['value'],
        'sp500_change_5d': nasdaq['change_5d'],
        'nasdaq_value': nasdaq['value'],
        'vix': vix['value'],
        'treasury_yield': treasury['value'],
        'gold_equity_corr': correlation,
        'gold_ai_correlation': correlation,
        # قيم افتراضية يمكن تحديثها يدوياً
        'tip_change': 0.002,
        'cpi_change': 0.004,
        'fed_stance': -0.8,
        'algo_intensity': 0.75,
        'open_interest_ratio': 1.5,
        'etf_outflow_ratio': 0.01,
        'ai_bubble_score': 0.75,
        'ai_earnings_surprise': -0.02,
        'ipo_sentiment': 0.0,
        'gold_history': gold['history'],
        'nasdaq_history': nasdaq['history'],
        # معلومات المصادر (للعرض للمستخدم)
        'sources': {
            'gold': gold['source'],
            'vix': vix['source'],
            'dxy': dxy['source'],
            'nasdaq': nasdaq['source'],
            'treasury': treasury['source'],
        }
    }
