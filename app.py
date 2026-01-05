import streamlit as st
import pandas as pd
import requests

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Meme-Watch Ultra 2026", layout="wide", page_icon="⚡")

# --- CSS UNTUK TAMPILAN PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI SEARCH AUTOMATIC DATA ---
@st.cache_data(ttl=60) # Data otomatis refresh setiap 1 menit
def fetch_trending_data(symbols):
    results = []
    for sym in symbols:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={sym}"
            res = requests.get(url).json()
            pairs = res.get('pairs', [])
            if pairs:
                # Ambil pair dengan likuiditas tertinggi untuk menghindari scam
                best_pair = max(pairs, key=lambda x: x.get('liquidity', {}).get('usd', 0))
                results.append({
                    "Koin": best_pair['baseToken']['symbol'],
                    "Harga": f"${float(best_pair['priceUsd']):.6f}",
                    "Perubahan 24h": f"{best_pair.get('priceChange', {}).get('h24', 0)}%",
                    "Likuiditas": f"${best_pair['liquidity']['usd']:,.0f}",
                    "Volume": f"${best_pair['volume']['h24']:,.0f}",
                    "Jaringan": best_pair['chainId'].upper(),
                    "Contract Address": best_pair['baseToken']['address'],
                    "Link": best_pair['url']
                })
        except:
            continue
    return results

# --- DATA AWAL (DAFTAR SMART MONEY TARGET) ---
target_list = ["PIPPIN", "GOAT", "PENGU", "SPX6900", "FARTCOIN", "MOCHI", "POPCAT", "PNUT", "MOODENG", "BRETT"]

# --- UI UTAMA ---
st.title("⚡ Meme-Watch Ultra-Auto 2026")
st.write(f"Sistem bekerja otomatis memantau Blockchain • **Live: {pd.Timestamp.now().strftime('%H:%M:%S')}**")

# 1. LIVE PERFORMANCE METRICS
st.header("📊 Performa Pasar Real-Time")
live_data = fetch_trending_data(target_list)

if live_data:
    df = pd.DataFrame(live_data)
    
    # Tampilkan 3 Koin Terbaik di Baris Atas
    top_3 = df.sort_values(by="Perubahan 24h", ascending=False).head(3)
    cols = st.columns(3)
    for i, (_, row) in enumerate(top_3.iterrows()):
        with cols[i]:
            st.metric(label=f"{row['Koin']} ({row['Jaringan']})", value=row['Harga'], delta=row['Perubahan 24h'])
            st.caption(f"Liq: {row['Likuiditas']}")

    st.divider()

    # 2. TABEL OTOMATIS LENGKAP
    st.header("📋 Daftar Pantauan Smart Money (Auto-Update)")
    st.dataframe(
        df[['Koin', 'Jaringan', 'Harga', 'Perubahan 24h', 'Volume', 'Likuiditas', 'Contract Address']],
        use_container_width=True,
        hide_index=True
    )

    # 3. LINK COPY CONTRACT (MEMUDAHKAN SWAP DI HP)
    st.subheader("🔗 Salin Kontrak & Analisis")
    for _, row in df.iterrows():
        with st.expander(f"Opsi untuk {row['Koin']}"):
            st.code(row['Contract Address'], language="text")
            st.markdown(f"[📈 Lihat Grafik Real-Time]({row['Link']})")
            st.markdown(f"[🛡️ Cek Keamanan (RugCheck)](https://www.rugcheck.xyz/mainnet/token/{row['Contract Address']})")

# 4. FITUR TAMBAH KOIN MANUAL (SIDEBAR)
st.sidebar.header("🔍 Cari Koin Baru")
new_coin = st.sidebar.text_input("Ketik Nama/Simbol Koin:")
if new_coin:
    custom_res = fetch_trending_data([new_coin])
    if custom_res:
        st.sidebar.success(f"Ditemukan: {custom_res[0]['Harga']}")
        st.sidebar.write(f"CA: `{custom_res[0]['Contract Address']}`")
    else:
        st.sidebar.error("Koin tidak ditemukan.")

st.sidebar.divider()
if st.sidebar.button("🔄 Paksa Update Data"):
    st.cache_data.clear()
    st.rerun()

# --- FOOTER ---
st.divider()
st.info("💡 **Tips Android:** Buka aplikasi ini di Chrome HP, pilih 'Instal Aplikasi' agar muncul di menu HP Anda tanpa bar browser.")
