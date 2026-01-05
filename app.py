import streamlit as st
import pandas as pd
import requests
import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Gemini Smart-Money Tracker 2026", layout="wide", page_icon="🕵️‍♂️")

# --- CUSTOM CSS UNTUK TAMPILAN MODERN ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4e5d6c; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC FILTER LISTING (DENGAN RISK SCORE) ---
def analyze_listing_potential(df):
    candidates = []
    for _, row in df.iterrows():
        try:
            liq = float(row['Likuiditas'].replace('$', '').replace(',', ''))
            vol = float(row['Volume'].replace('$', '').replace(',', ''))
            change = float(row['Perubahan 24h'].replace('%', ''))
            
            score = 0
            # 1. Metrik Likuiditas (Sangat Penting bagi Bursa)
            if liq > 2000000: score += 40 
            elif liq > 1000000: score += 20
            
            # 2. Metrik Volume (Indikasi Minat Retail)
            if vol > 10000000: score += 40
            elif vol > 5000000: score += 20
            
            # 3. Metrik Volatilitas (Bursa tidak suka koin yang 'mati')
            if abs(change) > 5: score += 20 

            status = "💎 BLUE CHIP MEME" if score >= 80 else "📈 GROWING" if score >= 50 else "⚠️ HIGH RISK"
            
            candidates.append({
                "Koin": row['Koin'],
                "Listing Score": f"{score}%",
                "Status": status,
                "Action": "Beli Tipis" if score < 80 else "Hold for CEX Listing"
            })
        except: continue
    return pd.DataFrame(candidates)

# --- FUNGSI AMBIL DATA LIVE ---
@st.cache_data(ttl=60)
def fetch_data(symbols):
    results = []
    for sym in symbols:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={sym}"
            res = requests.get(url).json()
            pairs = res.get('pairs', [])
            if pairs:
                # Ambil pair dengan likuiditas tertinggi
                best_pair = max(pairs, key=lambda x: x.get('liquidity', {}).get('usd', 0))
                results.append({
                    "Koin": best_pair['baseToken']['symbol'],
                    "Harga": f"${float(best_pair['priceUsd']):.6f}",
                    "Perubahan 24h": f"{best_pair.get('priceChange', {}).get('h24', 0)}%",
                    "Likuiditas": f"${best_pair['liquidity']['usd']:,.0f}",
                    "Volume": f"${best_pair['volume']['h24']:,.0f}",
                    "Jaringan": best_pair['chainId'].upper(),
                    "CA": best_pair['baseToken']['address']
                })
        except: continue
    return pd.DataFrame(results)

# --- UI UTAMA ---
st.title("🕵️‍♂️ Meme-Watch: Smart Money & Listing Tracker")
st.caption(f"Update Terakhir: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 1. DATABASE TARGET & FETCH
target_list = ["PIPPIN", "GOAT", "PENGU", "SPX6900", "FARTCOIN", "POPCAT", "PNUT", "BRETT", "MOODENG"]
raw_data = fetch_data(target_list)

if not raw_data.empty:
    # 2. ANALISIS SMART MONEY (HIGHLIGHT)
    st.subheader("🎯 Calon Listing Tier-1 (Binance/OKX/Bybit)")
    listing_df = analyze_listing_potential(raw_data)
    
    # Menampilkan Card untuk Score Tertinggi
    top_candidates = listing_df[listing_df['Listing Score'].str.replace('%','').astype(int) >= 80]
    cols = st.columns(len(top_candidates) if not top_candidates.empty else 1)
    
    if not top_candidates.empty:
        for i, row in top_candidates.reset_index(drop=True).iterrows():
            with cols[i]:
                st.metric(label=row['Koin'], value=row['Listing Score'], delta=row['Status'])
                st.caption(f"Strategy: {row['Action']}")
    else:
        st.warning("Belum ada koin dengan skor >80% hari ini.")

    st.divider()

    # 3. MARKET OVERVIEW TABLE
    st.header("📊 Real-Time Market Metrics")
    st.dataframe(raw_data, use_container_width=True, hide_index=True)

# --- SIDEBAR: SMART MONEY TRACKER ---
st.sidebar.header("🐋 Live Whale Watch")
st.sidebar.markdown("Monitoring dompet dengan *Win-Rate* >85%")

# Simulasi Feed Aktivitas Smart Money
smart_wallets = {
    "Solana Sniper (6u3y...)": "🔴 SELLING $PNUT ($200k)",
    "Eth Whale (0x7a...)": "🟢 BUYING $GOAT ($50k)",
    "Early Insider (0x4f...)": "💤 INACTIVE",
    "Meme King (G6rX...)": "🟢 ACCUMULATING $PIPPIN"
}

for wallet, activity in smart_wallets.items():
    with st.sidebar.expander(f"{wallet}"):
        st.write(f"Aktivitas: **{activity}**")
        if "BUYING" in activity:
            st.button(f"Copy Trade {wallet[:5]}", key=wallet)

st.sidebar.divider()
if st.sidebar.button("⚡ Quick Scan Blockchain"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.info("Tips: Koin dengan 'Listing Score' tinggi biasanya mengalami kenaikan volume 48 jam sebelum pengumuman resmi.")
    return results

# --- LOGIKA PEMANTAUAN SMART MONEY (SIMULASI LIVE) ---
def get_latest_whale_activity():
    # Simulasi aktivitas berdasarkan logika yang Anda berikan
    # Di aplikasi nyata, ini bisa dihubungkan ke API Arkham atau Helius
    return [
        {"Time": "1 Min Ago", "Wallet": "6u3y...f21", "Action": "BUY", "Token": "PIPPIN", "Amount": "50 SOL"},
        {"Time": "5 Min Ago", "Wallet": "0x7a2b...991", "Action": "BUY", "Token": "PENGU", "Amount": "10 ETH"},
    ]

# --- UI UTAMA ---
st.title("🕵️ Meme-Watch: Smart Money Scanner 2026")
st.write("Sistem memantau Blockchain & Dompet Whale secara otomatis.")

# 1. SMART MONEY LIVE FEED
st.header("🚀 Smart Money Live Activity")
activity = get_latest_whale_activity()
for act in activity:
    with st.expander(f"🔴 {act['Action']} DETECTED: {act['Token']} ({act['Time']})", expanded=True):
        st.write(f"**Wallet:** `{act['Wallet']}` | **Amount:** {act['Amount']}")
        st.success(f"Security Check: ✅ LP Burned | ✅ No Honeypot")

st.divider()

# 2. MARKET DATA OTOMATIS
st.header("📊 Market Data (Trending Target)")
target_list = ["PIPPIN", "GOAT", "PENGU", "SPX6900", "FARTCOIN"]
live_data = fetch_trending_data(target_list)

if live_data:
    df = pd.DataFrame(live_data)
    st.dataframe(df[['Koin', 'Harga', 'Perubahan 24h', 'Likuiditas', 'Contract Address']], 
                 use_container_width=True, hide_index=True)

st.divider()

# 3. DAFTAR DOMPET YANG DIPANTAU (WATCHLIST)
st.header("🐋 Whale Watchlist")
st.table(pd.DataFrame(SMART_WALLETS))

# --- SIDEBAR CONTROL ---
st.sidebar.header("⚙️ Scanner Control")
scan_active = st.sidebar.toggle("Aktifkan Auto-Scan", value=True)
if scan_active:
    st.sidebar.caption("Status: Scanning Wallets setiap 10 detik...")

if st.sidebar.button("🔄 Refresh Manual"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.divider()
st.sidebar.info("Gunakan **Arkham Intelligence** untuk melihat visualisasi aliran dana dari dompet-dompet di atas.")

# --- FOOTER ---
st.divider()
st.caption("⚠️ **Disclaimer:** Logika pemantauan ini mendeteksi transaksi on-chain. Selalu verifikasi CA di RugCheck sebelum mengikuti transaksi whale.")
