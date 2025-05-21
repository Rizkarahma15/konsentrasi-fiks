import os
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Siapkan requirements (sekadar membantu saat deploy)
# --------------------------------------------------
if not os.path.exists("requirements.txt"):
    with open("requirements.txt", "w") as f:
        f.write("streamlit\nnumpy\npandas\nmatplotlib\nPillow\n")

# --------------------------------------------------
# Fungsi regresi linear manual
# --------------------------------------------------
def calculate_regression_equation(X, Y, x_name="x", y_name="y"):
    n = len(X)
    if n < 2:
        raise ValueError("Jumlah data minimal dua titik.")
    if np.all(X == X[0]):
        raise ZeroDivisionError("Semua nilai X sama — tidak bisa regresi.")

    sum_x, sum_y = np.sum(X), np.sum(Y)
    sum_xy = np.sum(X * Y)
    sum_x2 = np.sum(X**2)
    sum_y2 = np.sum(Y**2)

    denom = n * sum_x2 - sum_x**2
    b = (n * sum_xy - sum_x * sum_y) / denom
    a = (sum_y - b * sum_x) / n

    r_denom = np.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
    r = 0 if r_denom == 0 else (n * sum_xy - sum_x * sum_y) / r_denom

    eq = f"{y_name} = {a:.4f} + {b:.4f}{x_name}"
    return {"equation": eq, "intercept": a, "slope": b, "r_value": r}

# --------------------------------------------------
# Aplikasi Streamlit
# --------------------------------------------------
def main():
    st.set_page_config(page_title="Regresi & Konsentrasi", layout="centered")
    st.title("✨ Penentuan Konsentrasi • Deret Standar ✨")

    # ---------- Dekorasi sederhana ----------
    st.markdown("""
        <style>
        .stApp {background:linear-gradient(135deg,#FFB6C1,#B0E0E6);}
        h1 {text-align:center;color:#8B4513;
            animation:floating 3s ease-in-out infinite;}
        @keyframes floating{0%{transform:translateY(0);}
                            50%{transform:translateY(-10px);}
                            100%{transform:translateY(0);}}
        .floating-image{width:60%;display:block;margin:auto;
                        animation:float 4s ease-in-out infinite;
                        border-radius:20px;box-shadow:0 10px 20px rgba(0,0,0,.2);}
        @keyframes float{0%{transform:translateY(0);}
                         50%{transform:translateY(-15px);}
                         100%{transform:translateY(0);}}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<img src="https://i.imgur.com/ZCCw6Ry.jpg" class="floating-image">',
        unsafe_allow_html=True
    )

    # ---------- Petunjuk ----------
    st.info("""
    **Cara pakai:**  
    1. Masukkan/ubah data **X** dan **Y** pada tabel.  
    2. (Opsional) Ganti nama variabel X & Y.  
    3. Klik **📌 Hitung Regresi** → muncul persamaan & grafik.  
    4. Masukkan nilai **Y** sampel, lalu klik **🔍 Hitung Konsentrasi** untuk dapatkan **X**.
    """)

    # ---------- Input variabel ----------
    col1, col2 = st.columns(2)
    x_name = col1.text_input("Nama variabel X", "x")
    y_name = col2.text_input("Nama variabel Y", "y")

    # ---------- Data editor ----------
    default_df = pd.DataFrame({"X": [0.0, 0.0, 0.0, 0.0],
                               "Y": [0.0, 0.0, 0.0, 0.0]})
    data_df = st.data_editor(
        default_df, num_rows="dynamic", use_container_width=True,
        key="data_editor"
    )

    # ---------- State untuk hasil regresi ----------
    if "reg_result" not in st.session_state:
        st.session_state.reg_result = None  # belum dihitung

    # ---------- Tombol: Hitung Regresi ----------
    if st.button("📌 Hitung Regresi"):
        try:
            X = data_df["X"].astype(float).to_numpy()
            Y = data_df["Y"].astype(float).to_numpy()
            reg = calculate_regression_equation(X, Y, x_name, y_name)
            st.session_state.reg_result = reg  # simpan
        except Exception as e:
            st.error(f"❌ {e}")

    # ---------- Jika sudah ada hasil regresi ----------
    if st.session_state.reg_result:
        reg = st.session_state.reg_result

        st.subheader("📉 Hasil Regresi")
        st.write(f"**Persamaan:** {reg['equation']}")
        st.write(f"Intercept (a): **{reg['intercept']:.4f}**")
        st.write(f"Slope (b): **{reg['slope']:.4f}**")
        st.write(f"Koefisien korelasi (r): **{reg['r_value']:.4f}**")

        # Grafik
        X_plot = data_df["X"].astype(float).to_numpy()
        Y_plot = data_df["Y"].astype(float).to_numpy()
        fig, ax = plt.subplots()
        ax.scatter(X_plot, Y_plot, label="Data")
        ax.plot(X_plot,
                reg["intercept"] + reg["slope"] * X_plot,
                label="Regresi")
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
        ax.set_title("Grafik Regresi Linear")
        ax.legend()
        st.pyplot(fig, use_container_width=True)

        # ---------- Hitung Konsentrasi ----------
        st.header("🧪 Hitung Konsentrasi (X)")
        y_val = st.number_input(f"Masukkan nilai {y_name} (Y)", value=0.0, format="%.4f")
        if st.button("🔍 Hitung Konsentrasi"):
            b, a = reg["slope"], reg["intercept"]
            if b == 0:
                st.error("Slope (b) = 0, tidak bisa menghitung X.")
            else:
                x_calc = (y_val - a) / b
                st.success(f"👉 {x_name} = **{x_calc:.4f}**")

# --------------------------------------------------
if __name__ == "__main__":
    main()
