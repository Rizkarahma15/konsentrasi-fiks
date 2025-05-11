import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi regresi
def calculate_regression_equation(X, Y, var_name_x='x', var_name_y='y'):
    n = len(X)
    if n < 2:
        raise ValueError("Jumlah data harus minimal 2 titik.")

    sum_x = np.sum(X)
    sum_y = np.sum(Y)
    sum_xy = np.sum(X * Y)
    sum_x_squared = np.sum(X**2)
    sum_y_squared = np.sum(Y**2)

    denominator = (n * sum_x_squared - sum_x**2)
    if denominator == 0:
        raise ZeroDivisionError("Pembagi dalam perhitungan slope bernilai nol. Pastikan data X tidak sama semua.")

    b = (n * sum_xy - sum_x * sum_y) / denominator
    a = (sum_y - b * sum_x) / n

    r_denominator = np.sqrt((n * sum_x_squared - sum_x**2) * (n * sum_y_squared - sum_y**2))
    r = (n * sum_xy - sum_x * sum_y) / r_denominator if r_denominator != 0 else 0

    equation = f'{var_name_y} = {a:.2f} + {b:.2f}{var_name_x}'
    return {'equation': equation, 'intercept': a, 'slope': b, 'r_value': r}

# ===== STREAMLIT UI =====

st.set_page_config(layout="centered")
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to right, #fceabb, #f8b500);
        color: #000000;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    h1 {
        text-align: center;
        color: #6A1B9A;
    }
    .floating-image {
        display: block;
        margin: auto;
        border-radius: 15px;
        max-width: 70%;
    }
</style>
""", unsafe_allow_html=True)

# Judul & Gambar
st.title("✨ Penentuan Konsentrasi dari Regresi Deret Standar ✨")
st.markdown("#### Aplikasi untuk membantu menghitung persamaan regresi linear dan menentukan nilai X berdasarkan Y (misalnya: konsentrasi).")

img_url = "https://i.imgur.com/ZCCw6Ry.jpg"
st.markdown(f'<img src="{img_url}" class="floating-image">', unsafe_allow_html=True)

# Tim
st.header("👩‍🔬 Kelompok 11 - E2 PMIP")
st.write("""
1. Kayla Nurrahma Siswoyo (2420606)  
2. Nahda Rensa Subari (2420632)  
3. Rizka Rahmawati Shavendira (2420656)  
4. Ummu Nabiilah (2420676)  
5. Dinda Aryantika (2320520)
""")

# Input data
st.header("📋 Input Data Deret Standar")
default_data = pd.DataFrame({'X': [0.0]*4, 'Y': [0.0]*4})
data_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

var_name_x = st.text_input('Nama variabel X (misal: konsentrasi):', 'x')
var_name_y = st.text_input('Nama variabel Y (misal: absorbansi):', 'y')

# Hitung regresi
if not data_df.empty and 'X' in data_df.columns and 'Y' in data_df.columns:
    try:
        X = data_df['X'].astype(float).to_numpy()
        Y = data_df['Y'].astype(float).to_numpy()

        if len(X) < 2:
            st.warning("⚠️ Masukkan minimal 2 titik data.")
        elif np.all(X == X[0]):
            st.warning("⚠️ Semua nilai X sama. Tidak bisa menghitung regresi.")
        else:
            reg = calculate_regression_equation(X, Y, var_name_x, var_name_y)

            st.header("📈 Hasil Regresi Linear")
            st.markdown(f"**Persamaan:** `{reg['equation']}`")
            st.write(f"Slope (b): `{reg['slope']:.4f}`")
            st.write(f"Intercept (a): `{reg['intercept']:.4f}`")
            st.write(f"Koefisien Korelasi (r): `{reg['r_value']:.4f}`")

            # Grafik
            fig, ax = plt.subplots()
            ax.scatter(X, Y, color='blue', label='Data')
            ax.plot(X, reg['intercept'] + reg['slope'] * X, color='red', label='Garis Regresi')
            ax.set_xlabel(var_name_x)
            ax.set_ylabel(var_name_y)
            ax.set_title('Grafik Regresi Linear')
            ax.legend()
            st.pyplot(fig)

            # Kalkulasi X dari input Y
            st.header("🔍 Hitung Nilai X dari Input Y")
            y_input = st.number_input(f"Masukkan nilai {var_name_y} untuk dihitung {var_name_x}-nya:", value=0.0)
            if reg['slope'] != 0:
                x_calc = (y_input - reg['intercept']) / reg['slope']
                st.success(f"Nilai {var_name_x} = `{x_calc:.4f}` untuk {var_name_y} = `{y_input}`")
            else:
                st.error("Slope (b) = 0. Tidak bisa menghitung nilai X.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("💡 Silakan masukkan data X dan Y terlebih dahulu.")
