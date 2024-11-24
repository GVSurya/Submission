import streamlit as st  # Mengimpor Streamlit untuk membangun aplikasi web
import pandas as pd  # Mengimpor pandas untuk manipulasi data
import matplotlib.pyplot as plt  # Mengimpor matplotlib untuk pembuatan grafik
import seaborn as sns  # Mengimpor seaborn untuk visualisasi yang lebih baik

# Mendefinisikan path file data untuk file hour.csv dan day.csv
hour_data_path = 'hour.csv'
day_data_path = 'day.csv'

# Fungsi untuk memuat data dari file CSV
def load_data():
    hour_data = pd.read_csv(hour_data_path)  # Membaca data dari 'hour.csv'
    day_data = pd.read_csv(day_data_path)  # Membaca data dari 'day.csv'
    return hour_data, day_data  # Mengembalikan kedua data

# Fungsi untuk memfilter data berdasarkan rentang tanggal
def date_filter(data):
    data['dteday'] = pd.to_datetime(data['dteday'])  # Mengonversi kolom 'dteday' menjadi format datetime
    start_date = st.date_input("Pilih Tanggal Mulai", data['dteday'].min().date())  # Input tanggal mulai
    end_date = st.date_input("Pilih Tanggal Akhir", data['dteday'].max().date())  # Input tanggal akhir
    filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]  # Filter data sesuai tanggal
    return filtered_data  # Mengembalikan data yang sudah difilter

# Fungsi untuk membuat visualisasi berdasarkan musim dan kondisi cuaca
def plot_usage_by_season_weather(data):
    # Mengelompokkan data berdasarkan musim (season) dan kondisi cuaca (weathersit), lalu menjumlahkan total penggunaan sepeda (cnt)
    season_weather_usage = data.groupby(['season', 'weathersit'])['cnt'].sum().reset_index()

    # Membuat figure (area plot) dengan ukuran 10x6 inci.
    plt.figure(figsize=(10,6))

    # Membuat bar plot menggunakan seaborn
    sns.barplot(x='season', y='cnt', hue='weathersit', data=season_weather_usage, palette="viridis")

    # Menambahkan judul plot
    plt.title("Pola Penggunaan Sepeda Berdasarkan Musim dan Kondisi Cuaca")

    # Menambahkan label sumbu x
    plt.xlabel("Season")

    # Menambahkan label sumbu y
    plt.ylabel("Jumlah Penggunaan Sepeda")

    # Menambahkan legend (keterangan)
    plt.legend(title="Kondisi Cuaca", loc='upper left')

    # Menampilkan plot
    st.pyplot(plt)


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
    # Menentukan jenis hari berdasarkan kolom 'workingday'
    data['is_working_day'] = data['workingday'].apply(lambda x: 'Weekday' if x == 1 else 'Weekend')

    # Mengelompokkan data berdasarkan jenis hari, pengguna kasual dan terdaftar
    usage_by_day_type = data.groupby(['is_working_day', 'casual', 'registered'])['cnt'].sum().reset_index()

    # Mengubah format data untuk visualisasi
    usage_by_day_type = usage_by_day_type.melt(id_vars=['is_working_day'], value_vars=['casual', 'registered'], 
                                               var_name='user_type', value_name='usage_count')

    # Membuat figure (bar plot) dengan ukuran 12x6 inci
    plt.figure(figsize=(12, 6))

    # Membuat bar plot menggunakan seaborn
    sns.barplot(x='is_working_day', y='usage_count', hue='user_type', data=usage_by_day_type, palette='muted')

    # Menambahkan judul plot
    plt.title('Perbandingan Penggunaan Sepeda: Pengguna Terdaftar vs Kasual per Jenis Hari')

    # Menambahkan label sumbu x
    plt.xlabel('Jenis Hari (Hari Kerja vs Akhir Pekan)')

    # Menambahkan label sumbu y
    plt.ylabel('Jumlah Penggunaan Sepeda')

    # Menambahkan legend
    plt.legend(title='Jenis Pengguna', loc='upper left')

    # Menampilkan plot
    st.pyplot(plt)

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
    
    # Menampilkan RFM Analysis
    st.header("RFM Analysis")
    st.dataframe(rfm_df)  # Menampilkan DataFrame RFM Analysis
    
    # Membuat scatter plot untuk RFM Analysis (Recency vs Frequency)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(rfm_df['Recency'], rfm_df['Frequency'], c=rfm_df['Monetary'], cmap='viridis')
    ax.set_title("RFM Analysis (Recency vs Frequency)")  # Menambahkan judul grafik
    ax.set_xlabel('Recency (Days Since Last Rental)')  # Menambahkan label sumbu X
    ax.set_ylabel('Frequency (Number of Rentals)')  # Menambahkan label sumbu Y
    st.pyplot(fig)  # Menampilkan grafik

# Memuat data dari kedua file CSV
hour_data, day_data = load_data()

st.title('Visualisasi Data Penyewaan Sepeda')  # Menambahkan judul aplikasi

# Pilihan untuk memilih antara data per jam atau per hari
option = st.selectbox("Pilih Data untuk Visualisasi", ["Hour Data", "Day Data"])

# Memilih data berdasarkan input pengguna
if option == "Hour Data":
    # Memilih dan menampilkan visualisasi berdasarkan data per jam
    filtered_hour_data = date_filter(hour_data)
    st.header("Tabel Data Penyewaan Sepeda (Hour Data) - Filtered")
    st.dataframe(filtered_hour_data)  # Menampilkan tabel data per jam yang sudah difilter
    plot_by_hour(filtered_hour_data)
    plot_usage_by_season_weather(filtered_hour_data)
    plot_usage_by_user_type_and_day_type(filtered_hour_data)
elif option == "Day Data":
    # Memilih dan menampilkan visualisasi berdasarkan data per hari
    filtered_day_data = date_filter(day_data)
    st.header("Tabel Data Penyewaan Sepeda (Day Data) - Filtered")
    st.dataframe(filtered_day_data)  # Menampilkan tabel data per hari yang sudah difilter
    plot_by_day_type(filtered_day_data)
    plot_usage_by_season_weather(filtered_day_data)
    plot_usage_by_user_type_and_day_type(filtered_day_data)

# Menambahkan RFM Analysis
rfm_analysis(hour_data)  # Melakukan RFM Analysis pada data per jam

