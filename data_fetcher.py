import json
import requests
import streamlit as st
import pandas as pd

@st.cache_data(ttl=60) # يقرأ الملف كل دقيقة
def fetch_all_data():
    try:
        # قراءة الملف مباشرة من مستودعك (استبدل NAJIB-26 باسم حسابك)
        url = "https://raw.githubusercontent.com/NAJIB-26/gold-x-3.0/main/data.json"
        response = requests.get(url)
        data = response.json()
        
        # إضافة القيم الافتراضية التي يحتاجها النموذج
        data['tip_change'] = 0.002
        data['cpi_change'] = 0.004
        data['fed_stance'] = -0.8
        data['algo_intensity'] = 0.75
        data['open_interest_ratio'] = 1.5
        data['etf_outflow_ratio'] = 0.01
        data['ai_bubble_score'] = 0.75
        data['ai_earnings_surprise'] = -0.02
        data['ipo_sentiment'] = 0.0
        
        return data
    except Exception as e:
        st.error(f"فشل قراءة البيانات من الملف: {e}")
        # قيم احتياطية في حال فشل القراءة
        return {
            'current_price': 3585.0, 'price_change': 0.0, 'volume_spike': 1.0,
            'dxy_change': 0.0, 'dxy_value': 103.0, 'sp500_change_5d': 0.0,
            'nasdaq_value': 22000.0, 'vix': 20.0, 'treasury_yield': 5.1,
            'gold_equity_corr': 0.5, 'gold_ai_correlation': 0.5,
            'tip_change': 0.002, 'cpi_change': 0.004, 'fed_stance': -0.8,
            'algo_intensity': 0.75, 'open_interest_ratio': 1.5,
            'etf_outflow_ratio': 0.01, 'ai_bubble_score': 0.75,
            'ai_earnings_surprise': -0.02, 'ipo_sentiment': 0.0,
            'sources': {'gold': '⚠️ احتياطي', 'vix': '⚠️ احتياطي', 'dxy': '⚠️ احتياطي', 'nasdaq': '⚠️ احتياطي', 'treasury': '⚠️ احتياطي'}
        }
