import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Mendefinisikan path file data untuk file hour.csv dan day.csv
hour_data_path = 'hour.csv'
day_data_path = 'day.csv'

# Fungsi untuk memuat data dari file CSV dengan penanganan error
def load_data():
    if os.path.exists(hour_data_path) and os.path.exists(day_data_path):
        hour_data = pd.read_csv(hour_data_path)  # Membaca data dari 'hour.csv'
        day_data = pd.read_csv(day_data_path)  # Membaca data dari 'day.csv'
        return hour_data, day_data  # Mengembalikan kedua data
    else:
        st.error("File CSV tidak ditemukan. Pastikan file 'hour.csv' dan 'day.csv' ada di direktori yang benar.")
        return None, None

# Fungsi untuk membuat visualisasi berdasarkan musim dan kondisi cuaca
def plot_usage_by_season_weather(data):
    data['cnt'] = pd.to_numeric(data['cnt'], errors='coerce')
    if data['cnt'].isnull().any():
        st.warning("Data 'cnt' mengandung nilai yang hilang. Mengisi nilai yang hilang dengan 0.")
        data['cnt'] = data['cnt'].fillna(0)
    season_dict = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    weather_dict = {1: 'Clear', 2: 'Mist + Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
    data['season'] = data['season'].map(season_dict)
    data['weathersit'] = data['weathersit'].map(weather_dict)
    season_weather_counts = data.groupby(['season', 'weathersit'])['cnt'].sum().unstack()
    if season_weather_counts.isnull().all().all():
        st.warning("Tidak ada data untuk dipetakan. Pastikan data valid.")
        return
    season_weather_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=['skyblue', 'lightcoral', 'orange', 'lightgreen'])
    plt.title('Pola Penggunaan Sepeda Berdasarkan Musim dan Kondisi Cuaca')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Penyewaan')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Fungsi untuk memfilter data berdasarkan rentang tanggal
def date_filter(data):
    data['dteday'] = pd.to_datetime(data['dteday'])
    start_date = st.date_input("Pilih Tanggal Mulai", data['dteday'].min().date())
    end_date = st.date_input("Pilih Tanggal Akhir", data['dteday'].max().date())
    filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]
    return filtered_data

# Memuat data dari kedua file CSV
hour_data, day_data = load_data()

if hour_data is not None and day_data is not None:
    st.title('Visualisasi Data Penyewaan Sepeda')

    data_type = st.radio("Pilih Tipe Data", ("Hour Data", "Day Data"))

    if data_type == "Day Data":
        filtered_data = date_filter(day_data)
        st.header("Tabel Data Penyewaan Sepeda (Day Data) - Filtered")
        st.dataframe(filtered_data)
        col1, col2 = st.columns(2)
        with col1:
            st.header("Pola Penggunaan Sepeda Berdasarkan Musim dan Kondisi Cuaca")
            plot_usage_by_season_weather(filtered_data)
        with col2:
            st.header("Perbandingan Penggunaan Sepeda: Pengguna Terdaftar vs Kasual per Jenis Hari")
            plot_usage_by_user_type_and_day_type(filtered_data)
        st.header("Analisis Lanjutan")
        st.subheader("RFM Analysis")
        rfm_analysis(filtered_data)

    elif data_type == "Hour Data":
        filtered_data = date_filter(hour_data)
        st.header("Tabel Data Penyewaan Sepeda (Hour Data) - Filtered")
        st.dataframe(filtered_data)
        col1, col2 = st.columns(2)
        with col1:
            st.header("Jumlah Penyewaan per Jam")
            plot_by_hour(filtered_data)
        with col2:
            st.header("Jumlah Penyewaan Berdasarkan Jenis Hari")
            plot_by_day_type(filtered_data)
