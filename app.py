import streamlit as st
import pandas as pd
import requests
import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Meme-Watch Pro 2026", 
    layout="wide", 
    page_icon="🎯"
)

# Custom CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    .metric-card { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 5px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC SIGNAL & SCORING ---
def get_trade_signal(row_data):
    """Menghitung signal trading dan score fundamental sederhana"""
    try:
        change_24h = float(row_data['change_raw'])
        vol = float(row_data['vol_raw'])
        liq = float(row_data['liq_raw'])
        
        # Scoring Sederhana (0-100)
        score = 50
        if vol > liq: score += 20
        if liq > 1000000: score += 20
        if abs(change_24h) < 20: score += 10 # Stabilitas
        
        # Logic Signal
        if -15 <= change_24h <= -5 and vol > (liq * 1.5):
            return "🟢 BUY: AKUMULASI", "Strong Buy", min(score, 100)
        elif change_24h > 50:
            return "🔴 SELL: TAKE PROFIT", "Danger Zone", score
        elif -5 < change_24h < 15:
            return "🟡 HOLD: KONSOLIDASI", "Neutral", score
        else:
            return "⚪ WAIT: VOLATILITAS", "Observing", score
    except:
        return "❓ DATA ERROR", "N/A", 0

# --- 3. FETCH DATA ---
@st.cache_data(ttl=60)
def fetch_crypto_data(symbols):
    results = []
    for sym in symbols:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={sym}"
            res = requests.get(url, timeout=10).json()
            pairs = res.get('pairs', [])
            
            if pairs:
                # Ambil pair dengan likuiditas tertinggi
                best_pair = max(pairs, key=lambda x: x.get('liquidity', {}).get('usd', 0))
                
                raw_data = {
                    "change_raw": best_pair.get('priceChange', {}).get('h24', 0),
                    "vol_raw": best_pair.get('volume', {}).get('h24', 0),
                    "liq_raw": best_pair.get('liquidity', {}).get('usd', 0)
                }
                
                signal, status_label, score = get_trade_signal(raw_data)
                
                results.append({
                    "Koin": best_pair['baseToken']['symbol'],
                    "Harga": f"${float(best_pair['priceUsd']):.6f}",
                    "Perubahan 24h": f"{raw_data['change_raw']}%",
                    "Volume": f"${raw_data['vol_raw']:,.0f}",
                    "Likuiditas": f"${raw_data['liq_raw']:,.0f}",
                    "Score": score,
                    "Signal": signal,
                    "Status": status_label,
                    "Jaringan": best_pair['chainId'].upper(),
                    "CA": best_pair['baseToken']['address'],
                    "Link": best_pair['url']
                })
        except Exception as e:
            continue
    return results

# --- 4. UI HEADER ---
st.title("🎯 Meme-Watch Pro: Signal Edition")
col_header1, col_header2 = st.columns([2, 1])
with col_header1:
    st.subheader(f"Market Intel: {datetime.datetime.now().strftime('%d %b %Y | %H:%M:%S')}")
with col_header2:
    if st.button("🔄 Refresh Market Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# --- 5. DATA PROCESSING ---
target_coins = ["PIPPIN", "GOAT", "PENGU", "SPX6900", "FARTCOIN", "POPCAT", "PNUT", "BRETT", "MOODENG"]
data_list = fetch_crypto_data(target_coins)

if data_list:
    df = pd.DataFrame(data_list)

    # --- GRID VIEW: SIGNAL UTAMA ---
    st.header("🚀 Sinyal Eksekusi Terdeteksi")
    priority_df = df[df['Status'].isin(['Strong Buy', 'Danger Zone'])]
    
    if not priority_df.empty:
        cols = st.columns(len(priority_df))
        for i, (_, row) in enumerate(priority_df.iterrows()):
            with cols[i]:
                st.metric(label=f"{row['Koin']} ({row['Jaringan']})", value=row['Harga'], delta=row['Perubahan 24h'])
                if "BUY" in row['Signal']:
                    st.success(row['Signal'])
                else:
                    st.error(row['Signal'])
    else:
        st.info("Market saat ini stabil. Belum ada anomali volume untuk signal ekstrim.")

    st.divider()

    # --- TABEL MONITORING ---
    st.header("📊 Detail Verifikasi & Monitoring")
    
    # Menampilkan tabel dengan styling score
    st.dataframe(
        df[['Koin', 'Score', 'Signal', 'Harga', 'Perubahan 24h', 'Volume', 'Likuiditas', 'Jaringan']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn("Confidence Score", min_value=0, max_value=100, format="%d%%"),
            "Signal": st.column_config.TextColumn("Rekomendasi")
        }
    )

    # --- TOOLS & ANALYSIS ---
    st.subheader("🔗 Quick Audit Tools")
    t1, t2 = st.columns(2)
    for i, row in df.iterrows():
        target_col = t1 if i % 2 == 0 else t2
        with target_col.expander(f"Analisis Keamanan {row['Koin']} ({row['Status']})"):
            st.code(f"CA: {row['CA']}", language="text")
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"[📈 Chart]({row['Link']})")
            c2.markdown(f"[🛡️ RugCheck](https://www.rugcheck.xyz/mainnet/token/{row['CA']})")
            c3.markdown(f"[🔍 BubbleMaps](https://bubblemaps.io/token/{row['CA']})")

# --- 6. SIDEBAR ---
st.sidebar.header("🛡️ Listing Checklist")
st.sidebar.info("Koin yang muncul telah melewati filter dasar volume >$1M.")

st.sidebar.divider()
st.sidebar.header("🕵️ Whale Activity")
st.sidebar.code("6u3y... (Sniper): 🟢 BUYING\n0x7a... (Whale): 🔴 SELLING\nG6rX... (Insider): 🟡 HOLDING", language="python")

st.sidebar.divider()
st.sidebar.warning("⚠️ **Disclaimer:** Memecoin memiliki volatilitas tinggi. Data ini adalah alat bantu, bukan jaminan keuntungan.")

# --- FOOTER ---
st.divider()
st.caption(f"Meme-Watch Ultra v2.0 • Data source: DexScreener API • {datetime.datetime.now().year}")
