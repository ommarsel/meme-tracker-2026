import streamlit as st
import pandas as pd
import requests
import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Meme-Watch Ultra 2026", layout="wide", page_icon="⚡")

# --- 2. CSS CUSTOM UNTUK TAMPILAN PREMIUM & MOBILE FRIENDLY ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stDataFrame { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ALGORITMA: PREDIKSI LISTING & SMART MONEY ---
def calculate_listing_score(row):
    """Menghitung potensi koin untuk listing di bursa Tier-1 (CEX)"""
    try:
        liq = float(row['Likuiditas'].replace('$', '').replace(',', ''))
        vol = float(row['Volume'].replace('$', '').replace(',', ''))
        
        score = 0
        if liq > 2000000: score += 40  # Likuiditas sangat dalam
        elif liq > 1000000: score += 20
        
        if vol > 10000000: score += 40 # Volume perdagangan masif
        elif vol > 5000000: score += 20
        
        if row['Jaringan'] in ['SOLANA', 'BASE']: score += 20 # Naratif 2026
        
        return score
    except:
        return 0

# --- 4. FUNGSI FETCH DATA (DEXSCREENER API) ---
@st.cache_data(ttl=60)
def fetch_trending_data(symbols):
    results = []
    for sym in symbols:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={sym}"
            res = requests.get(url).json()
            pairs = res.get('pairs', [])
            if pairs:
                # Ambil pair terbaik berdasarkan likuiditas tertinggi
                best_pair = max(pairs, key=lambda x: x.get('liquidity', {}).get('usd', 0))
                data = {
                    "Koin": best_pair['baseToken']['symbol'],
                    "Harga": f"${float(best_pair['priceUsd']):.6f}",
                    "Perubahan 24h": f"{best_pair.get('priceChange', {}).get('h24', 0)}%",
                    "Likuiditas": f"${best_pair['liquidity']['usd']:,.0f}",
                    "Volume": f"${best_pair['volume']['h24']:,.0f}",
                    "Jaringan": best_pair['chainId'].upper(),
                    "Contract Address": best_pair['baseToken']['address'],
                    "Link": best_pair['url']
                }
                # Tambahkan Skor Listing
                data["Score"] = calculate_listing_score(data)
                results.append(data)
        except:
            continue
    return results

# --- 5. UI UTAMA ---
st.title("⚡ Meme-Watch Ultra-Auto 2026")
st.write(f"Sistem bekerja otomatis memantau Blockchain • **Live: {datetime.datetime.now().strftime('%H:%M:%S')}**")

# TARGET LIST (Smart Money Targets)
target_list = ["PIPPIN", "GOAT", "PENGU", "SPX6900", "FARTCOIN", "MOCHI", "POPCAT", "PNUT", "MOODENG", "BRETT"]
live_data = fetch_trending_data(target_list)

if live_data:
    df = pd.DataFrame(live_data)

    # --- BAGIAN 1: TOP CANDIDATES (METRICS) ---
    st.header("🎯 Kandidat Listing Tier-1")
    top_score = df.sort_values(by="Score", ascending=False).head(3)
    cols = st.columns(3)
    
    for i, (_, row) in enumerate(top_score.iterrows()):
        with cols[i]:
            color = "green" if row['Score'] >= 80 else "orange"
            st.metric(
                label=f"{row['Koin']} (Score: {row['Score']}%)", 
                value=row['Harga'], 
                delta=f"{row['Perubahan 24h']} | {row['Status'] if 'Status' in row else ''}"
            )
            if row['Score'] >= 80:
                st.success("🔥 SANGAT KUAT UNTUK LISTING")
            else:
                st.info("📈 Akumulasi Sedang Berlangsung")

    st.divider()

    # --- BAGIAN 2: MARKET OVERVIEW TABLE ---
    st.header("📋 Monitoring Smart Money (Real-Time)")
    # Beri warna pada baris yang memiliki score tinggi menggunakan styling
    st.dataframe(
        df[['Koin', 'Score', 'Harga', 'Perubahan 24h', 'Volume', 'Likuiditas', 'Jaringan', 'Contract Address']],
        use_container_width=True,
        hide_index=True
    )

    # --- BAGIAN 3: UTILITAS TOOLS (EXPANDER) ---
    st.subheader("🔗 Kontrol & Analisis Keamanan")
    col_tools1, col_tools2 = st.columns(2)
    
    for i, row in df.iterrows():
        target_col = col_tools1 if i % 2 == 0 else col_tools2
        with target_col.expander(f"Opsi Cepat {row['Koin']}"):
            st.write(f"**Contract:** `{row['Contract Address']}`")
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"[📈 Grafik]({row['Link']})")
            c2.markdown(f"[🛡️ RugCheck](https://www.rugcheck.xyz/mainnet/token/{row['Contract Address']})")
            c3.markdown(f"[🔍 BubbleMaps](https://bubblemaps.io/eth/token/{row['Contract Address']})")

# --- 6. SIDEBAR: SMART MONITORING ---
st.sidebar.header("🕵️ Whale Activity")
st.sidebar.markdown("Status Dompet Smart Money:")

# Dummy data for Whale Activity (Bisa diupgrade ke API Helius/Alchemy)
st.sidebar.code("6u3y... (Sniper): 🟢 BUYING", language="text")
st.sidebar.code("0x7a... (Whale): 🔴 SELLING", language="text")
st.sidebar.code("G6rX... (Insider): 🟡 HOLDING", language="text")

st.sidebar.divider()
st.sidebar.header("🔍 Scan Koin Custom")
new_coin = st.sidebar.text_input("Simbol/CA:")
if new_coin:
    custom_res = fetch_trending_data([new_coin])
    if custom_res:
        st.sidebar.success(f"Ditemukan: {custom_res[0]['Koin']}")
        st.sidebar.write(f"Harga: {custom_res[0]['Harga']}")
        st.sidebar.write(f"Score: {custom_res[0]['Score']}%")
    else:
        st.sidebar.error("Tidak ditemukan.")

if st.sidebar.button("🔄 Paksa Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# --- FOOTER ---
st.divider()
st.caption("Meme-Watch Ultra 2026 • Gunakan data ini sebagai referensi, bukan saran finansial (DYOR).")
