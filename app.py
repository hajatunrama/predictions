import streamlit as st
import pickle
import pandas as pd

# 1. Pengaturan Halaman (Harus di baris paling atas)
st.set_page_config(
    page_title="Kalkulator Harga Laptop",
    page_icon="💻",
    layout="wide"
)

# 2. Mengambil Model dari file .pkl (pakai cache agar loading web lebih cepat)
@st.cache_resource
def load_model():
    pipe = pickle.load(open('pipe.pkl', 'rb'))
    df = pickle.load(open('df.pkl', 'rb'))
    return pipe, df

pipe, df = load_model()

# 3. SIDEBAR: Panduan Penggunaan
with st.sidebar:
    st.header("📖 Cara Penggunaan")
    st.markdown("""
    Selamat datang di Kalkulator Harga Laptop cerdas!
    
    **Langkah-langkah:**
    1. Pilih **Brand** dan kapasitas **RAM/Storage** di kolom kiri.
    2. Sesuaikan **Kecepatan Prosesor**, **Ukuran Layar**, dan **Berat** di kolom kanan.
    3. Klik tombol **Hitung Estimasi Harga**.
    """)
    
    st.markdown("---")
    st.info("🤖 **Info AI:** Sistem ini ditenagai oleh algoritma *Machine Learning* (Random Forest) yang telah mempelajari ribuan data harga laptop di pasaran untuk memberikan estimasi paling akurat.")

# 4. HALAMAN UTAMA
st.title("💻 Prediksi Harga Laptop & PC")
st.markdown("Cari tahu estimasi harga laptop impianmu berdasarkan spesifikasinya sebelum membeli!")
st.markdown("---")

# 5. Membagi form menjadi 2 kolom agar tidak memanjang ke bawah
col1, col2 = st.columns(2)

with col1:
    st.subheader("⚙️ Spesifikasi Utama")
    # Mengambil pilihan dari dataset
    brand = st.selectbox('Pilih Brand / Merek', sorted(df['Brand'].unique()))
    ram_size = st.selectbox('Kapasitas RAM (GB)', sorted(df['RAM_Size'].unique()))
    storage = st.selectbox('Kapasitas Storage / SSD (GB)', sorted(df['Storage_Capacity'].unique()))

with col2:
    st.subheader("📏 Dimensi & Performa")
    processor_speed = st.slider('Kecepatan Prosesor (GHz)', min_value=1.0, max_value=5.0, value=2.5, step=0.1)
    screen_size = st.slider('Ukuran Layar (Inch)', min_value=10.0, max_value=18.0, value=14.0, step=0.1)
    weight = st.slider('Berat Laptop (Kg)', min_value=1.0, max_value=6.0, value=2.0, step=0.1)

st.markdown("---")

# 6. Tombol Eksekusi
if st.button('🚀 Hitung Estimasi Harga', use_container_width=True):
    # Animasi loading singkat biar terasa lebih interaktif
    with st.spinner('Menghitung estimasi harga menggunakan AI...'):
        # Membuat array data frame persis seperti struktur saat training
        query = pd.DataFrame([[brand, processor_speed, ram_size, storage, screen_size, weight]], 
                             columns=['Brand', 'Processor_Speed', 'RAM_Size', 'Storage_Capacity', 'Screen_Size', 'Weight'])
        
        # Melakukan prediksi
        prediction = pipe.predict(query)[0]
        
    # Menampilkan hasil dengan gaya "Metric" yang besar dan menonjol
    st.success("Perhitungan selesai!")
    st.metric(label="Estimasi Harga di Pasaran:", value=f"$ {round(prediction, 2):,}")
    
    # Catatan tambahan di bawah hasil
    st.caption("*Harga di atas adalah estimasi yang dihitung secara otomatis oleh sistem kecerdasan buatan. Harga asli di lapangan mungkin sedikit berbeda.*")
