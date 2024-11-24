import streamlit as st  # Mengimpor Streamlit untuk membangun aplikasi web
import pandas as pd  # Mengimpor pandas untuk manipulasi data
import matplotlib.pyplot as plt  # Mengimpor matplotlib untuk pembuatan grafik
import seaborn as sns  # Mengimpor seaborn untuk visualisasi yang lebih baik

# Mendefinisikan path file data untuk file hour.csv dan day.csv
hour_data_path = 'dashboard/hour.csv'
day_data_path = 'dashboard/day.csv'

# Fungsi untuk memuat data dari file CSV
def load_data():
    hour_data = pd.read_csv(hour_data_path)  # Membaca data dari 'hour.csv'
    day_data = pd.read_csv(day_data_path)  # Membaca data dari 'day.csv'
    return hour_data, day_data  # Mengembalikan kedua data

# Fungsi untuk membuat visualisasi berdasarkan musim dan kondisi cuaca
def plot_usage_by_season_weather(data):
    data['cnt'] = pd.to_numeric(data['cnt'], errors='coerce')  # Mengubah kolom 'cnt' menjadi tipe numerik
    if data['cnt'].isnull().any():  # Memeriksa jika ada nilai yang hilang
        st.warning("Data 'cnt' mengandung nilai yang hilang. Mengisi nilai yang hilang dengan 0.")  # Peringatan jika ada data yang hilang
        data['cnt'] = data['cnt'].fillna(0)  # Mengisi nilai yang hilang dengan 0
    season_dict = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}  # Pemetaan angka ke musim
    weather_dict = {1: 'Clear', 2: 'Mist + Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}  # Pemetaan angka ke kondisi cuaca
    data['season'] = data['season'].map(season_dict)  # Mengubah angka musim menjadi nama musim
    data['weathersit'] = data['weathersit'].map(weather_dict)  # Mengubah angka cuaca menjadi nama cuaca
    season_weather_counts = data.groupby(['season', 'weathersit'])['cnt'].sum().unstack()  # Mengelompokkan data dan menghitung total penyewaan berdasarkan musim dan cuaca
    if season_weather_counts.isnull().all().all():  # Memeriksa apakah ada data yang bisa dipetakan
        st.warning("Tidak ada data untuk dipetakan. Pastikan data valid.")  # Peringatan jika tidak ada data yang dapat dipetakan
        return
    # Membuat grafik batang untuk visualisasi
    season_weather_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=['skyblue', 'lightcoral', 'orange', 'lightgreen'])
    plt.title('Pola Penggunaan Sepeda Berdasarkan Musim dan Kondisi Cuaca')  # Menambahkan judul grafik
    plt.xlabel('Musim')  # Menambahkan label sumbu X
    plt.ylabel('Jumlah Penyewaan')  # Menambahkan label sumbu Y
    plt.xticks(rotation=45)  # Memutar label sumbu X agar tidak saling tumpang tindih
    st.pyplot(plt)  # Menampilkan grafik

# Fungsi untuk membuat visualisasi jumlah penyewaan sepeda per jam
def plot_by_hour(data):
    data['hr'] = data['hr'].astype(int)  # Mengonversi kolom jam ('hr') menjadi integer
    hourly_counts = data.groupby('hr').size()  # Menghitung jumlah penyewaan per jam
    if hourly_counts.empty:  # Memeriksa apakah ada data untuk plot
        st.warning("Tidak ada data untuk plot jumlah penyewaan per jam.")  # Peringatan jika tidak ada data
        return
    # Membuat grafik garis untuk jumlah penyewaan per jam
    plt.figure(figsize=(8, 5))
    hourly_counts.plot(kind='line', marker='o', color='orange')
    plt.title('Jumlah Penyewaan Sepeda per Jam')  # Menambahkan judul grafik
    plt.xlabel('Jam')  # Menambahkan label sumbu X
    plt.ylabel('Jumlah Penyewaan')  # Menambahkan label sumbu Y
    st.pyplot(plt)  # Menampilkan grafik

# Fungsi untuk membuat visualisasi jumlah penyewaan berdasarkan jenis hari (Holiday, Weekend, Workingday)
def plot_by_day_type(data):
    # Menentukan jenis hari berdasarkan kolom 'holiday' dan 'workingday'
    data['day_type'] = data.apply(lambda row: 'Holiday' if row['holiday'] == 1 else ('Weekend' if row['workingday'] == 0 else 'Workingday'), axis=1)
    day_type_counts = data['day_type'].value_counts()  # Menghitung jumlah penyewaan berdasarkan jenis hari
    if day_type_counts.empty:  # Memeriksa apakah ada data untuk plot
        st.warning("Tidak ada data untuk plot jumlah penyewaan berdasarkan jenis hari.")  # Peringatan jika tidak ada data
        return
    # Membuat grafik batang untuk jumlah penyewaan berdasarkan jenis hari
    plt.figure(figsize=(8, 5))
    day_type_counts.plot(kind='bar', color=['lightcoral', 'lightgreen', 'skyblue'])
    plt.title('Jumlah Penyewaan Sepeda Berdasarkan Jenis Hari')  # Menambahkan judul grafik
    plt.xlabel('Jenis Hari')  # Menambahkan label sumbu X
    plt.ylabel('Jumlah Penyewaan')  # Menambahkan label sumbu Y
    st.pyplot(plt)  # Menampilkan grafik

# Fungsi untuk membandingkan penggunaan sepeda antara pengguna terdaftar dan kasual berdasarkan jenis hari
def plot_usage_by_user_type_and_day_type(data):
    # Menentukan jenis hari (Weekend atau Workingday)
    data['day_type'] = data.apply(lambda row: 'Weekend' if row['workingday'] == 0 else 'Workingday', axis=1)
    user_type_day_counts = data.groupby(['day_type'])[['casual', 'registered']].sum()  # Mengelompokkan berdasarkan jenis hari dan menghitung jumlah penyewaan oleh pengguna kasual dan terdaftar
    if user_type_day_counts.empty:  # Memeriksa apakah ada data untuk plot
        st.warning("Tidak ada data untuk plot perbandingan penggunaan sepeda.")  # Peringatan jika tidak ada data
        return
    # Membuat grafik batang untuk perbandingan antara pengguna kasual dan terdaftar
    user_type_day_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=['skyblue', 'lightcoral'])
    plt.title('Perbandingan Penggunaan Sepeda: Pengguna Terdaftar vs Kasual per Jenis Hari')  # Menambahkan judul grafik
    plt.xlabel('Jenis Hari')  # Menambahkan label sumbu X
    plt.ylabel('Jumlah Penyewaan')  # Menambahkan label sumbu Y
    plt.xticks(rotation=0)  # Memutar label sumbu X agar tidak saling tumpang tindih
    st.pyplot(plt)  # Menampilkan grafik

# Fungsi untuk melakukan RFM Analysis (Recency, Frequency, Monetary)
def rfm_analysis(data):
    data['dteday'] = pd.to_datetime(data['dteday'])  # Mengonversi kolom 'dteday' menjadi format datetime
    today = data['dteday'].max()  # Menentukan tanggal terakhir dalam data
    data['Recency'] = (today - data['dteday']).dt.days  # Menghitung Recency (hari sejak penyewaan terakhir)
    frequency = data.groupby('casual')['cnt'].count()  # Menghitung jumlah penyewaan per pengguna kasual
    monetary = data.groupby('casual')['cnt'].sum()  # Menghitung total penyewaan per pengguna kasual
    # Membuat DataFrame untuk RFM Analysis
    rfm_df = pd.DataFrame({
        'Recency': data.groupby('casual')['Recency'].min(),  # Mengambil nilai Recency untuk setiap pengguna kasual
        'Frequency': frequency,  # Mengambil nilai Frequency untuk setiap pengguna kasual
        'Monetary': monetary  # Mengambil nilai Monetary untuk setiap pengguna kasual
    }).reset_index()  # Reset index untuk DataFrame yang lebih rapi
    st.header("RFM Analysis")  # Menambahkan header RFM Analysis
    st.dataframe(rfm_df)  # Menampilkan DataFrame RFM Analysis
    fig, ax = plt.subplots(figsize=(10, 6))  # Membuat grafik scatter
    ax.scatter(rfm_df['Recency'], rfm_df['Frequency'], c=rfm_df['Monetary'], cmap='viridis')  # Scatter plot RFM (Recency vs Frequency)
    ax.set_title("RFM Analysis (Recency vs Frequency)")  # Menambahkan judul grafik
    ax.set_xlabel('Recency (Days Since Last Rental)')  # Menambahkan label sumbu X
    ax.set_ylabel('Frequency (Number of Rentals)')  # Menambahkan label sumbu Y
    st.pyplot(fig)  # Menampilkan grafik

# Fungsi untuk memfilter data berdasarkan rentang tanggal
def date_filter(data):
    data['dteday'] = pd.to_datetime(data['dteday'])  # Mengonversi kolom 'dteday' menjadi format datetime
    start_date = st.date_input("Pilih Tanggal Mulai", data['dteday'].min().date())  # Input tanggal mulai
    end_date = st.date_input("Pilih Tanggal Akhir", data['dteday'].max().date())  # Input tanggal akhir
    filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]  # Filter data sesuai tanggal
    return filtered_data  # Mengembalikan data yang sudah difilter

# Memuat data dari kedua file CSV
hour_data, day_data = load_data()

st.title('Visualisasi Data Penyewaan Sepeda')  # Menambahkan judul aplikasi

# Pilihan untuk memilih antara data per jam atau per hari
data_type = st.radio("Pilih Tipe Data", ("Hour Data", "Day Data"))

# Kondisi untuk menampilkan visualisasi dan analisis berdasarkan data yang dipilih
if data_type == "Day Data":
    filtered_data = date_filter(day_data)  # Menggunakan data harian yang sudah difilter
    st.header("Tabel Data Penyewaan Sepeda (Day Data) - Filtered")  # Menambahkan header tabel data
    st.dataframe(filtered_data)  # Menampilkan tabel data
    col1, col2 = st.columns(2)  # Membuat dua kolom untuk menampilkan grafik
    with col1:
        st.header("Pola Penggunaan Sepeda Berdasarkan Musim dan Kondisi Cuaca")
        plot_usage_by_season_weather(filtered_data)  # Menampilkan grafik pola penggunaan sepeda berdasarkan musim dan cuaca
    with col2:
        st.header("Perbandingan Penggunaan Sepeda: Pengguna Terdaftar vs Kasual per Jenis Hari")
        plot_usage_by_user_type_and_day_type(filtered_data)  # Menampilkan grafik perbandingan pengguna sepeda
    st.header("Analisis Lanjutan")  # Menambahkan header analisis lanjutan
    st.subheader("RFM Analysis")  # Menambahkan subheader RFM Analysis
    rfm_analysis(filtered_data)  # Menampilkan hasil RFM Analysis

elif data_type == "Hour Data":
    filtered_data = date_filter(hour_data)  # Menggunakan data per jam yang sudah difilter
    st.header("Tabel Data Penyewaan Sepeda (Hour Data) - Filtered")  # Menambahkan header tabel data
    st.dataframe(filtered_data)  # Menampilkan tabel data
    col1, col2 = st.columns(2)  # Membuat dua kolom untuk menampilkan grafik
    with col1:
        st.header("Jumlah Penyewaan per Jam")
        plot_by_hour(filtered_data)  # Menampilkan grafik jumlah penyewaan per jam
    with col2:
        st.header("Jumlah Penyewaan Berdasarkan Jenis Hari")
        plot_by_day_type(filtered_data)  # Menampilkan grafik jumlah penyewaan berdasarkan jenis hari
