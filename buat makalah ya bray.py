import os
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Buat requirements.txt otomatis
if not os.path.exists('requirements.txt'):
    with open('requirements.txt', 'w') as f:
        f.write("streamlit\nnumpy\npandas\nmatplotlib\nPillow\n")

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
    if r_denominator == 0:
        r = 0
    else:
        r = (n * sum_xy - sum_x * sum_y) / r_denominator

    equation = f'{var_name_y} = {a:.2f} + {b:.2f}{var_name_x}'
    return {'equation': equation, 'intercept': a, 'slope': b, 'r_value': r}

def main():
    st.title('✨ Penentuan Konsentrasi dari Persamaan Regresi Deret Standar ✨')

    # CSS
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #FFB6C1, #B0E0E6);
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
        h1 {
            text-align: center;
            color: #8B4513;
            animation: floating 3s ease-in-out infinite;
        }
        @keyframes floating {
            0% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0); }
        }
        .floating-image {
            width: 60%;
            display: block;
            margin: auto;
            animation: float 4s ease-in-out infinite;
            border-radius: 20px;
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
        }
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
            100% { transform: translateY(0px); }
        }
        </style>
    """, unsafe_allow_html=True)

    # Gambar
    img_url = "https://i.imgur.com/ZCCw6Ry.jpg"
    st.markdown(f'<img src="{img_url}" class="floating-image">', unsafe_allow_html=True)

    # Tim
    st.header("INTRODUCTION OUR TEAM")
    st.subheader("👥 Kelompok 11 (E2-PMIP)")
    st.write("""
    1. Kayla Nurrahma Siswoyo (2420606)  
    2. Nahda Rensa Subari (2420632)  
    3. Rizka Rahmawati Shavendira (2420656)  
    4. Ummu Nabiilah (2420676)  
    5. Dinda Aryantika (2320520)
    """)

    # Input variabel
    st.header("📈 Kalkulator Regresi Linear")
    default_data = pd.DataFrame({'X': [0.0, 0.0, 0.0, 0.0], 'Y': [0.0, 0.0, 0.0, 0.0]})
    data_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)
    var_name_x = st.text_input('Nama variabel X:', 'x')
    var_name_y = st.text_input('Nama variabel Y:', 'y')

    # Tempat simpan regresi
    if 'regresi' not in st.session_state:
        st.session_state.regresi = None

    # Tombol hitung regresi
    if st.button("📌 Hitung Regresi"):
        try:
            X = data_df['X'].astype(float).to_numpy()
            Y = data_df['Y'].astype(float).to_numpy()

            if len(X) < 2:
                st.warning("⚠️ Minimal diperlukan 2 titik data.")
            elif np.all(X == X[0]):
                st.warning("📝 Nilai X harus bervariasi.")
            else:
                reg = calculate_regression_equation(X, Y, var_name_x, var_name_y)
                st.session_state.regresi = reg

                st.subheader("📉 Hasil Regresi:")
                st.markdown(f"**Persamaan:** {reg['equation']}")
                st.write(f"Intercept (a): {reg['intercept']:.2f}")
                st.write(f"Slope (b): {reg['slope']:.2f}")
                st.write(f"Koefisien korelasi (r): {reg['r_value']:.4f}")

                # Grafik
                fig, ax = plt.subplots()
                ax.scatter(X, Y, color='blue', label='Data')
                ax.plot(X, reg['intercept'] + reg['slope'] * X, color='red', label='Regresi')
                ax.set_xlabel(var_name_x)
                ax.set_ylabel(var_name_y)
                ax.set_title('Grafik Regresi Linear')
                ax.legend()
                st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ Error: {e}")

    # Input & tombol hitung konsentrasi
    st.header("🧪 Hitung Konsentrasi dari Nilai Y")
    y_input = st.number_input(f'Masukkan nilai {var_name_y} (Y):', value=0.0, format="%.4f")

    if st.button("🔍 Hitung Konsentrasi (X)"):
        reg = st.session_state.get('regresi', None)
        if reg:
            b = reg['slope']
            a = reg['intercept']
            if b != 0:
                x_calc = (y_input - a) / b
                st.success(f"Hasil: {var_name_x} = {x_calc:.4f}")
            else:
                st.error("Slope = 0, tidak bisa menghitung X.")
        else:
            st.warning("⚠️ Silakan hitung regresi terlebih dahulu.")

# Jalankan aplikasi
if __name__ == '__main__':
    main()
