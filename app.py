import streamlit as st
import pickle
import pandas as pd

# Load model dan dataframe
# pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

st.title("Prediksi Harga Laptop 💻")
st.write("Masukkan spesifikasi laptop di bawah ini untuk mengetahui estimasi harganya.")

# Layout menggunakan kolom agar terlihat lebih rapi
col1, col2 = st.columns(2)

with col1:
    # Mengambil pilihan brand dari dataset
    brand = st.selectbox('Pilih Brand', df['Brand'].unique())
    
    # Slider untuk kecepatan prosesor (GHz), berdasarkan data minimal ~1.5 max ~4.0
    processor_speed = st.slider('Kecepatan Prosesor (GHz)', min_value=1.0, max_value=5.0, value=2.5, step=0.1)
    
    # Pilihan RAM Size yang ada di data (4, 8, 16, 32)
    ram_size = st.selectbox('Kapasitas RAM (GB)', sorted(df['RAM_Size'].unique()))

with col2:
    # Pilihan Storage yang ada di data (256, 512, 1000)
    storage = st.selectbox('Kapasitas Storage (GB)', sorted(df['Storage_Capacity'].unique()))
    
    # Slider untuk ukuran layar (inch), berdasarkan data minimal ~11 max ~17
    screen_size = st.slider('Ukuran Layar (Inch)', min_value=10.0, max_value=18.0, value=14.0, step=0.1)
    
    # Slider untuk berat (Kg), berdasarkan data minimal ~2 max ~5
    weight = st.slider('Berat Laptop (Kg)', min_value=1.0, max_value=6.0, value=2.5, step=0.1)

# Tombol Prediksi (Harus rata kiri)
if st.button('Hitung Estimasi Harga'):
    # Isi dari if harus menjorok ke dalam
    query = pd.DataFrame([[brand, processor_speed, ram_size, storage, screen_size, weight]], 
                         columns=['Brand', 'Processor_Speed', 'RAM_Size', 'Storage_Capacity', 'Screen_Size', 'Weight'])
    
    # Melakukan prediksi
    prediction = pipe.predict(query)[0]
    
    # Menampilkan hasil
    st.success(f"Estimasi Harga Laptop: **$ {round(prediction, 2):,}**")
