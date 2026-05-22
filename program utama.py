import streamlit as st
import json

st.set_page_config(page_title="ChemAssist Lab", layout="wide")

def load_data():
    try:
        with open('database_kimia.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Database tidak ditemukan!")
        return []

data_kimia = load_data()

st.sidebar.title("🧪 ChemAssist v1.0")
menu = st.sidebar.radio("Navigasi Fitur:", 
    ["Beranda & Mini MSDS", "Pengendalian Tumpahan", "Kalkulator Ar/BM", "Konversi Kimia"])

if menu == "Beranda & Mini MSDS":
    st.title("🏠 Sistem Informasi Bahan Kimia (Mini MSDS)")
    nama_senyawa = [item['nama'] for item in data_kimia]
    pilihan = st.selectbox("Cari dan Pilih Bahan Kimia:", nama_senyawa)
    selected_item = next((item for item in data_kimia if item['nama'] == pilihan), None)
    
    if selected_item:
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Nama Kimia:** {selected_item['nama']}")
            st.info(f"**Rumus Molekul:** {selected_item['rumus']}")
            st.info(f"**Wujud:** {selected_item['wujud']}")
        with col2:
            st.warning(f"**Sifat Bahaya:** {selected_item['bahaya']}")
            st.success(f"**Warna:** {selected_item['warna']}")
            st.success(f"**Bau:** {selected_item['bau']}")

elif menu == "Pengendalian Tumpahan":
    st.title("⚠️ Prosedur K3L: Penanganan Tumpahan")
    pilihan = st.selectbox("Pilih Bahan yang Tumpah:", [item['nama'] for item in data_kimia])
    target = next((item for item in data_kimia if item['nama'] == pilihan), None)
    
    if target:
        st.subheader(f"Prosedur untuk: {target['nama']} ({target['bahaya']})")
        kat = target['kategori']
        if "asam_kuat" in kat:
            st.error("1. Segera gunakan APD Lengkap.")
            st.success("2. Netralkan perlahan dengan NaHCO3 hingga buih hilang.")
        elif "basa_kuat" in kat:
            st.error("1. Hindari kontak kulit langsung.")
            st.success("2. Netralkan dengan asam lemah encer.")
        elif "flamabel" in kat:
            st.error("1. MATIKAN SEMUA SUMBER API.")
            st.warning("2. Gunakan pasir atau absorben universal.")
        else:
            st.info("1. Bersihkan tumpahan dengan prosedur standar.")

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
