import os
import pickle
import textwrap

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sistem Kualitas Udara Jakarta",
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
        "penjelasan": "Gas yang sering berasal dari pembakaran bahan bakar tertentu.",
    },
    {
        "label": "Gas Karbon (CO)",
        "kolom": "CO",
        "default": 12.0,
        "penjelasan": "Gas yang sering muncul dari asap kendaraan dan pembakaran tidak sempurna.",
    },
    {
        "label": "Ozon Permukaan (O3)",
        "kolom": "O3",
        "default": 30.0,
        "penjelasan": "Polutan yang dapat terbentuk saat polusi bereaksi dengan panas matahari.",
    },
    {
        "label": "Gas Nitrogen (NO2)",
        "kolom": "NO2",
        "default": 22.0,
        "penjelasan": "Gas yang sering berkaitan dengan asap kendaraan dan aktivitas perkotaan.",
    },
]

PRESET_INPUT = {
    "Contoh Udara Baik": [32.0, 38.0, 18.0, 7.0, 18.0, 12.0],
    "Contoh Udara Sedang": [65.0, 78.0, 28.0, 13.0, 36.0, 22.0],
    "Contoh Udara Kurang Sehat": [120.0, 145.0, 40.0, 22.0, 58.0, 36.0],
    "Input Manual": [45.0, 65.0, 15.0, 12.0, 30.0, 22.0],
}


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
        --radius-xxl: 32px;
        --radius-xl: 26px;
        --radius-lg: 20px;
        --radius-md: 16px;
        --transisi: all 0.25s ease;
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

    h1, h2, h3, h4, .serif {
        font-family: 'Playfair Display', serif !important;
        letter-spacing: -0.035em;
    }

    p, li, label, span, div {
        word-wrap: break-word;
    }

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 18px;
        margin-bottom: 18px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-mark {
        width: 44px;
        height: 44px;
        border-radius: 16px;
        display: grid;
        place-items: center;
        background: linear-gradient(135deg, var(--utama) 0%, var(--utama-gelap) 100%);
        color: var(--latar);
        font-size: 1.35rem;
        box-shadow: var(--bayangan-tipis);
    }

    .brand-title {
        color: var(--cokelat);
        font-weight: 900;
        font-size: 1.05rem;
        line-height: 1.2;
    }

    .brand-subtitle {
        color: var(--teks-lembut);
        font-size: 0.86rem;
        line-height: 1.4;
        margin-top: 2px;
    }

    .status-pill {
        padding: 10px 14px;
        border-radius: 999px;
        background: rgba(255, 253, 247, 0.78);
        border: 1px solid var(--garis);
        color: var(--utama-gelap);
        font-size: 0.88rem;
        font-weight: 800;
        box-shadow: var(--bayangan-tipis);
        white-space: nowrap;
    }

    .hero {
        position: relative;
        overflow: hidden;
        border-radius: var(--radius-xxl);
        background:
            radial-gradient(circle at 88% 12%, rgba(248, 250, 229, 0.18), transparent 28%),
            linear-gradient(135deg, #43766C 0%, #345E56 48%, #294B45 100%);
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: var(--bayangan);
        padding: 38px;
        margin-bottom: 22px;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.35fr) minmax(300px, 0.82fr);
        gap: 24px;
        align-items: stretch;
    }

    .hero-badge {
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

    .hero-title {
        color: #F8FAE5 !important;
        font-size: clamp(2.15rem, 5vw, 4rem);
        line-height: 1.02;
        margin: 0 0 16px 0;
        max-width: 820px;
    }

    .hero-text {
        color: rgba(248, 250, 229, 0.90);
        font-size: 1.04rem;
        line-height: 1.78;
        margin: 0;
        max-width: 780px;
    }

    .hero-side {
        display: grid;
        gap: 14px;
    }

    .hero-mini {
        background: rgba(255, 255, 255, 0.11);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 22px;
        padding: 18px;
        backdrop-filter: blur(8px);
    }

    .hero-mini-label {
        color: #F8FAE5;
        font-size: 0.9rem;
        font-weight: 900;
        margin-bottom: 7px;
    }

    .hero-mini-text {
        color: rgba(248, 250, 229, 0.86);
        font-size: 0.94rem;
        line-height: 1.68;
        margin: 0;
    }

    .nav-wrap {
        margin-bottom: 22px;
    }

    div[data-testid="stRadio"] > div {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        background: rgba(255, 253, 247, 0.78);
        border: 1px solid var(--garis);
        border-radius: 24px;
        padding: 12px;
        box-shadow: var(--bayangan-tipis);
    }

    div[data-testid="stRadio"] label {
        min-height: 68px;
        border-radius: 18px !important;
        background: #FFFEFB !important;
        border: 1px solid transparent !important;
        padding: 14px 18px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: var(--transisi);
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
        font-size: 0.97rem !important;
        font-weight: 900 !important;
        text-align: center;
    }

    div[data-testid="stRadio"] label[data-checked="true"] p,
    div[data-testid="stRadio"] label:has(input:checked) p {
        color: #FFFFFF !important;
    }

    .panel {
        background: rgba(255, 253, 247, 0.88);
        border: 1px solid var(--garis);
        border-radius: var(--radius-xxl);
        box-shadow: var(--bayangan);
        margin-bottom: 22px;
        overflow: hidden;
    }

    .panel-pad {
        padding: 26px;
    }

    .panel-head {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 18px;
        padding: 26px 26px 0 26px;
    }

    .panel-title-wrap {
        max-width: 860px;
    }

    .overline {
        color: var(--utama);
        font-size: 0.8rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        margin-bottom: 9px;
    }

    .panel-title {
        color: var(--cokelat) !important;
        font-size: clamp(1.48rem, 2.5vw, 2.25rem);
        line-height: 1.14;
        margin: 0 0 10px 0;
    }

    .panel-subtitle {
        color: var(--teks-lembut);
        font-size: 1rem;
        line-height: 1.76;
        margin: 0;
    }

    .mini-note {
        min-width: 260px;
        max-width: 340px;
        padding: 16px 18px;
        border-radius: 20px;
        background: var(--utama-muda);
        border: 1px solid rgba(67, 118, 108, 0.16);
        color: var(--utama-gelap);
        font-size: 0.93rem;
        line-height: 1.65;
        font-weight: 700;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
        padding: 26px;
    }

    .stat-card {
        background: linear-gradient(180deg, #FFFFFF 0%, #FBF9F4 100%);
        border: 1px solid var(--garis);
        border-radius: 22px;
        padding: 19px;
        min-height: 134px;
    }

    .stat-icon {
        width: 38px;
        height: 38px;
        border-radius: 14px;
        display: grid;
        place-items: center;
        background: var(--utama-muda);
        color: var(--utama-gelap);
        font-size: 1.15rem;
        margin-bottom: 12px;
    }

    .stat-label {
        color: var(--teks-lembut);
        font-size: 0.86rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .stat-value {
        color: var(--cokelat);
        font-size: 1.38rem;
        font-weight: 900;
        line-height: 1.22;
        margin-bottom: 7px;
    }

    .stat-desc {
        color: var(--teks-lembut);
        font-size: 0.91rem;
        line-height: 1.62;
    }

    .info-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
        padding: 0 26px 26px 26px;
    }

    .info-card {
        background: #FFFEFB;
        border: 1px solid var(--garis);
        border-radius: 22px;
        padding: 19px;
        min-height: 178px;
    }

    .info-number {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: inline-grid;
        place-items: center;
        background: var(--utama-muda);
        color: var(--utama-gelap);
        font-weight: 900;
        margin-bottom: 13px;
    }

    .info-title {
        color: var(--cokelat);
        font-size: 1rem;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .info-text {
        color: var(--teks-lembut);
        line-height: 1.72;
        font-size: 0.94rem;
        margin: 0;
    }

    .form-section {
        padding: 26px;
    }

    div[data-testid="stForm"] {
        border: 0 !important;
        background: transparent !important;
        padding: 0 !important;
        box-shadow: none !important;
    }

    .control-box {
        background: #FFFEFB;
        border: 1px solid var(--garis);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 16px;
    }

    .control-title {
        color: var(--cokelat);
        font-weight: 900;
        font-size: 0.98rem;
        margin-bottom: 8px;
    }

    .control-text {
        color: var(--teks-lembut);
        font-size: 0.9rem;
        line-height: 1.65;
        margin: 0;
    }

    .field-wrap {
        background: #FFFEFB;
        border: 1px solid var(--garis);
        border-radius: 20px;
        padding: 15px 15px 8px 15px;
        height: 100%;
        transition: var(--transisi);
    }

    .field-wrap:hover {
        border-color: rgba(67, 118, 108, 0.26);
        box-shadow: 0 10px 20px rgba(67, 118, 108, 0.06);
    }

    .field-caption {
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
        margin-top: 10px;
    }

    div[data-testid="stFormSubmitButton"] > button,
    button[kind="primary"] {
        width: 100% !important;
        min-height: 56px !important;
        border-radius: 17px !important;
        border: none !important;
        background: linear-gradient(135deg, var(--utama) 0%, var(--utama-gelap) 100%) !important;
        color: white !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
        box-shadow: 0 16px 24px rgba(67, 118, 108, 0.22) !important;
        transition: var(--transisi) !important;
    }

    div[data-testid="stFormSubmitButton"] > button:hover,
    button[kind="primary"]:hover {
        transform: translateY(-1px);
        filter: brightness(0.98);
    }

    .result-grid {
        display: grid;
        grid-template-columns: minmax(300px, 0.9fr) minmax(0, 1.35fr);
        gap: 18px;
        padding: 0 26px 26px 26px;
    }

    .result-card {
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

    .badge {
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

    .result-title {
        color: var(--cokelat) !important;
        font-size: 1.72rem;
        line-height: 1.18;
        margin: 0 0 12px 0;
    }

    .result-text {
        color: var(--teks);
        line-height: 1.78;
        margin-bottom: 18px;
    }

    .action-list {
        display: grid;
        gap: 10px;
        margin-top: 12px;
    }

    .action-item {
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

    .highlight-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
        margin-top: 16px;
    }

    .highlight-box {
        background: #FFFFFF;
        border: 1px solid var(--garis);
        border-radius: 18px;
        padding: 16px;
    }

    .highlight-label {
        color: var(--teks-lembut);
        font-size: 0.84rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .highlight-value {
        color: var(--cokelat);
        font-size: 1.18rem;
        line-height: 1.35;
        font-weight: 900;
    }

    .recommendation-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
        margin-top: 16px;
    }

    .recommendation-card {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid var(--garis);
        border-radius: 18px;
        padding: 16px;
    }

    .recommendation-title {
        color: var(--cokelat);
        font-weight: 900;
        margin-bottom: 8px;
    }

    .recommendation-text {
        color: var(--teks-lembut);
        font-size: 0.92rem;
        line-height: 1.68;
        margin: 0;
    }

    .dataframe-wrap {
        margin-top: 12px;
    }

    .foot-note {
        color: var(--teks-lembut);
        font-size: 0.92rem;
        line-height: 1.72;
        padding: 18px 26px 26px 26px;
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

        .stats-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 1080px) {
        .hero-grid,
        .result-grid,
        .info-grid {
            grid-template-columns: 1fr;
        }

        .panel-head {
            flex-direction: column;
        }

        .mini-note {
            max-width: none;
            width: 100%;
        }
    }

    @media (max-width: 920px) {
        div[data-testid="stRadio"] > div,
        .highlight-grid,
        .recommendation-grid,
        .stats-grid {
            grid-template-columns: 1fr;
        }

        div[data-testid="stRadio"] label {
            min-height: 56px;
        }

        .topbar {
            align-items: flex-start;
            flex-direction: column;
        }

        .status-pill {
            white-space: normal;
        }
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 18px 16px 36px 16px;
        }

        .hero {
            padding: 24px 18px;
            border-radius: 24px;
        }

        .hero-title {
            font-size: 2rem;
        }

        .hero-text,
        .panel-subtitle,
        .info-text,
        .field-caption,
        .result-text,
        .recommendation-text,
        .control-text {
            font-size: 0.94rem;
        }

        .panel,
        .result-card,
        .stat-card,
        .info-card,
        .highlight-box,
        .field-wrap,
        .control-box,
        .recommendation-card {
            border-radius: 20px;
        }

        .panel-head,
        .panel-pad,
        .form-section,
        .stats-grid,
        .result-grid,
        .info-grid,
        .foot-note {
            padding-left: 16px;
            padding-right: 16px;
        }
    }

    @media (max-width: 560px) {
        .brand-mark {
            width: 40px;
            height: 40px;
            border-radius: 14px;
        }

        .hero-badge {
            font-size: 0.72rem;
            line-height: 1.4;
            align-items: flex-start;
        }

        .hero-title {
            font-size: 1.66rem;
        }

        .panel-title {
            font-size: 1.34rem;
        }

        .result-title {
            font-size: 1.30rem;
        }

        .stat-value,
        .highlight-value {
            font-size: 1.08rem;
        }

        .panel-head {
            padding-top: 20px;
        }

        .stats-grid,
        .form-section,
        .result-grid,
        .info-grid {
            gap: 12px;
        }
    }

    @media (max-width: 420px) {
        .block-container {
            padding-left: 12px;
            padding-right: 12px;
        }

        .hero {
            padding: 20px 14px;
        }

        .hero-title {
            font-size: 1.48rem;
        }

        .hero-mini,
        .stat-card,
        .info-card,
        .result-card,
        .control-box,
        .field-wrap,
        .recommendation-card {
            padding: 14px;
        }

        .action-item {
            padding: 10px 12px;
        }
    }
    </style>
    """
    st.markdown(textwrap.dedent(css), unsafe_allow_html=True)


def ambil_preset(nama_preset):
    return PRESET_INPUT.get(nama_preset, PRESET_INPUT["Input Manual"])


def buat_dataframe_input(nilai_input):
    return pd.DataFrame([nilai_input], columns=KOLOM_MODEL)


def buat_dataframe_grafik(nilai_input):
    df = pd.DataFrame(
        {
            "Jenis Polutan": ["PM10", "PM2.5", "SO2", "CO", "O3", "NO2"],
            "Nilai": nilai_input,
        }
    )
    return df.sort_values("Nilai", ascending=True)


def cari_zat_tertinggi(nilai_input):
    pasangan = {item["label"]: nilai for item, nilai in zip(INFO_POLUSI, nilai_input)}
    nama = max(pasangan, key=pasangan.get)
    return nama, pasangan[nama]


def normalisasi_kategori(kategori):
    if kategori == "VERY_UNHEALTHY":
        return "UNHEALTHY"
    return kategori


def ambil_ringkasan_status(kategori):
    kategori = normalisasi_kategori(kategori)

    data = {
        "GOOD": {
            "judul": "Udara Bersih dan Nyaman",
            "kelas": "baik",
            "badge": "Aman",
            "saran": (
                "Kondisi udara tergolong baik. Aktivitas harian masih dapat dilakukan dengan nyaman. "
                "Pengguna tetap disarankan menjaga kebersihan lingkungan dan memantau kondisi jika beraktivitas lama di luar."
            ),
            "aksi": [
                "Aktivitas luar ruangan dapat dilakukan seperti biasa.",
                "Ventilasi rumah dapat dibuka agar sirkulasi udara tetap baik.",
                "Tetap perhatikan kondisi tubuh jika sensitif terhadap debu.",
            ],
        },
        "MEDIUM": {
            "judul": "Udara Sedang, Perlu Waspada",
            "kelas": "sedang",
            "badge": "Waspada",
            "saran": (
                "Udara masih dapat diterima, tetapi kelompok sensitif sebaiknya mulai berhati-hati. "
                "Aktivitas luar ruangan tetap dapat dilakukan, namun tidak disarankan terlalu lama."
            ),
            "aksi": [
                "Kurangi olahraga berat di luar ruangan.",
                "Gunakan masker saat berada di jalan ramai.",
                "Kelompok sensitif disarankan lebih banyak beraktivitas di dalam ruangan.",
            ],
        },
        "UNHEALTHY": {
            "judul": "Udara Kurang Sehat",
            "kelas": "buruk",
            "badge": "Perlu Perlindungan",
            "saran": (
                "Kualitas udara tergolong kurang sehat dan dapat mengganggu pernapasan. "
                "Aktivitas luar ruangan sebaiknya dibatasi, terutama untuk anak-anak, lansia, dan pengguna dengan gangguan pernapasan."
            ),
            "aksi": [
                "Tunda aktivitas luar ruangan yang tidak mendesak.",
                "Gunakan masker dengan filtrasi baik jika harus keluar.",
                "Tutup jendela jika udara luar terasa lebih kotor dari dalam ruangan.",
            ],
        },
    }

    return data.get(kategori, data["MEDIUM"])


def ambil_rekomendasi_tambahan(kategori, tipe_pengguna, aktivitas, durasi, waktu):
    kategori = normalisasi_kategori(kategori)

    masker = "Masker tidak wajib, tetapi boleh digunakan jika berada di area padat kendaraan."
    aktivitas_saran = "Aktivitas dapat dilakukan secara normal."
    perlindungan = "Bawa air minum dan perhatikan kondisi tubuh."
    sunscreen = "Sunscreen disarankan jika aktivitas dilakukan di luar ruangan pada siang hari."

    if kategori == "MEDIUM":
        masker = "Gunakan masker jika berada di jalan ramai atau area berdebu."
        aktivitas_saran = "Kurangi aktivitas luar ruangan yang terlalu lama, terutama untuk kelompok sensitif."
        perlindungan = "Pilih rute yang lebih teduh dan kurangi paparan asap kendaraan."

    if kategori == "UNHEALTHY":
        masker = "Gunakan masker dengan filtrasi baik jika harus keluar rumah."
        aktivitas_saran = "Hindari aktivitas berat di luar ruangan dan batasi durasi keluar."
        perlindungan = "Utamakan berada di dalam ruangan, tutup jendela, dan hindari area padat kendaraan."

    if tipe_pengguna in ["Anak-anak", "Lansia", "Gangguan pernapasan"]:
        aktivitas_saran = aktivitas_saran + " Kelompok sensitif disarankan lebih berhati-hati."
        masker = masker + " Pemakaian masker lebih disarankan untuk kelompok ini."

    if aktivitas == "Olahraga luar ruangan":
        if kategori == "GOOD":
            aktivitas_saran = "Olahraga luar ruangan masih dapat dilakukan, tetapi tetap pilih area yang tidak terlalu padat kendaraan."
        elif kategori == "MEDIUM":
            aktivitas_saran = "Olahraga berat sebaiknya dikurangi. Pilih olahraga ringan dan durasi lebih singkat."
        else:
            aktivitas_saran = "Olahraga luar ruangan sebaiknya ditunda sampai kondisi udara lebih baik."

    if aktivitas == "Perjalanan kerja/sekolah":
        perlindungan = perlindungan + " Pilih rute yang lebih sedikit paparan asap kendaraan jika memungkinkan."

    if durasi == "Lebih dari 1 jam":
        perlindungan = perlindungan + " Karena durasi cukup lama, siapkan masker dan kurangi paparan langsung."

    if waktu == "Siang":
        sunscreen = "Jika keluar pada siang hari, gunakan sunscreen SPF 30 atau lebih, topi, dan pakaian yang nyaman."
    elif aktivitas == "Di dalam ruangan":
        sunscreen = "Sunscreen tidak menjadi prioritas jika aktivitas sepenuhnya di dalam ruangan."
    else:
        sunscreen = "Sunscreen dapat dipertimbangkan jika aktivitas luar ruangan berlangsung cukup lama."

    return {
        "Masker": masker,
        "Aktivitas": aktivitas_saran,
        "Perlindungan": perlindungan,
        "Sunscreen": sunscreen,
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


def tampilkan_topbar():
    st.markdown(
        """
        <div class="topbar">
            <div class="brand">
                <div class="brand-mark">☁️</div>
                <div>
                    <div class="brand-title">Sistem Kualitas Udara Jakarta</div>
                    <div class="brand-subtitle">Klasifikasi udara, rekomendasi aktivitas, dan edukasi polusi</div>
                </div>
            </div>
            <div class="status-pill">Aplikasi berbasis Machine Learning</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tampilkan_hero():
    st.markdown(
        """
        <section class="hero">
            <div class="hero-grid">
                <div>
                    <div class="hero-badge">SISTEM EDUKASI DAN SIMULASI KUALITAS UDARA</div>
                    <h1 class="hero-title">Cek kualitas udara Jakarta dengan cara yang lebih mudah dipahami</h1>
                    <p class="hero-text">
                        Aplikasi ini mengubah angka polutan menjadi kategori kualitas udara, menampilkan zat yang paling dominan,
                        lalu memberikan rekomendasi aktivitas dan perlindungan diri. Sistem ini dapat digunakan oleh publik
                        sebagai media edukasi, simulasi, dan demonstrasi penerapan machine learning.
                    </p>
                </div>
                <div class="hero-side">
                    <div class="hero-mini">
                        <div class="hero-mini-label">Untuk siapa aplikasi ini?</div>
                        <p class="hero-mini-text">
                            Mahasiswa, peneliti, komunitas lingkungan, dosen, dan masyarakat umum yang ingin memahami simulasi kualitas udara.
                        </p>
                    </div>
                    <div class="hero-mini">
                        <div class="hero-mini-label">Sumber input angka</div>
                        <p class="hero-mini-text">
                            Nilai dapat berasal dari dataset, alat sensor, stasiun pemantau, laporan kualitas udara, atau preset simulasi.
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
            <div class="panel-head">
                <div class="panel-title-wrap">
                    <div class="overline">Ringkasan Proyek</div>
                    <h2 class="panel-title">Sistem klasifikasi udara dengan alur input, proses, dan output</h2>
                    <p class="panel-subtitle">
                        Fokus utama aplikasi ini adalah membantu pengguna memahami kondisi udara dari data polutan.
                        Sistem tidak diklaim sebagai alat resmi pengukuran, melainkan sebagai prototype klasifikasi dan edukasi kualitas udara.
                    </p>
                </div>
            </div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">01</div>
                    <div class="stat-label">Input</div>
                    <div class="stat-value">6 polutan</div>
                    <div class="stat-desc">PM10, PM2.5, SO2, CO, O3, dan NO2 sebagai fitur utama model.</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">02</div>
                    <div class="stat-label">Proses</div>
                    <div class="stat-value">Machine Learning</div>
                    <div class="stat-desc">Model membaca pola input dan mengklasifikasikan kualitas udara.</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">03</div>
                    <div class="stat-label">Output</div>
                    <div class="stat-value">3 kategori</div>
                    <div class="stat-desc">GOOD, MEDIUM, dan UNHEALTHY sebagai hasil utama klasifikasi.</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">04</div>
                    <div class="stat-label">Tambahan</div>
                    <div class="stat-value">Rekomendasi</div>
                    <div class="stat-desc">Saran aktivitas, masker, perlindungan diri, dan sunscreen untuk aktivitas luar ruangan.</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_field(item, value, preset_key):
    st.markdown('<div class="field-wrap">', unsafe_allow_html=True)
    nilai = st.number_input(
        item["label"],
        min_value=0.0,
        value=float(value),
        step=1.0,
        key=f"input_{preset_key}_{item['kolom']}",
    )
    st.markdown(f'<div class="field-caption">{item["penjelasan"]}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    return nilai


def tampilkan_beranda():
    st.markdown(
        """
        <section class="panel">
            <div class="panel-head">
                <div class="panel-title-wrap">
                    <div class="overline">Halaman Awal</div>
                    <h2 class="panel-title">Apa nilai utama dari aplikasi ini?</h2>
                    <p class="panel-subtitle">
                        Aplikasi ini dibuat agar data polusi tidak hanya tampil sebagai angka,
                        tetapi berubah menjadi informasi yang lebih mudah dibaca dan digunakan.
                    </p>
                </div>
            </div>
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-number">1</div>
                    <div class="info-title">Media edukasi publik</div>
                    <p class="info-text">Masyarakat dapat memahami hubungan antara angka polutan dan kondisi udara.</p>
                </div>
                <div class="info-card">
                    <div class="info-number">2</div>
                    <div class="info-title">Simulasi data udara</div>
                    <p class="info-text">Pengguna dapat mencoba preset atau memasukkan angka dari data yang dimiliki.</p>
                </div>
                <div class="info-card">
                    <div class="info-number">3</div>
                    <div class="info-title">Rekomendasi praktis</div>
                    <p class="info-text">Sistem memberi saran aktivitas, masker, dan perlindungan diri sesuai hasil klasifikasi.</p>
                </div>
            </div>
            <div class="foot-note">
                Aplikasi ini paling tepat diposisikan sebagai aplikasis para penelitian terapan, bukan alat resmi pengganti pemantauan kualitas udara pemerintah.
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def tampilkan_form_cek_udara():
    st.markdown(
        """
        <section class="panel">
            <div class="panel-head">
                <div class="panel-title-wrap">
                    <div class="overline">Bagian Utama</div>
                    <h2 class="panel-title">Cek kualitas udara berdasarkan input polutan</h2>
                    <p class="panel-subtitle">
                        Gunakan input manual jika memiliki data dari sensor,
                        dataset, laporan kualitas udara, atau hasil pengukuran lain.
                    </p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.form("form_kualitas_udara"):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)

        col_a, col_b, col_c, col_d = st.columns(4, gap="medium")

        with col_a:
            preset = st.selectbox(
                "Mode input",
                list(PRESET_INPUT.keys()),
                index=1,
                key="preset_input",
            )

        with col_b:
            tipe_pengguna = st.selectbox(
                "Jenis pengguna",
                ["Umum", "Anak-anak", "Lansia", "Gangguan pernapasan", "Pekerja luar ruangan"],
                key="tipe_pengguna",
            )

        with col_c:
            aktivitas = st.selectbox(
                "Rencana aktivitas",
                ["Di dalam ruangan", "Perjalanan kerja/sekolah", "Olahraga luar ruangan", "Aktivitas luar ruangan ringan"],
                key="aktivitas",
            )

        with col_d:
            durasi = st.selectbox(
                "Durasi aktivitas",
                ["Kurang dari 30 menit", "30 sampai 60 menit", "Lebih dari 1 jam"],
                key="durasi",
            )

        waktu = st.selectbox(
            "Waktu aktivitas",
            ["Pagi", "Siang", "Sore/Malam"],
            key="waktu_aktivitas",
        )

        st.markdown(
            """
            <div class="control-box">
                <div class="control-title">Catatan input</div>
                <p class="control-text">
                    Sistem menerima angka polutan sebagai masukan. Jika pengguna umum tidak memiliki data asli,
                    preset dapat digunakan sebagai contoh simulasi agar alur input, proses, dan output tetap mudah dipahami.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        nilai_preset = ambil_preset(preset)
        preset_key = preset.lower().replace(" ", "_")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            nilai_pm10 = render_field(INFO_POLUSI[0], nilai_preset[0], preset_key)
            nilai_pm25 = render_field(INFO_POLUSI[1], nilai_preset[1], preset_key)
            nilai_so2 = render_field(INFO_POLUSI[2], nilai_preset[2], preset_key)

        with col2:
            nilai_co = render_field(INFO_POLUSI[3], nilai_preset[3], preset_key)
            nilai_o3 = render_field(INFO_POLUSI[4], nilai_preset[4], preset_key)
            nilai_no2 = render_field(INFO_POLUSI[5], nilai_preset[5], preset_key)

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
            rekomendasi = ambil_rekomendasi_tambahan(kategori, tipe_pengguna, aktivitas, durasi, waktu)

            st.markdown(
                f"""
                <section class="panel">
                    <div class="panel-head">
                        <div class="panel-title-wrap">
                            <div class="overline">Hasil Pembacaan</div>
                            <h2 class="panel-title">Kesimpulan kondisi udara dan rekomendasi perlindungan</h2>
                            <p class="panel-subtitle">
                                Hasil ini menunjukkan kategori udara, polutan dominan, dan saran tindakan berdasarkan profil aktivitas pengguna.
                            </p>
                        </div>
                    </div>
                    <div class="result-grid">
                        <div class="result-card status-{status['kelas']}">
                            <div class="badge">{status['badge']}</div>
                            <h3 class="result-title serif">{status['judul']}</h3>
                            <p class="result-text">{status['saran']}</p>
                            <div class="action-list">
                                <div class="action-item">Langkah 1: {status['aksi'][0]}</div>
                                <div class="action-item">Langkah 2: {status['aksi'][1]}</div>
                                <div class="action-item">Langkah 3: {status['aksi'][2]}</div>
                            </div>
                            <div class="highlight-grid">
                                <div class="highlight-box">
                                    <div class="highlight-label">Kategori model</div>
                                    <div class="highlight-value">{kategori}</div>
                                </div>
                                <div class="highlight-box">
                                    <div class="highlight-label">Polutan dominan</div>
                                    <div class="highlight-value">{zat_nama}</div>
                                </div>
                                <div class="highlight-box">
                                    <div class="highlight-label">Nilai tertinggi</div>
                                    <div class="highlight-value">{zat_nilai} µg/m³</div>
                                </div>
                                <div class="highlight-box">
                                    <div class="highlight-label">Profil pengguna</div>
                                    <div class="highlight-value">{tipe_pengguna}</div>
                                </div>
                            </div>
                        </div>
                        <div class="result-card">
                            <div class="overline">Rekomendasi Tambahan</div>
                            <h3 class="result-title serif" style="font-size:1.35rem;">Saran berdasarkan aktivitas pengguna</h3>
                            <div class="recommendation-grid">
                                <div class="recommendation-card">
                                    <div class="recommendation-title">Masker</div>
                                    <p class="recommendation-text">{rekomendasi['Masker']}</p>
                                </div>
                                <div class="recommendation-card">
                                    <div class="recommendation-title">Aktivitas</div>
                                    <p class="recommendation-text">{rekomendasi['Aktivitas']}</p>
                                </div>
                                <div class="recommendation-card">
                                    <div class="recommendation-title">Perlindungan diri</div>
                                    <p class="recommendation-text">{rekomendasi['Perlindungan']}</p>
                                </div>
                                <div class="recommendation-card">
                                    <div class="recommendation-title">Sunscreen</div>
                                    <p class="recommendation-text">{rekomendasi['Sunscreen']}</p>
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
                    <div class="panel-head">
                        <div class="panel-title-wrap">
                            <div class="overline">Visualisasi</div>
                            <h2 class="panel-title">Perbandingan nilai setiap polutan</h2>
                            <p class="panel-subtitle">
                                Grafik membantu pengguna melihat polutan mana yang memiliki nilai paling menonjol.
                            </p>
                        </div>
                    </div>
                    <div class="panel-pad">
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
            st.error("Data belum bisa diproses. Periksa kembali model, file, atau nilai input.")
            st.code(str(error))


def tampilkan_cara_penggunaan():
    st.markdown(
        """
        <section class="panel">
            <div class="panel-head">
                <div class="panel-title-wrap">
                    <div class="overline">Panduan Singkat</div>
                    <h2 class="panel-title">Cara menggunakan aplikasi</h2>
                    <p class="panel-subtitle">
                        Aplikasi ini dibuat agar pengguna tidak bingung meskipun belum memiliki data asli.
                        Preset tersedia untuk simulasi, sedangkan input manual dapat digunakan jika memiliki data pengukuran.
                    </p>
                </div>
            </div>
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-number">1</div>
                    <div class="info-title">Pilih mode input</div>
                    <p class="info-text">Gunakan preset untuk simulasi atau input manual jika memiliki data polutan sendiri.</p>
                </div>
                <div class="info-card">
                    <div class="info-number">2</div>
                    <div class="info-title">Pilih profil pengguna</div>
                    <p class="info-text">Profil membantu sistem memberi rekomendasi yang lebih sesuai dengan kebutuhan pengguna.</p>
                </div>
                <div class="info-card">
                    <div class="info-number">3</div>
                    <div class="info-title">Isi enam nilai polutan</div>
                    <p class="info-text">Masukkan PM10, PM2.5, SO2, CO, O3, dan NO2 sesuai data atau contoh simulasi.</p>
                </div>
                <div class="info-card">
                    <div class="info-number">4</div>
                    <div class="info-title">Tekan tombol proses</div>
                    <p class="info-text">Sistem akan memproses data menggunakan model klasifikasi kualitas udara.</p>
                </div>
                <div class="info-card">
                    <div class="info-number">5</div>
                    <div class="info-title">Baca hasil kategori</div>
                    <p class="info-text">Hasil utama berupa GOOD, MEDIUM, atau UNHEALTHY.</p>
                </div>
                <div class="info-card">
                    <div class="info-number">6</div>
                    <div class="info-title">Ikuti rekomendasi</div>
                    <p class="info-text">Rekomendasi mencakup aktivitas, masker, perlindungan diri, dan sunscreen jika relevan.</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def main():
    terapkan_css()
    tampilkan_topbar()
    tampilkan_hero()
    tampilkan_ringkasan()

    st.markdown('<div class="nav-wrap">', unsafe_allow_html=True)
    menu = st.radio(
        "Navigasi",
        ["Beranda", "Cek Kualitas Udara", "Cara Penggunaan"],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if menu == "Beranda":
        tampilkan_beranda()
    elif menu == "Cek Kualitas Udara":
        tampilkan_form_cek_udara()
    else:
        tampilkan_cara_penggunaan()


if __name__ == "__main__":
    main()