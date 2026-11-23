import yfinance as yf
import json
from datetime import datetime

def fetch_and_save():
    print("بدء جلب البيانات...")
    data = {}
    
    try:
        # جلب الذهب والدولار والناسداك من ياهو
        tickers = yf.download("GC=F DX-Y.NYB ^IXIC ^VIX ^TNX", period="5d", interval="1d")
        
        data['current_price'] = float(tickers['Close']['GC=F'].iloc[-1])
        data['price_change'] = float((tickers['Close']['GC=F'].iloc[-1] / tickers['Close']['GC=F'].iloc[-2] - 1))
        data['dxy_value'] = float(tickers['Close']['DX-Y.NYB'].iloc[-1])
        data['nasdaq_value'] = float(tickers['Close']['^IXIC'].iloc[-1])
        data['vix'] = float(tickers['Close']['^VIX'].iloc[-1])
        data['treasury_yield'] = float(tickers['Close']['^TNX'].iloc[-1])
        
        # حسابات إضافية
        data['dxy_change'] = float((tickers['Close']['DX-Y.NYB'].iloc[-1] / tickers['Close']['DX-Y.NYB'].iloc[-5] - 1))
        data['sp500_change_5d'] = float((tickers['Close']['^IXIC'].iloc[-1] / tickers['Close']['^IXIC'].iloc[-5] - 1))
        
        # قيم افتراضية للارتباط وغيرها
        data['gold_equity_corr'] = 0.45 
        data['gold_ai_correlation'] = 0.45
        data['volume_spike'] = 1.0
        data['sources'] = {"gold": "Yahoo via Updater", "vix": "Yahoo via Updater", "dxy": "Yahoo via Updater", "nasdaq": "Yahoo via Updater", "treasury": "Yahoo via Updater"}
        data['last_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("تم تحديث الملف بنجاح!")
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    fetch_and_save()
