import os
import pickle
import textwrap

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sistem Kualitas Udara Jakarta",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

try:
    import plotly.express as px
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False


class ModelSementara:
    def predict(self, x):
        return ["MEDIUM"]


@st.cache_resource
def muat_model():
    if os.path.exists("model/model.pkl"):
        with open("model/model.pkl", "rb") as file:
            return pickle.load(file)
    return ModelSementara()


model = muat_model()

KOLOM_MODEL = ["PM10", "PM25", "SO2", "CO", "O3", "NO2"]

INFO_POLUSI = [
    {
        "label": "Debu Kasar (PM10)",
        "kolom": "PM10",
        "default": 45.0,
        "penjelasan": "Debu dari jalan, bangunan, dan asap yang ukurannya masih lebih besar.",
    },
    {
        "label": "Debu Halus (PM2.5)",
        "kolom": "PM25",
        "default": 65.0,
        "penjelasan": "Debu sangat kecil yang lebih mudah masuk ke saluran pernapasan.",
    },
    {
        "label": "Gas Belerang (SO2)",
        "kolom": "SO2",
        "default": 15.0,
        "penjelasan": "Gas dari pembakaran bahan bakar tertentu.",
    },
    {
        "label": "Gas Karbon (CO)",
        "kolom": "CO",
        "default": 12.0,
        "penjelasan": "Gas dari asap kendaraan dan pembakaran tidak sempurna.",
    },
    {
        "label": "Ozon Permukaan (O3)",
        "kolom": "O3",
        "default": 30.0,
        "penjelasan": "Polutan yang terbentuk saat polusi bereaksi dengan panas matahari.",
    },
    {
        "label": "Gas Nitrogen (NO2)",
        "kolom": "NO2",
        "default": 22.0,
        "penjelasan": "Gas yang sering muncul dari asap kendaraan dan kegiatan perkotaan.",
    },
]

CONTOH_NILAI = {
    "Contoh Udara Baik": [32.0, 38.0, 18.0, 7.0, 18.0, 12.0],
    "Contoh Udara Sedang": [65.0, 78.0, 28.0, 13.0, 36.0, 22.0],
    "Contoh Udara Kurang Sehat": [120.0, 145.0, 40.0, 22.0, 58.0, 36.0],
    "Isi Sendiri": [45.0, 65.0, 15.0, 12.0, 30.0, 22.0],
}

TAHAP_KERJA = [
    {
        "nomor": "01",
        "judul": "Memahami Masalah",
        "isi": "Masalah utama adalah data udara sering tampil sebagai angka, tetapi sulit dipahami oleh masyarakat.",
        "hasil": "Tujuan sistem ditentukan, yaitu mengubah angka polutan menjadi informasi kualitas udara.",
    },
    {
        "nomor": "02",
        "judul": "Memahami Data",
        "isi": "Data berisi tanggal, lokasi pengukuran, nilai polutan, dan kategori kualitas udara.",
        "hasil": "Kolom penting dikenali, seperti PM10, PM2.5, SO2, CO, O3, NO2, dan kategori udara.",
    },
    {
        "nomor": "03",
        "judul": "Menyiapkan Data",
        "isi": "Data dibersihkan, nilai kosong diperiksa, dan angka polutan disiapkan agar bisa diproses.",
        "hasil": "Data siap digunakan untuk membuat model penentu kategori udara.",
    },
    {
        "nomor": "04",
        "judul": "Membuat Model",
        "isi": "Sistem belajar dari data yang sudah memiliki kategori udara.",
        "hasil": "Model dapat menerima enam angka polutan dan menghasilkan kategori udara.",
    },
    {
        "nomor": "05",
        "judul": "Menilai Hasil",
        "isi": "Hasil model diperiksa untuk melihat apakah kategori yang diberikan sudah sesuai.",
        "hasil": "Model dinilai dari ketepatan hasil dan perbandingan data latih serta data uji.",
    },
    {
        "nomor": "06",
        "judul": "Menerapkan Sistem",
        "isi": "Model dimasukkan ke aplikasi agar bisa digunakan melalui halaman web.",
        "hasil": "Pengguna dapat mengisi angka polutan dan membaca hasilnya secara langsung.",
    },
]


def terapkan_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800&display=swap');

    :root {
        --utama: #43766C;
        --utama-gelap: #345E56;
        --utama-muda: #EAF2EF;
        --latar: #F8FAE5;
        --kartu: #FFFDF7;
        --putih: #FFFFFF;
        --aksen: #B19470;
        --cokelat: #76453B;
        --teks: #2E2A27;
        --teks-lembut: #615954;
        --garis: rgba(118, 69, 59, 0.14);
        --garis-kuat: rgba(118, 69, 59, 0.24);
        --baik: #43766C;
        --sedang: #B19470;
        --buruk: #B55D42;
        --bayangan: 0 18px 44px rgba(67, 118, 108, 0.10), 0 4px 14px rgba(118, 69, 59, 0.07);
        --bayangan-tipis: 0 10px 26px rgba(67, 118, 108, 0.08);
        --radius-besar: 32px;
        --radius-sedang: 22px;
        --radius-kecil: 16px;
        --gerak: all 0.25s ease;
    }

    html, body, .stApp {
        background:
            radial-gradient(circle at 8% 5%, rgba(177, 148, 112, 0.16), transparent 28%),
            radial-gradient(circle at 92% 8%, rgba(67, 118, 108, 0.14), transparent 30%),
            linear-gradient(180deg, #FBFCF2 0%, #F8FAE5 100%);
        color: var(--teks);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        overflow-x: hidden;
    }

    .block-container {
        max-width: 1400px;
        padding: 26px 36px 56px 36px;
    }

    header, footer, [data-testid="collapsedControl"] {
        display: none !important;
    }

    h1, h2, h3, h4, .huruf-judul {
        font-family: 'Playfair Display', serif !important;
        letter-spacing: -0.035em;
    }

    p, li, label, span, div {
        word-wrap: break-word;
    }

    .kepala-atas {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 18px;
        margin-bottom: 18px;
    }

    .merek {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .ikon-merek {
        width: 46px;
        height: 46px;
        border-radius: 17px;
        display: grid;
        place-items: center;
        background: linear-gradient(135deg, var(--utama) 0%, var(--utama-gelap) 100%);
        color: var(--latar);
        font-size: 1.35rem;
        box-shadow: var(--bayangan-tipis);
    }

    .judul-merek {
        color: var(--cokelat);
        font-weight: 900;
        font-size: 1.07rem;
        line-height: 1.2;
    }

    .teks-merek {
        color: var(--teks-lembut);
        font-size: 0.86rem;
        line-height: 1.4;
        margin-top: 2px;
    }

    .label-status {
        padding: 10px 14px;
        border-radius: 999px;
        background: rgba(255, 253, 247, 0.82);
        border: 1px solid var(--garis);
        color: var(--utama-gelap);
        font-size: 0.88rem;
        font-weight: 800;
        box-shadow: var(--bayangan-tipis);
        white-space: nowrap;
    }

    .pahlawan {
        position: relative;
        overflow: hidden;
        border-radius: var(--radius-besar);
        background:
            radial-gradient(circle at 88% 12%, rgba(248, 250, 229, 0.18), transparent 28%),
            linear-gradient(135deg, #43766C 0%, #345E56 48%, #294B45 100%);
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: var(--bayangan);
        padding: 40px;
        margin-bottom: 22px;
    }

    .pahlawan-kisi {
        display: grid;
        grid-template-columns: minmax(0, 1.35fr) minmax(300px, 0.82fr);
        gap: 24px;
        align-items: stretch;
    }

    .lencana-atas {
        display: inline-flex;
        align-items: center;
        gap: 9px;
        padding: 9px 14px;
        border-radius: 999px;
        background: rgba(248, 250, 229, 0.13);
        border: 1px solid rgba(248, 250, 229, 0.22);
        color: #F8FAE5;
        font-size: 0.82rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 18px;
    }

    .judul-pahlawan {
        color: #F8FAE5 !important;
        font-size: clamp(2.1rem, 5vw, 4rem);
        line-height: 1.02;
        margin: 0 0 16px 0;
        max-width: 840px;
    }

    .teks-pahlawan {
        color: rgba(248, 250, 229, 0.90);
        font-size: 1.04rem;
        line-height: 1.78;
        margin: 0;
        max-width: 800px;
    }

    .sisi-pahlawan {
        display: grid;
        gap: 14px;
    }

    .kartu-pahlawan {
        background: rgba(255, 255, 255, 0.11);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 22px;
        padding: 18px;
        backdrop-filter: blur(8px);
    }

    .judul-kartu-pahlawan {
        color: #F8FAE5;
        font-size: 0.94rem;
        font-weight: 900;
        margin-bottom: 7px;
    }

    .teks-kartu-pahlawan {
        color: rgba(248, 250, 229, 0.86);
        font-size: 0.94rem;
        line-height: 1.68;
        margin: 0;
    }

    .wadah-menu {
        margin-bottom: 22px;
    }

    div[data-testid="stRadio"] > div {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        background: rgba(255, 253, 247, 0.82);
        border: 1px solid var(--garis);
        border-radius: 24px;
        padding: 12px;
        box-shadow: var(--bayangan-tipis);
    }

    div[data-testid="stRadio"] label {
        min-height: 66px;
        border-radius: 18px !important;
        background: #FFFEFB !important;
        border: 1px solid transparent !important;
        padding: 14px 18px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: var(--gerak);
    }

    div[data-testid="stRadio"] label:hover {
        border-color: rgba(67, 118, 108, 0.22) !important;
        transform: translateY(-1px);
    }

    div[data-testid="stRadio"] label[data-checked="true"],
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, var(--utama) 0%, var(--utama-gelap) 100%) !important;
        box-shadow: 0 12px 22px rgba(67, 118, 108, 0.18);
    }

    div[data-testid="stRadio"] p {
        margin: 0 !important;
        color: var(--teks) !important;
        font-size: 0.95rem !important;
        font-weight: 900 !important;
        text-align: center;
    }

    div[data-testid="stRadio"] label[data-checked="true"] p,
    div[data-testid="stRadio"] label:has(input:checked) p {
        color: #FFFFFF !important;
    }

    .panel {
        background: rgba(255, 253, 247, 0.90);
        border: 1px solid var(--garis);
        border-radius: var(--radius-besar);
        box-shadow: var(--bayangan);
        margin-bottom: 22px;
        overflow: hidden;
    }

    .isi-panel {
        padding: 28px;
    }

    .kepala-panel {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 18px;
        padding: 28px 28px 0 28px;
    }

    .bungkus-judul-panel {
        max-width: 900px;
    }

    .teks-atas {
        color: var(--utama);
        font-size: 0.8rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        margin-bottom: 9px;
    }

    .judul-panel {
        color: var(--cokelat) !important;
        font-size: clamp(1.48rem, 2.5vw, 2.25rem);
        line-height: 1.14;
        margin: 0 0 10px 0;
    }

    .teks-panel {
        color: var(--teks-lembut);
        font-size: 1rem;
        line-height: 1.76;
        margin: 0;
    }

    .catatan-kecil {
        min-width: 260px;
        max-width: 350px;
        padding: 16px 18px;
        border-radius: 20px;
        background: var(--utama-muda);
        border: 1px solid rgba(67, 118, 108, 0.16);
        color: var(--utama-gelap);
        font-size: 0.93rem;
        line-height: 1.65;
        font-weight: 700;
    }

    .kisi-ringkasan {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
        padding: 28px;
    }

    .kartu-ringkasan {
        background: linear-gradient(180deg, #FFFFFF 0%, #FBF9F4 100%);
        border: 1px solid var(--garis);
        border-radius: 22px;
        padding: 20px;
        min-height: 150px;
    }

    .angka-kecil {
        width: 40px;
        height: 40px;
        border-radius: 15px;
        display: grid;
        place-items: center;
        background: var(--utama-muda);
        color: var(--utama-gelap);
        font-size: 0.88rem;
        font-weight: 900;
        margin-bottom: 12px;
    }

    .label-kartu {
        color: var(--teks-lembut);
        font-size: 0.86rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .nilai-kartu {
        color: var(--cokelat);
        font-size: 1.28rem;
        font-weight: 900;
        line-height: 1.25;
        margin-bottom: 7px;
    }

    .teks-kartu {
        color: var(--teks-lembut);
        font-size: 0.91rem;
        line-height: 1.62;
        margin: 0;
    }

    .kisi-tahap {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
        padding: 28px;
    }

    .kartu-tahap {
        position: relative;
        background: #FFFEFB;
        border: 1px solid var(--garis);
        border-radius: 24px;
        padding: 22px;
        min-height: 260px;
        overflow: hidden;
    }

    .kartu-tahap::before {
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 6px;
        background: linear-gradient(180deg, var(--utama), var(--aksen));
    }

    .nomor-tahap {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 16px;
        background: var(--utama-muda);
        color: var(--utama-gelap);
        font-weight: 900;
        margin-bottom: 14px;
    }

    .judul-tahap {
        color: var(--cokelat);
        font-size: 1.05rem;
        font-weight: 900;
        margin-bottom: 10px;
    }

    .isi-tahap {
        color: var(--teks-lembut);
        font-size: 0.94rem;
        line-height: 1.7;
        margin-bottom: 14px;
    }

    .hasil-tahap {
        background: rgba(67, 118, 108, 0.08);
        border: 1px solid rgba(67, 118, 108, 0.12);
        border-radius: 16px;
        padding: 12px;
        color: var(--utama-gelap);
        font-size: 0.9rem;
        line-height: 1.6;
        font-weight: 700;
    }

    .kisi-info {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
        padding: 28px;
    }

    .kartu-info {
        background: #FFFEFB;
        border: 1px solid var(--garis);
        border-radius: 22px;
        padding: 20px;
        min-height: 185px;
    }

    .nomor-info {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: inline-grid;
        place-items: center;
        background: var(--utama-muda);
        color: var(--utama-gelap);
        font-weight: 900;
        margin-bottom: 13px;
    }

    .judul-info {
        color: var(--cokelat);
        font-size: 1rem;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .teks-info {
        color: var(--teks-lembut);
        line-height: 1.72;
        font-size: 0.94rem;
        margin: 0;
    }

    .bagian-form {
        padding: 28px;
    }

    div[data-testid="stForm"] {
        border: 0 !important;
        background: transparent !important;
        padding: 0 !important;
        box-shadow: none !important;
    }

    .kotak-catatan {
        background: #FFFEFB;
        border: 1px solid var(--garis);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 18px;
    }

    .judul-catatan {
        color: var(--cokelat);
        font-weight: 900;
        font-size: 0.98rem;
        margin-bottom: 8px;
    }

    .teks-catatan {
        color: var(--teks-lembut);
        font-size: 0.9rem;
        line-height: 1.65;
        margin: 0;
    }

    .bungkus-kolom {
        background: #FFFEFB;
        border: 1px solid var(--garis);
        border-radius: 20px;
        padding: 15px 15px 8px 15px;
        height: 100%;
        transition: var(--gerak);
    }

    .bungkus-kolom:hover {
        border-color: rgba(67, 118, 108, 0.26);
        box-shadow: 0 10px 20px rgba(67, 118, 108, 0.06);
    }

    .keterangan-kolom {
        color: var(--teks-lembut);
        font-size: 0.86rem;
        line-height: 1.55;
        margin-top: 7px;
        min-height: 42px;
    }

    .stSelectbox label p,
    .stNumberInput label p {
        color: var(--cokelat) !important;
        font-weight: 900 !important;
        font-size: 0.94rem !important;
    }

    [data-baseweb="select"] > div,
    [data-baseweb="input"] {
        background: #FFFFFF !important;
        border: 1px solid var(--garis-kuat) !important;
        border-radius: 15px !important;
        min-height: 48px;
    }

    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="input"]:focus-within {
        border-color: var(--utama) !important;
        box-shadow: 0 0 0 3px rgba(67, 118, 108, 0.12) !important;
    }

    [data-baseweb="input"] input {
        color: var(--teks) !important;
        font-weight: 800 !important;
    }

    div[data-testid="stFormSubmitButton"] {
        margin-top: 12px;
    }

    div[data-testid="stFormSubmitButton"] > button,
    button[kind="primary"] {
        width: 100% !important;
        min-height: 58px !important;
        border-radius: 18px !important;
        border: none !important;
        background: linear-gradient(135deg, var(--utama) 0%, var(--utama-gelap) 100%) !important;
        color: white !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
        box-shadow: 0 16px 24px rgba(67, 118, 108, 0.22) !important;
        transition: var(--gerak) !important;
    }

    div[data-testid="stFormSubmitButton"] > button:hover,
    button[kind="primary"]:hover {
        transform: translateY(-1px);
        filter: brightness(0.98);
    }

    .kisi-hasil {
        display: grid;
        grid-template-columns: minmax(300px, 0.92fr) minmax(0, 1.32fr);
        gap: 18px;
        padding: 0 28px 28px 28px;
    }

    .kartu-hasil {
        background: #FFFEFB;
        border: 1px solid var(--garis);
        border-radius: 24px;
        padding: 22px;
        height: 100%;
    }

    .status-baik {
        border-left: 8px solid var(--baik);
        background: linear-gradient(180deg, rgba(67, 118, 108, 0.075) 0%, #FFFEFB 82%);
    }

    .status-sedang {
        border-left: 8px solid var(--sedang);
        background: linear-gradient(180deg, rgba(177, 148, 112, 0.10) 0%, #FFFEFB 82%);
    }

    .status-buruk {
        border-left: 8px solid var(--buruk);
        background: linear-gradient(180deg, rgba(181, 93, 66, 0.10) 0%, #FFFEFB 82%);
    }

    .lencana-hasil {
        display: inline-flex;
        align-items: center;
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(67, 118, 108, 0.10);
        color: var(--utama-gelap);
        font-size: 0.82rem;
        font-weight: 900;
        margin-bottom: 14px;
    }

    .judul-hasil {
        color: var(--cokelat) !important;
        font-size: 1.72rem;
        line-height: 1.18;
        margin: 0 0 12px 0;
    }

    .teks-hasil {
        color: var(--teks);
        line-height: 1.78;
        margin-bottom: 18px;
    }

    .daftar-saran {
        display: grid;
        gap: 10px;
        margin-top: 12px;
    }

    .isi-saran {
        display: flex;
        gap: 10px;
        align-items: flex-start;
        padding: 12px 14px;
        border-radius: 15px;
        background: rgba(248, 250, 229, 0.75);
        border: 1px solid rgba(67, 118, 108, 0.10);
        color: var(--teks);
        line-height: 1.6;
    }

    .kisi-sorotan {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
        margin-top: 16px;
    }

    .kotak-sorotan {
        background: #FFFFFF;
        border: 1px solid var(--garis);
        border-radius: 18px;
        padding: 16px;
    }

    .label-sorotan {
        color: var(--teks-lembut);
        font-size: 0.84rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .nilai-sorotan {
        color: var(--cokelat);
        font-size: 1.18rem;
        line-height: 1.35;
        font-weight: 900;
    }

    .kisi-anjuran {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
        margin-top: 16px;
    }

    .kartu-anjuran {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid var(--garis);
        border-radius: 18px;
        padding: 16px;
    }

    .judul-anjuran {
        color: var(--cokelat);
        font-weight: 900;
        margin-bottom: 8px;
    }

    .teks-anjuran {
        color: var(--teks-lembut);
        font-size: 0.92rem;
        line-height: 1.68;
        margin: 0;
    }

    .catatan-bawah {
        color: var(--teks-lembut);
        font-size: 0.92rem;
        line-height: 1.72;
        padding: 18px 28px 28px 28px;
    }

    [data-testid="stPlotlyChart"],
    [data-testid="stVegaLiteChart"],
    [data-testid="stBarChart"],
    [data-testid="stDataFrame"] {
        background: transparent !important;
    }

    @media (max-width: 1440px) {
        .block-container {
            max-width: 1280px;
        }
    }

    @media (max-width: 1280px) {
        .block-container {
            max-width: 1160px;
            padding-left: 28px;
            padding-right: 28px;
        }

        .kisi-ringkasan {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .kisi-tahap {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 1080px) {
        .pahlawan-kisi,
        .kisi-hasil,
        .kisi-info {
            grid-template-columns: 1fr;
        }

        .kepala-panel {
            flex-direction: column;
        }

        .catatan-kecil {
            max-width: none;
            width: 100%;
        }

        div[data-testid="stRadio"] > div {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 920px) {
        div[data-testid="stRadio"] > div,
        .kisi-sorotan,
        .kisi-anjuran,
        .kisi-ringkasan,
        .kisi-tahap {
            grid-template-columns: 1fr;
        }

        div[data-testid="stRadio"] label {
            min-height: 56px;
        }

        .kepala-atas {
            align-items: flex-start;
            flex-direction: column;
        }

        .label-status {
            white-space: normal;
        }
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 18px 16px 36px 16px;
        }

        .pahlawan {
            padding: 24px 18px;
            border-radius: 24px;
        }

        .judul-pahlawan {
            font-size: 2rem;
        }

        .teks-pahlawan,
        .teks-panel,
        .teks-info,
        .keterangan-kolom,
        .teks-hasil,
        .teks-anjuran,
        .teks-catatan {
            font-size: 0.94rem;
        }

        .panel,
        .kartu-hasil,
        .kartu-ringkasan,
        .kartu-info,
        .kotak-sorotan,
        .bungkus-kolom,
        .kotak-catatan,
        .kartu-anjuran,
        .kartu-tahap {
            border-radius: 20px;
        }

        .kepala-panel,
        .isi-panel,
        .bagian-form,
        .kisi-ringkasan,
        .kisi-hasil,
        .kisi-info,
        .kisi-tahap,
        .catatan-bawah {
            padding-left: 16px;
            padding-right: 16px;
        }
    }

    @media (max-width: 560px) {
        .ikon-merek {
            width: 40px;
            height: 40px;
            border-radius: 14px;
        }

        .lencana-atas {
            font-size: 0.72rem;
            line-height: 1.4;
            align-items: flex-start;
        }

        .judul-pahlawan {
            font-size: 1.66rem;
        }

        .judul-panel {
            font-size: 1.34rem;
        }

        .judul-hasil {
            font-size: 1.30rem;
        }

        .nilai-kartu,
        .nilai-sorotan {
            font-size: 1.08rem;
        }

        .kepala-panel {
            padding-top: 20px;
        }

        .kisi-ringkasan,
        .bagian-form,
        .kisi-hasil,
        .kisi-info,
        .kisi-tahap {
            gap: 12px;
        }
    }

    @media (max-width: 420px) {
        .block-container {
            padding-left: 12px;
            padding-right: 12px;
        }

        .pahlawan {
            padding: 20px 14px;
        }

        .judul-pahlawan {
            font-size: 1.48rem;
        }

        .kartu-pahlawan,
        .kartu-ringkasan,
        .kartu-info,
        .kartu-hasil,
        .kotak-catatan,
        .bungkus-kolom,
        .kartu-anjuran,
        .kartu-tahap {
            padding: 14px;
        }

        .isi-saran {
            padding: 10px 12px;
        }
    }
    </style>
    """
    st.markdown(textwrap.dedent(css), unsafe_allow_html=True)


def ambil_contoh_nilai(nama):
    return CONTOH_NILAI.get(nama, CONTOH_NILAI["Isi Sendiri"])


def buat_dataframe_input(nilai_input):
    return pd.DataFrame([nilai_input], columns=KOLOM_MODEL)


def buat_dataframe_grafik(nilai_input):
    return pd.DataFrame(
        {
            "Jenis Polutan": ["PM10", "PM2.5", "SO2", "CO", "O3", "NO2"],
            "Nilai": nilai_input,
        }
    ).sort_values("Nilai", ascending=True)


def cari_zat_tertinggi(nilai_input):
    pasangan = {item["label"]: nilai for item, nilai in zip(INFO_POLUSI, nilai_input)}
    nama = max(pasangan, key=pasangan.get)
    return nama, pasangan[nama]


def normalisasi_kategori(kategori):
    if kategori == "VERY_UNHEALTHY":
        return "UNHEALTHY"
    return kategori


def ubah_nama_kategori(kategori):
    kategori = normalisasi_kategori(kategori)
    if kategori == "GOOD":
        return "Baik"
    if kategori == "MEDIUM":
        return "Sedang"
    if kategori == "UNHEALTHY":
        return "Kurang Sehat"
    return "Sedang"


def ambil_ringkasan_status(kategori):
    kategori = normalisasi_kategori(kategori)

    data = {
        "GOOD": {
            "judul": "Udara Bersih dan Nyaman",
            "kelas": "baik",
            "badge": "Aman",
            "saran": (
                "Kondisi udara tergolong baik. Kegiatan harian masih dapat dilakukan dengan nyaman. "
                "Pengguna tetap disarankan menjaga kebersihan lingkungan dan memantau kondisi jika berada lama di luar ruangan."
            ),
            "aksi": [
                "Kegiatan luar ruangan dapat dilakukan seperti biasa.",
                "Ventilasi rumah dapat dibuka agar udara segar masuk.",
                "Tetap perhatikan kondisi tubuh jika sensitif terhadap debu.",
            ],
        },
        "MEDIUM": {
            "judul": "Udara Sedang, Perlu Waspada",
            "kelas": "sedang",
            "badge": "Waspada",
            "saran": (
                "Udara masih dapat diterima, tetapi kelompok sensitif sebaiknya mulai berhati-hati. "
                "Kegiatan luar ruangan masih bisa dilakukan, namun jangan terlalu lama."
            ),
            "aksi": [
                "Kurangi olahraga berat di luar ruangan.",
                "Gunakan masker saat berada di jalan ramai.",
                "Kelompok sensitif lebih aman berada di dalam ruangan.",
            ],
        },
        "UNHEALTHY": {
            "judul": "Udara Kurang Sehat",
            "kelas": "buruk",
            "badge": "Perlu Perlindungan",
            "saran": (
                "Kualitas udara tergolong kurang sehat dan dapat mengganggu pernapasan. "
                "Kegiatan luar ruangan sebaiknya dibatasi, terutama untuk anak-anak, lansia, dan orang dengan gangguan pernapasan."
            ),
            "aksi": [
                "Tunda kegiatan luar ruangan yang tidak mendesak.",
                "Gunakan masker dengan penyaring baik jika harus keluar.",
                "Tutup jendela jika udara luar terasa lebih kotor.",
            ],
        },
    }

    return data.get(kategori, data["MEDIUM"])


def ambil_anjuran_tambahan(kategori, tipe_pengguna, aktivitas, durasi, waktu):
    kategori = normalisasi_kategori(kategori)

    masker = "Masker tidak wajib, tetapi boleh digunakan jika berada di area padat kendaraan."
    aktivitas_saran = "Kegiatan dapat dilakukan secara normal."
    perlindungan = "Bawa air minum dan perhatikan kondisi tubuh."
    tabir_surya = "Tabir surya disarankan jika kegiatan dilakukan di luar ruangan pada siang hari."

    if kategori == "MEDIUM":
        masker = "Gunakan masker jika berada di jalan ramai atau area berdebu."
        aktivitas_saran = "Kurangi kegiatan luar ruangan yang terlalu lama, terutama untuk kelompok sensitif."
        perlindungan = "Pilih rute yang lebih teduh dan kurangi paparan asap kendaraan."

    if kategori == "UNHEALTHY":
        masker = "Gunakan masker dengan penyaring baik jika harus keluar rumah."
        aktivitas_saran = "Hindari kegiatan berat di luar ruangan dan batasi lama berada di luar."
        perlindungan = "Utamakan berada di dalam ruangan, tutup jendela, dan hindari area padat kendaraan."

    if tipe_pengguna in ["Anak-anak", "Lansia", "Gangguan pernapasan"]:
        aktivitas_saran += " Kelompok sensitif perlu lebih berhati-hati."
        masker += " Pemakaian masker lebih disarankan untuk kelompok ini."

    if aktivitas == "Olahraga luar ruangan":
        if kategori == "GOOD":
            aktivitas_saran = "Olahraga luar ruangan masih dapat dilakukan, tetapi pilih tempat yang tidak terlalu padat kendaraan."
        elif kategori == "MEDIUM":
            aktivitas_saran = "Olahraga berat sebaiknya dikurangi. Pilih olahraga ringan dengan waktu lebih singkat."
        else:
            aktivitas_saran = "Olahraga luar ruangan sebaiknya ditunda sampai udara lebih baik."

    if aktivitas == "Perjalanan kerja atau sekolah":
        perlindungan += " Pilih rute yang lebih sedikit asap kendaraan jika memungkinkan."

    if durasi == "Lebih dari 1 jam":
        perlindungan += " Karena waktunya cukup lama, siapkan masker dan kurangi paparan langsung."

    if waktu == "Siang":
        tabir_surya = "Jika keluar pada siang hari, gunakan tabir surya, topi, dan pakaian yang nyaman."
    elif aktivitas == "Di dalam ruangan":
        tabir_surya = "Tabir surya tidak menjadi hal utama jika kegiatan sepenuhnya di dalam ruangan."
    else:
        tabir_surya = "Tabir surya dapat dipertimbangkan jika kegiatan luar ruangan berlangsung cukup lama."

    return {
        "Masker": masker,
        "Kegiatan": aktivitas_saran,
        "Perlindungan diri": perlindungan,
        "Tabir surya": tabir_surya,
    }


def buat_grafik(nilai_input):
    if not HAS_PLOTLY:
        return None

    df = buat_dataframe_grafik(nilai_input)
    fig = px.bar(df, x="Nilai", y="Jenis Polutan", orientation="h", text_auto=".1f")
    fig.update_traces(
        marker_color="#43766C",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Nilai: %{x}<extra></extra>",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=28, t=10, b=0),
        xaxis_title=None,
        yaxis_title=None,
        font=dict(color="#2E2A27", family="Inter, sans-serif", size=13),
        xaxis=dict(showgrid=True, gridcolor="rgba(67,118,108,0.12)", zeroline=False),
        yaxis=dict(showgrid=False),
        height=360,
    )
    return fig


def tampilkan_kepala_atas():
    st.markdown(
        """
        <div class="kepala-atas">
            <div class="merek">
                <div class="ikon-merek">☁️</div>
                <div>
                    <div class="judul-merek">Sistem Kualitas Udara Jakarta</div>
                    <div class="teks-merek">Alur kerja data, klasifikasi udara, dan anjuran kegiatan</div>
                </div>
            </div>
            <div class="label-status">Aplikasi penelitian berbasis data</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tampilkan_pahlawan():
    st.markdown(
        """
        <section class="pahlawan">
            <div class="pahlawan-kisi">
                <div>
                    <div class="lencana-atas">ALUR KERJA DATA UNTUK KUALITAS UDARA</div>
                    <h1 class="judul-pahlawan huruf-judul">Cek kualitas udara Jakarta dengan alur penelitian yang jelas</h1>
                    <p class="teks-pahlawan">
                        Aplikasi ini menerima angka polutan, mengolahnya dengan model yang sudah dibuat dari data,
                        lalu menampilkan kategori udara, polutan paling tinggi, grafik, dan anjuran tindakan yang mudah dipahami.
                    </p>
                </div>
                <div class="sisi-pahlawan">
                    <div class="kartu-pahlawan">
                        <div class="judul-kartu-pahlawan">Arah penelitian</div>
                        <p class="teks-kartu-pahlawan">
                            Sistem mengikuti alur CRISP-DM, yaitu alur kerja data dari memahami masalah sampai menerapkan hasil ke aplikasi.
                        </p>
                    </div>
                    <div class="kartu-pahlawan">
                        <div class="judul-kartu-pahlawan">Untuk siapa?</div>
                        <p class="teks-kartu-pahlawan">
                            Mahasiswa, dosen, peneliti, komunitas lingkungan, dan masyarakat umum yang ingin memahami simulasi kualitas udara.
                        </p>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def tampilkan_ringkasan():
    st.markdown(
        """
        <section class="panel">
            <div class="kepala-panel">
                <div class="bungkus-judul-panel">
                    <div class="teks-atas">Ringkasan Sistem</div>
                    <h2 class="judul-panel huruf-judul">Masukan, proses, hasil, dan manfaat</h2>
                    <p class="teks-panel">
                        Sistem ini tidak hanya menampilkan angka. Sistem membantu mengubah data udara menjadi penjelasan
                        yang lebih jelas agar pengguna dapat memahami kondisi udara dan tindakan yang perlu dilakukan.
                    </p>
                </div>
            </div>
            <div class="kisi-ringkasan">
                <div class="kartu-ringkasan">
                    <div class="angka-kecil">01</div>
                    <div class="label-kartu">Masukan</div>
                    <div class="nilai-kartu">6 polutan</div>
                    <p class="teks-kartu">PM10, PM2.5, SO2, CO, O3, dan NO2 menjadi nilai utama yang dimasukkan pengguna.</p>
                </div>
                <div class="kartu-ringkasan">
                    <div class="angka-kecil">02</div>
                    <div class="label-kartu">Proses</div>
                    <div class="nilai-kartu">Model data</div>
                    <p class="teks-kartu">Model membaca pola angka polutan untuk menentukan kondisi udara.</p>
                </div>
                <div class="kartu-ringkasan">
                    <div class="angka-kecil">03</div>
                    <div class="label-kartu">Hasil</div>
                    <div class="nilai-kartu">3 kategori</div>
                    <p class="teks-kartu">Hasil utama berupa Baik, Sedang, atau Kurang Sehat.</p>
                </div>
                <div class="kartu-ringkasan">
                    <div class="angka-kecil">04</div>
                    <div class="label-kartu">Manfaat</div>
                    <div class="nilai-kartu">Anjuran</div>
                    <p class="teks-kartu">Sistem memberi saran kegiatan, masker, perlindungan diri, dan tabir surya jika diperlukan.</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def tampilkan_beranda():
    st.markdown(
        """
        <section class="panel">
            <div class="kepala-panel">
                <div class="bungkus-judul-panel">
                    <div class="teks-atas">Halaman Awal</div>
                    <h2 class="judul-panel huruf-judul">Apa inti dari aplikasi ini?</h2>
                    <p class="teks-panel">
                        Inti aplikasi ini adalah membantu pengguna memahami kualitas udara Jakarta.
                        Pengguna memasukkan angka polutan, lalu sistem menampilkan kondisi udara dan anjuran yang mudah dipahami.
                    </p>
                </div>
            </div>
            <div class="kisi-info">
                <div class="kartu-info">
                    <div class="nomor-info">1</div>
                    <div class="judul-info">Media edukasi</div>
                    <p class="teks-info">Pengguna dapat memahami hubungan antara angka polutan dan kondisi udara.</p>
                </div>
                <div class="kartu-info">
                    <div class="nomor-info">2</div>
                    <div class="judul-info">Simulasi data udara</div>
                    <p class="teks-info">Pengguna dapat mencoba contoh nilai atau memasukkan angka dari data yang dimiliki.</p>
                </div>
                <div class="kartu-info">
                    <div class="nomor-info">3</div>
                    <div class="judul-info">Anjuran praktis</div>
                    <p class="teks-info">Sistem memberi saran kegiatan dan perlindungan diri sesuai hasil kategori udara.</p>
                </div>
            </div>
            <div class="catatan-bawah">
                Aplikasi ini paling tepat diposisikan sebagai rancangan awal penelitian terapan,
                bukan alat resmi pengganti pemantauan kualitas udara pemerintah.
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def tampilkan_alur_kerja_data():
    kartu = ""

    for tahap in TAHAP_KERJA:
        kartu += f"""
        <div class="kartu-tahap">
            <div class="nomor-tahap">{tahap["nomor"]}</div>
            <div class="judul-tahap">{tahap["judul"]}</div>
            <div class="isi-tahap">{tahap["isi"]}</div>
            <div class="hasil-tahap">{tahap["hasil"]}</div>
        </div>
        """

    st.markdown(
        f"""
        <section class="panel">
            <div class="kepala-panel">
                <div class="bungkus-judul-panel">
                    <div class="teks-atas">CRISP-DM</div>
                    <h2 class="judul-panel huruf-judul">Alur kerja data pada penelitian ini</h2>
                    <p class="teks-panel">
                        CRISP-DM digunakan agar penelitian berjalan rapi. Tahapannya dimulai dari memahami masalah,
                        memahami data, menyiapkan data, membuat model, menilai hasil, sampai menerapkan sistem ke aplikasi.
                    </p>
                </div>
            </div>
            <div class="kisi-tahap">
                {kartu}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_field(item, value, key_prefix):
    st.markdown('<div class="bungkus-kolom">', unsafe_allow_html=True)
    nilai = st.number_input(
        item["label"],
        min_value=0.0,
        value=float(value),
        step=1.0,
        key=f"{key_prefix}_{item['kolom']}",
    )
    st.markdown(f'<div class="keterangan-kolom">{item["penjelasan"]}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    return nilai


def tampilkan_form_cek_udara():
    st.markdown(
        """
        <section class="panel">
            <div class="kepala-panel">
                <div class="bungkus-judul-panel">
                    <div class="teks-atas">Tahap Penerapan</div>
                    <h2 class="judul-panel huruf-judul">Cek kualitas udara berdasarkan angka polutan</h2>
                    <p class="teks-panel">
                        Pilih contoh nilai jika hanya ingin mencoba. Gunakan isi sendiri jika memiliki data dari alat ukur,
                        kumpulan data, laporan kualitas udara, atau hasil pengukuran lain.
                    </p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.form("form_kualitas_udara"):
        st.markdown('<div class="bagian-form">', unsafe_allow_html=True)

        col_a, col_b, col_c, col_d = st.columns(4, gap="medium")

        with col_a:
            contoh = st.selectbox(
                "Pilihan nilai",
                list(CONTOH_NILAI.keys()),
                index=1,
                key="pilihan_nilai",
            )

        with col_b:
            tipe_pengguna = st.selectbox(
                "Jenis pengguna",
                ["Umum", "Anak-anak", "Lansia", "Gangguan pernapasan", "Pekerja luar ruangan"],
                key="tipe_pengguna",
            )

        with col_c:
            aktivitas = st.selectbox(
                "Rencana kegiatan",
                ["Di dalam ruangan", "Perjalanan kerja atau sekolah", "Olahraga luar ruangan", "Kegiatan luar ruangan ringan"],
                key="aktivitas",
            )

        with col_d:
            durasi = st.selectbox(
                "Lama kegiatan",
                ["Kurang dari 30 menit", "30 sampai 60 menit", "Lebih dari 1 jam"],
                key="durasi",
            )

        waktu = st.selectbox(
            "Waktu kegiatan",
            ["Pagi", "Siang", "Sore atau Malam"],
            key="waktu_kegiatan",
        )

        st.markdown(
            """
            <div class="kotak-catatan">
                <div class="judul-catatan">Catatan masukan</div>
                <p class="teks-catatan">
                    Sistem menerima angka polutan sebagai masukan. Jika pengguna belum memiliki data asli,
                    contoh nilai dapat digunakan agar alur masukan, proses, dan hasil tetap mudah dipahami.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        nilai_awal = ambil_contoh_nilai(contoh)
        key_prefix = contoh.lower().replace(" ", "_")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            nilai_pm10 = render_field(INFO_POLUSI[0], nilai_awal[0], key_prefix)
            nilai_pm25 = render_field(INFO_POLUSI[1], nilai_awal[1], key_prefix)
            nilai_so2 = render_field(INFO_POLUSI[2], nilai_awal[2], key_prefix)

        with col2:
            nilai_co = render_field(INFO_POLUSI[3], nilai_awal[3], key_prefix)
            nilai_o3 = render_field(INFO_POLUSI[4], nilai_awal[4], key_prefix)
            nilai_no2 = render_field(INFO_POLUSI[5], nilai_awal[5], key_prefix)

        tombol = st.form_submit_button("Proses dan tampilkan hasil", type="primary", width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    if tombol:
        nilai_input = [nilai_pm10, nilai_pm25, nilai_so2, nilai_co, nilai_o3, nilai_no2]
        tampilkan_hasil_analisis(nilai_input, tipe_pengguna, aktivitas, durasi, waktu)


def tampilkan_hasil_analisis(nilai_input, tipe_pengguna, aktivitas, durasi, waktu):
    with st.spinner("Sedang membaca data udara..."):
        try:
            df_input = buat_dataframe_input(nilai_input)
            kategori = normalisasi_kategori(model.predict(df_input)[0])
            status = ambil_ringkasan_status(kategori)
            zat_nama, zat_nilai = cari_zat_tertinggi(nilai_input)
            grafik = buat_grafik(nilai_input)
            anjuran = ambil_anjuran_tambahan(kategori, tipe_pengguna, aktivitas, durasi, waktu)
            kategori_tampil = ubah_nama_kategori(kategori)

            st.markdown(
                f"""
                <section class="panel">
                    <div class="kepala-panel">
                        <div class="bungkus-judul-panel">
                            <div class="teks-atas">Hasil Pembacaan</div>
                            <h2 class="judul-panel huruf-judul">Kesimpulan kondisi udara dan anjuran tindakan</h2>
                            <p class="teks-panel">
                                Bagian ini menunjukkan kategori udara, polutan paling tinggi, dan saran tindakan berdasarkan kegiatan pengguna.
                            </p>
                        </div>
                    </div>
                    <div class="kisi-hasil">
                        <div class="kartu-hasil status-{status['kelas']}">
                            <div class="lencana-hasil">{status['badge']}</div>
                            <h3 class="judul-hasil huruf-judul">{status['judul']}</h3>
                            <p class="teks-hasil">{status['saran']}</p>
                            <div class="daftar-saran">
                                <div class="isi-saran">Langkah 1: {status['aksi'][0]}</div>
                                <div class="isi-saran">Langkah 2: {status['aksi'][1]}</div>
                                <div class="isi-saran">Langkah 3: {status['aksi'][2]}</div>
                            </div>
                            <div class="kisi-sorotan">
                                <div class="kotak-sorotan">
                                    <div class="label-sorotan">Kategori udara</div>
                                    <div class="nilai-sorotan">{kategori_tampil}</div>
                                </div>
                                <div class="kotak-sorotan">
                                    <div class="label-sorotan">Polutan paling tinggi</div>
                                    <div class="nilai-sorotan">{zat_nama}</div>
                                </div>
                                <div class="kotak-sorotan">
                                    <div class="label-sorotan">Nilai tertinggi</div>
                                    <div class="nilai-sorotan">{zat_nilai}</div>
                                </div>
                                <div class="kotak-sorotan">
                                    <div class="label-sorotan">Jenis pengguna</div>
                                    <div class="nilai-sorotan">{tipe_pengguna}</div>
                                </div>
                            </div>
                        </div>
                        <div class="kartu-hasil">
                            <div class="teks-atas">Anjuran Tambahan</div>
                            <h3 class="judul-hasil huruf-judul" style="font-size:1.35rem;">Saran berdasarkan kegiatan pengguna</h3>
                            <div class="kisi-anjuran">
                                <div class="kartu-anjuran">
                                    <div class="judul-anjuran">Masker</div>
                                    <p class="teks-anjuran">{anjuran['Masker']}</p>
                                </div>
                                <div class="kartu-anjuran">
                                    <div class="judul-anjuran">Kegiatan</div>
                                    <p class="teks-anjuran">{anjuran['Kegiatan']}</p>
                                </div>
                                <div class="kartu-anjuran">
                                    <div class="judul-anjuran">Perlindungan diri</div>
                                    <p class="teks-anjuran">{anjuran['Perlindungan diri']}</p>
                                </div>
                                <div class="kartu-anjuran">
                                    <div class="judul-anjuran">Tabir surya</div>
                                    <p class="teks-anjuran">{anjuran['Tabir surya']}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <section class="panel">
                    <div class="kepala-panel">
                        <div class="bungkus-judul-panel">
                            <div class="teks-atas">Gambaran Angka</div>
                            <h2 class="judul-panel huruf-judul">Perbandingan nilai setiap polutan</h2>
                            <p class="teks-panel">
                                Grafik membantu pengguna melihat jenis polutan yang nilainya paling menonjol.
                            </p>
                        </div>
                    </div>
                    <div class="isi-panel">
                """,
                unsafe_allow_html=True,
            )

            if grafik is not None:
                st.plotly_chart(grafik, width="stretch", config={"displayModeBar": False})
            else:
                df_chart = buat_dataframe_grafik(nilai_input).set_index("Jenis Polutan")
                st.bar_chart(df_chart, width="stretch")

            df_ringkasan = pd.DataFrame(
                {
                    "Parameter": ["PM10", "PM2.5", "SO2", "CO", "O3", "NO2"],
                    "Nilai": nilai_input,
                }
            )
            st.dataframe(df_ringkasan, width="stretch", hide_index=True)
            st.markdown("</div></section>", unsafe_allow_html=True)

        except Exception as error:
            st.error("Data belum bisa diproses. Periksa kembali model, file, atau nilai masukan.")
            st.code(str(error))


def tampilkan_panduan():
    st.markdown(
        """
        <section class="panel">
            <div class="kepala-panel">
                <div class="bungkus-judul-panel">
                    <div class="teks-atas">Panduan Singkat</div>
                    <h2 class="judul-panel huruf-judul">Cara menggunakan aplikasi</h2>
                    <p class="teks-panel">
                        Aplikasi ini dibuat agar pengguna tetap bisa mencoba alurnya meskipun belum memiliki data asli.
                    </p>
                </div>
            </div>
            <div class="kisi-info">
                <div class="kartu-info">
                    <div class="nomor-info">1</div>
                    <div class="judul-info">Pilih contoh nilai</div>
                    <p class="teks-info">Gunakan contoh nilai untuk simulasi atau isi sendiri jika memiliki data polutan.</p>
                </div>
                <div class="kartu-info">
                    <div class="nomor-info">2</div>
                    <div class="judul-info">Pilih jenis pengguna</div>
                    <p class="teks-info">Jenis pengguna membantu sistem memberi anjuran yang lebih sesuai.</p>
                </div>
                <div class="kartu-info">
                    <div class="nomor-info">3</div>
                    <div class="judul-info">Isi enam nilai polutan</div>
                    <p class="teks-info">Masukkan PM10, PM2.5, SO2, CO, O3, dan NO2.</p>
                </div>
                <div class="kartu-info">
                    <div class="nomor-info">4</div>
                    <div class="judul-info">Tekan tombol proses</div>
                    <p class="teks-info">Sistem akan membaca angka dan menentukan kategori udara.</p>
                </div>
                <div class="kartu-info">
                    <div class="nomor-info">5</div>
                    <div class="judul-info">Baca hasil kategori</div>
                    <p class="teks-info">Hasil utama berupa Baik, Sedang, atau Kurang Sehat.</p>
                </div>
                <div class="kartu-info">
                    <div class="nomor-info">6</div>
                    <div class="judul-info">Ikuti anjuran</div>
                    <p class="teks-info">Anjuran mencakup kegiatan, masker, perlindungan diri, dan tabir surya jika diperlukan.</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def main():
    terapkan_css()
    tampilkan_kepala_atas()
    tampilkan_pahlawan()
    tampilkan_ringkasan()

    st.markdown('<div class="wadah-menu">', unsafe_allow_html=True)
    menu = st.radio(
        "Navigasi",
        ["Beranda", "Alur Kerja Data", "Cek Kualitas Udara", "Panduan"],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if menu == "Beranda":
        tampilkan_beranda()
    elif menu == "Alur Kerja Data":
        tampilkan_alur_kerja_data()
    elif menu == "Cek Kualitas Udara":
        tampilkan_form_cek_udara()
    else:
        tampilkan_panduan()


if __name__ == "__main__":
    main()