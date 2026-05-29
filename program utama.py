import streamlit as st
import json

# Konfigurasi Halaman Web
st.set_page_config(page_title="ChemAssist Lab", layout="wide")

# Fungsi untuk memuat data JSON
def load_data():
    try:
        with open('database_kimia.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Database tidak ditemukan! Pastikan file database_kimia.json ada di folder yang sama.")
        return []

data_kimia = load_data()

# ==========================================
# SIDEBAR NAVIGASI
# ==========================================
st.sidebar.title("🧪 ChemAssist v1.0")
menu = st.sidebar.radio("Navigasi Fitur:", 
    ["Beranda & Mini MSDS", "Pengendalian Tumpahan", "Kalkulator Ar/BM", "Konversi Kimia"])

# ==========================================
# 1. BERANDA & MINI MSDS
# ==========================================
if menu == "Beranda & Mini MSDS":
    st.title("🏠 Sistem Informasi Bahan Kimia (Mini MSDS)")
    
    # Mengambil list nama senyawa dari JSON dengan kata kunci baru 'nama_senyawa'
    nama_senyawa = [item['nama_senyawa'] for item in data_kimia]
    pilihan = st.selectbox("Cari dan Pilih Bahan Kimia:", nama_senyawa)
    
    # Mencari seluruh data untuk senyawa yang dipilih
    selected_item = next((item for item in data_kimia if item['nama_senyawa'] == pilihan), None)
    
    if selected_item:
        st.subheader(f"Informasi Detail: {selected_item['nama_senyawa']}")
        col1, col2 = st.columns(2)
        
        # Menyesuaikan dengan kata kunci (keys) JSON yang baru
        with col1:
            st.info(f"**Rumus Molekul:** {selected_item['rumus_kimia']}")
            st.info(f"**Wujud:** {selected_item['wujud']}")
            st.info(f"**Sifat Bahaya:** {selected_item['sifat']}")
        with col2:
            st.success(f"**Warna:** {selected_item['warna']}")
            st.success(f"**Bau:** {selected_item['bau']}")
            st.warning(f"**Klasifikasi LGK:** {selected_item['lgk']} ({selected_item['keterangan_lgk']})")

# ==========================================
# 2. PENGENDALIAN TUMPAHAN & P3K
# ==========================================
elif menu == "Pengendalian Tumpahan":
    st.title("⚠️ Prosedur K3L: Penanganan Tumpahan & P3K")
    
    pilihan = st.selectbox("Pilih Bahan yang Mengalami Insiden:", [item['nama_senyawa'] for item in data_kimia])
    target = next((item for item in data_kimia if item['nama_senyawa'] == pilihan), None)
    
    if target:
        st.subheader(f"Tindakan Darurat untuk {target['nama_senyawa']}")
        st.markdown(f"**Status Bahaya:** `{target['sifat']}`")
        
        # Karena di JSON sudah ada teks spesifik, kita bisa langsung memanggilnya (tidak perlu if/else kategori lagi)
        st.warning(f"**🧹 Prosedur Pengendalian Tumpahan:**\n\n{target['pengendalian_tumpahan']}")
        st.error(f"**🚑 Pertolongan Pertama (P3K):**\n\n{target['pertolongan_pertama']}")

# ==========================================
# 3. KALKULATOR Ar/BM
# ==========================================
elif menu == "Kalkulator Ar/BM":
    st.title("🧮 Kalkulator Berat Molekul (BM)")
    dict_ar = {"H": 1.008, "C": 12.011, "O": 15.999, "N": 14.007, "Na": 22.990, "S": 32.06, "Cl": 35.45}
    st.write("Masukkan jumlah atom per unsur:")
    cols = st.columns(4)
    user_inputs = {}
    
    for i, (unsur, nilai) in enumerate(dict_ar.items()):
        with cols[i % 4]:
            user_inputs[unsur] = st.number_input(f"Jumlah {unsur}:", min_value=0, step=1, key=unsur)
            
    if st.button("Hitung BM"):
        total_bm = sum(jumlah * dict_ar[unsur] for unsur, jumlah in user_inputs.items() if jumlah > 0)
        st.success(f"**Total Berat Molekul (BM): {total_bm:.4f} g/mol**")

# ==========================================
# 4. KONVERSI KIMIA
# ==========================================
elif menu == "Konversi Kimia":
    st.title("🔄 Kalkulator Konversi Komprehensif")
    tab1, tab2 = st.tabs(["Mol & Molaritas", "%b/b ➡ %b/v"])

    with tab1:
        st.subheader("Mol & Molaritas")
        try:
            massa = st.number_input("Massa (gram):", min_value=0.0)
            bm = st.number_input("BM (g/mol):", min_value=0.1)
            st.write(f"Hasil: **{massa/bm:.4f} mol**")
        except Exception:
            pass

    with tab2:
        st.subheader("Konversi % b/b ke % b/v")
        bb = st.number_input("Konsentrasi (% b/b):")
        rho = st.number_input("Densitas (g/mL):", min_value=0.0)
        st.info(f"Hasil Konsentrasi: **{bb * rho:.2f} % b/v**")
