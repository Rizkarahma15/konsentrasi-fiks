def main():
    st.title('✨ Penentuan Konsentrasi dari Persamaan Regresi Deret Standar ✨')
    st.write('Penentuan konsentrasi dari persamaan regresi deret standar yang dapat memudahkan analisis tanpa perlu menghitung secara manual. ENJOY FOR ACCESS 🧪👩‍🔬')

    # Gaya
    st.markdown("""<style>
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
    </style>""", unsafe_allow_html=True)

    # Gambar
    st.markdown(f'<img src="https://i.imgur.com/ZCCw6Ry.jpg" class="floating-image">', unsafe_allow_html=True)

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

    st.header("📈 Kalkulator Regresi Linear")
    default_data = pd.DataFrame({'X': [0.0]*4, 'Y': [0.0]*4})
    data_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

    var_name_x = st.text_input('Nama variabel X:', 'x')
    var_name_y = st.text_input('Nama variabel Y:', 'y')

    reg = None
    fig = None

    if not data_df.empty and 'X' in data_df.columns and 'Y' in data_df.columns:
        try:
            X = data_df['X'].astype(float).to_numpy()
            Y = data_df['Y'].astype(float).to_numpy()

            if len(X) >= 2 and not np.all(X == X[0]):
                reg = calculate_regression_equation(X, Y, var_name_x, var_name_y)
                fig, ax = plt.subplots()
                ax.scatter(X, Y, color='blue', label='Data')
                ax.plot(X, reg['intercept'] + reg['slope'] * X, color='red', label='Regresi')
                ax.set_xlabel(var_name_x)
                ax.set_ylabel(var_name_y)
                ax.set_title('Grafik Regresi Linear')
                ax.legend()
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {e}")

    # Tampilkan hasil meskipun belum valid
    st.markdown("## Hasil Regresi:")
    if reg:
        st.markdown(f"### 📌 {reg['equation']}")
        st.write(f"Slope (b): {reg['slope']:.2f}")
        st.write(f"Intercept (a): {reg['intercept']:.2f}")
        st.write(f"Koefisien Korelasi (r): {reg['r_value']:.4f}")
    else:
        st.info("📌 Masukkan data yang valid untuk melihat persamaan regresi.")

    st.markdown("## Grafik Regresi:")
    if fig:
        st.pyplot(fig)
    else:
        st.info("📊 Grafik akan ditampilkan setelah data valid diisi.")

    st.header("📊 Hitung Nilai X Berdasarkan Y")
    y_input = st.number_input(f'Masukkan nilai {var_name_y}:', value=0.0)

    if reg:
        b = reg['slope']
        a = reg['intercept']
        if b != 0:
            x_calc = (y_input - a) / b
            st.success(f"Nilai {var_name_x} untuk {var_name_y} = {y_input} adalah: {x_calc:.2f}")
        else:
            st.error("Slope (b) = 0, tidak bisa menghitung X.")
    else:
        st.info("Masukkan data valid terlebih dahulu untuk menghitung nilai X.")
