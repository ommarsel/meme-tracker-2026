import streamlit as st
import pandas as pd

# Judul Aplikasi
st.set_page_config(page_title="Meme-Watch 2026 Insider", layout="wide")
st.title("🚀 Meme-Watch 2026: Smart Money Tracker")

# 1. Dashboard Watchlist Listing
st.header("📋 Watchlist Listing Bursa Besar")
data_listing = {
    "Koin": ["PIPPIN", "PENGU", "GOAT", "MOCHI", "SPX6900", "PNUT", "SUDENG", "FARTCOIN", "MIU", "BRETT"],
    "Jaringan": ["Solana", "Ethereum", "Solana", "Base", "Eth/Sol", "Solana", "Sui", "Solana", "Sui", "Base"],
    "Potensi Listing": ["Sangat Tinggi", "Tinggi (Coinbase)", "Sangat Tinggi", "Tinggi (Base)", "Global Expansion", "Medium", "High (Sui Eco)", "Medium", "High", "High"],
    "Status Smart Money": ["Akumulasi", "Holding", "Accumulation", "Whale Buy", "Stable", "Re-entry", "Accumulation", "Day Trading", "Holding", "Holding"]
}
df_listing = pd.DataFrame(data_listing)
st.table(df_listing)

# 2. Database Alamat Dompet Smart Money (BARU)
st.header("🐋 Smart Money Wallet Watchlist")
st.write("Pantau dompet ini di Arkham atau Explorer untuk melihat apa yang mereka beli selanjutnya.")

smart_money_data = {
    "Nama Whale": ["Pippin OG Whale", "Goat Alpha Trader", "SPX Institutional", "Sui Meme Hunter"],
    "Network": ["Solana", "Solana", "Ethereum", "Sui"],
    "Address": [
        "7nB8...v4Yh (Copy to Arkham)", 
        "49bk...k92p (Copy to Arkham)", 
        "0x3d...dE4f (Copy to Arkham)",
        "0x7b...31ae (Copy to Arkham)"
    ],
    "Cek Transaksi": [
        "https://solscan.io/", 
        "https://solscan.io/", 
        "https://etherscan.io/",
        "https://suiscan.xyz/"
    ]
}
df_smart = pd.DataFrame(smart_money_data)
st.dataframe(df_smart, use_container_width=True)

# 3. Alat Pantau Eksternal
st.header("🔍 Alat Investigasi On-Chain")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("Arkham Intelligence")
    st.markdown("[Buka Arkham](https://platform.arkhamintelligence.com/)")
with col2:
    st.info("Bubblemaps (Struktur Holder)")
    st.markdown("[Buka Bubblemaps](https://bubblemaps.io/)")
with col3:
    st.info("DexScreener (Real-time Chart)")
    st.markdown("[Buka DexScreener](https://dexscreener.com/)")

# 4. Form Peringatan (Simulasi)
st.sidebar.header("🔔 Atur Notifikasi")
target_coin = st.sidebar.selectbox("Pilih Koin:", df_listing["Koin"])
alert_type = st.sidebar.radio("Tipe Alert:", ["Listing Baru", "Whale Buy > $50k", "Harga Naik 20%"])

if st.sidebar.button("Aktifkan Alert"):
    st.sidebar.success(f"Alert untuk {target_coin} ({alert_type}) AKTIF!")

# 5. Tips Keamanan
st.warning("⚠️ Tips: Jika dompet Whale di atas tiba-tiba mengirim koin dalam jumlah besar ke Bursa (Binance/Bybit), itu tandanya mereka akan JUAL (Take Profit).")
