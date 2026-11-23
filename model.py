"""نموذج GOLD-X 3.0"""
import numpy as np
from enum import Enum


class MarketRegime(Enum):
    NORMAL = "normal"
    STRESS = "stress"
    CRISIS = "crisis"


def detect_regime(vix, sp500_change_5d, gold_equity_corr, algo_intensity, open_interest_ratio):
    score = 0
    if vix > 35: score += 3
    elif vix > 25: score += 2
    elif vix > 20: score += 1
    
    if sp500_change_5d < -0.05: score += 3
    elif sp500_change_5d < -0.02: score += 2
    elif sp500_change_5d < 0: score += 1
    
    if gold_equity_corr > 0.4: score += 3
    elif gold_equity_corr > 0.2: score += 2
    
    if algo_intensity > 0.75: score += 2
    elif algo_intensity > 0.6: score += 1
    
    if open_interest_ratio > 1.8: score += 3
    elif open_interest_ratio > 1.4: score += 2
    
    if score >= 8: return MarketRegime.CRISIS
    elif score >= 4: return MarketRegime.STRESS
    return MarketRegime.NORMAL


def economic_model(dxy_change, tip_change, cpi_change, fed_stance, regime):
    betas = {
        MarketRegime.NORMAL:  {'dxy': -0.85, 'tip': -1.20, 'cpi': 0.55, 'fed': 0.20},
        MarketRegime.STRESS:  {'dxy': -0.60, 'tip': -0.90, 'cpi': 0.70, 'fed': 0.15},
        MarketRegime.CRISIS:  {'dxy': -0.30, 'tip': -0.40, 'cpi': 0.30, 'fed': 0.05},
    }[regime]
    return (betas['dxy'] * dxy_change + betas['tip'] * tip_change +
            betas['cpi'] * cpi_change + betas['fed'] * fed_stance)


def flow_model(open_interest_ratio, volume_spike, etf_outflow_ratio, regime):
    pressure = (max(0, open_interest_ratio - 1.0) * 0.4 +
                max(0, volume_spike - 1.5) * 0.3 +
                max(0, etf_outflow_ratio) * 0.3)
    mult = {MarketRegime.CRISIS: 0.15, MarketRegime.STRESS: 0.08,
            MarketRegime.NORMAL: 0.02}[regime]
    return -pressure * mult


def ai_tech_model(ai_bubble_score, ai_earnings_surprise, ipo_sentiment, gold_ai_correlation, regime):
    direct = -ai_bubble_score * 0.05 + ai_earnings_surprise * 0.03
    crash_risk = 0
    if ai_bubble_score > 0.8 and ai_earnings_surprise < 0:
        crash_risk = (ai_bubble_score - 0.8) * gold_ai_correlation * 0.25
    return direct - crash_risk - ipo_sentiment * 0.02


def dynamic_weights(regime):
    return {
        MarketRegime.NORMAL: {'economic': 0.60, 'flow': 0.15, 'ai': 0.25},
        MarketRegime.STRESS: {'economic': 0.40, 'flow': 0.35, 'ai': 0.25},
        MarketRegime.CRISIS: {'economic': 0.15, 'flow': 0.60, 'ai': 0.25},
    }[regime]


def forced_selling_radar(volume_spike, price_change, open_interest_ratio, sp500_change):
    score = 0
    if volume_spike > 2.0: score += 3
    elif volume_spike > 1.5: score += 2
    if price_change < -0.02: score += 2
    elif price_change < -0.01: score += 1
    if sp500_change < -0.03: score += 3
    elif sp500_change < -0.015: score += 2
    if open_interest_ratio > 1.5: score += 2
    
    if score >= 7:
        return {"status": "CRITICAL", "score": score,
                "msg": "⛔ بيع قسري نشط. لا تشترِ الآن. انتظر 48-72 ساعة."}
    elif score >= 4:
        return {"status": "WARNING", "score": score,
                "msg": "⚡ ضغط بيع محتمل. راقب السوق."}
    return {"status": "CLEAR", "score": score,
            "msg": "✅ السوق مستقر نسبياً. يمكن التفكير في الشراء."}


def stagflation_index(core_pce=3.1, gdp_growth=3.4, unemployment_change=-0.1,
                      real_rate=0.78, oil=95.8):
    score = 0
    if core_pce > 3.0: score += 25
    elif core_pce > 2.5: score += 15
    if gdp_growth < 1.0: score += 25
    elif gdp_growth < 2.0: score += 15
    if unemployment_change > 0.5: score += 25
    elif unemployment_change > 0.3: score += 15
    if real_rate > 1.5: score += 15
    elif real_rate > 0.5: score += 10
    if oil > 120: score += 10
    elif oil > 100: score += 5
    return min(100, score)


def gold_x_model(data):
    regime = detect_regime(data['vix'], data['sp500_change_5d'],
                           data['gold_equity_corr'], data['algo_intensity'],
                           data['open_interest_ratio'])
                           
    econ = economic_model(data['dxy_change'], data['tip_change'],
                          data['cpi_change'], data['fed_stance'], regime)
                          
    flow = flow_model(data['open_interest_ratio'], data['volume_spike'],
                      data['etf_outflow_ratio'], regime)
                      
    ai = ai_tech_model(data['ai_bubble_score'], data['ai_earnings_surprise'],
                       data['ipo_sentiment'], data['gold_ai_correlation'], regime)
                       
    w = dynamic_weights(regime)
    change = w['economic'] * econ + w['flow'] * flow + w['ai'] * ai
    
    radar = forced_selling_radar(data['volume_spike'], change,
                                  data['open_interest_ratio'],
                                  data['sp500_change_5d'])
                                  
    warnings = []
    if data['ai_bubble_score'] > 0.85: warnings.append("🔴 فقاعة AI في خطر")
    if data['gold_ai_correlation'] > 0.5: warnings.append("🟡 ارتباط الذهب بـ AI مرتفع")
    if data['open_interest_ratio'] > 1.8: warnings.append("🟠 مراكز مفتوحة ضخمة")
    if data['vix'] > 35: warnings.append("🔴 VIX في منطقة ذعر")
    if data['treasury_yield'] > 5.0: warnings.append("🔴 عائد السندات فوق 5%")
    
    predicted = data['current_price'] * (1 + change)
    
    # تصحيح معادلة درجة الثقة
    base_conf = abs(change) * 100
    penalty = {MarketRegime.NORMAL: 0, MarketRegime.STRESS: 1.5,
               MarketRegime.CRISIS: 3.0}[regime]
    confidence = min(10, base_conf + penalty)
    
    if radar['status'] == "CRITICAL":
        rec = "⛔ لا تشترِ. بيع قسري نشط. انتظر 48-72 ساعة."
    elif change > 0.02 and confidence > 5:
        rec = "🟢 شراء (حسب خطة الدفعات)"
    elif change < -0.02 and confidence > 5:
        rec = "🔴 لا تشترِ الآن. انتظر استقرار السوق."
    else:
        rec = "🟡 انتظار / حياد"
        
    return {
        'regime': regime.value, 'change_pct': change * 100,
        'predicted_price': predicted, 'confidence': confidence,
        'recommendation': rec, 'radar': radar, 'warnings': warnings,
        'stagflation_probability': stagflation_index(),
        'breakdown': {'economic': round(econ, 4), 'flow': round(flow, 4),
                      'ai': round(ai, 4), 'weights': w}
    }