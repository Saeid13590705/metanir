import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ==================== تنظیمات صفحه ====================
st.set_page_config(
    page_title="داشبورد ترانسفورماتورها",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== استایل حرفه‌ای - طراحی مدرن ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap');
    
    * {
        font-family: 'Vazirmatn', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
    }
    
    /* ===== هدر اصلی ===== */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border-bottom: 5px solid #00d4ff;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        color: #ffffff;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0.8rem 0 0 0;
        color: #e8f4f8;
    }
    
    /* ===== کارت‌های معیار (Metric Cards) ===== */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 2px solid #e9ecef;
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
        color: #2c3e50;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.12);
        border-color: #00d4ff;
        background: linear-gradient(145deg, #ffffff 0%, #e8f4ff 100%);
    }
    
    .metric-icon { 
        font-size: 2.8rem; 
        display: block; 
        margin-bottom: 0.8rem; 
    }
    
    .metric-value { 
        font-size: 2.5rem; 
        font-weight: 900; 
        color: #1e3c72; 
        margin: 0.5rem 0; 
        line-height: 1.1;
    }
    
    .metric-label { 
        font-size: 0.95rem; 
        color: #5a6c7d; 
        font-weight: 600; 
        margin-top: 0.5rem; 
    }
    
    .metric-sub { 
        font-size: 0.85rem; 
        color: #8b9aad; 
        margin-top: 0.4rem; 
    }
    
    /* ===== کارت‌های اطلاعات و هشدار ===== */
    .ai-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-right: 5px solid #00d4ff;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        color: #1a237e;
    }
    
    .ai-card h4 { 
        color: #1e3c72; 
        margin: 0 0 0.8rem 0; 
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .ai-card ul { 
        margin: 0.5rem 0; 
        padding-right: 1.5rem;
    }
    
    .ai-card li { 
        margin: 0.5rem 0; 
        line-height: 1.6;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #ffebee 0%, #fff3e0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-right: 5px solid #e74c3c;
        margin: 1rem 0;
        color: #c0392b;
    }
    
    .warning-card h4 { 
        color: #e74c3c; 
        margin: 0 0 0.8rem 0; 
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .success-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-right: 5px solid #27ae60;
        margin: 1rem 0;
        color: #1b5e20;
    }
    
    .success-card h4 { 
        color: #27ae60; 
        margin: 0 0 0.8rem 0; 
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .info-card {
        background: linear-gradient(135deg, #e0f2f1 0%, #eceff1 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-right: 5px solid #00bcd4;
        margin: 1rem 0;
        color: #004d40;
    }
    
    .info-card h4 { 
        color: #00796b; 
        margin: 0 0 0.8rem 0; 
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    /* ===== نوار بالای داشبورد ===== */
    .dashboard-bar {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: #ffffff;
    }
    
    .dashboard-bar .item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    }
    
    .dashboard-bar .badge {
        background: #00d4ff;
        color: #1e3c72;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    
    /* ===== تب‌ها ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f0f2f5;
        border-radius: 12px;
        padding: 6px;
        border-bottom: 2px solid #e9ecef;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 600;
        color: #5a6c7d;
        transition: all 0.3s ease;
        background: transparent;
        font-size: 0.95rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(30, 60, 114, 0.2);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e3f2fd;
        color: #1e3c72;
    }
    
    /* ===== جدول‌ها ===== */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        background: #ffffff;
    }
    
    .stDataFrame thead tr th {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        text-align: center !important;
        padding: 14px !important;
    }
    
    .stDataFrame tbody tr td {
        text-align: center !important;
        padding: 10px !important;
        color: #2c3e50;
        background: #ffffff;
        border-bottom: 1px solid #eceff1;
    }
    
    .stDataFrame tbody tr:hover {
        background: #f5f7fa !important;
    }
    
    /* ===== دکمه‌ها ===== */
    .stButton button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        color: #ffffff !important;
        border: 2px solid #00d4ff !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
        background: linear-gradient(135deg, #2a5298 0%, #3a6db8 100%) !important;
    }
    
    /* ===== فیلد جستجو ===== */
    .stTextInput input {
        border-radius: 10px !important;
        border: 2px solid #e9ecef !important;
        padding: 0.8rem !important;
        background: #ffffff !important;
        color: #2c3e50 !important;
        font-family: 'Vazirmatn', sans-serif !important;
    }
    
    .stTextInput input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.1) !important;
    }
    
    /* ===== سایدبار ===== */
    .css-1d391kg {
        background: linear-gradient(180deg, #f5f7fa 0%, #e9ecef 100%) !important;
        border-left: 3px solid #00d4ff;
    }
    
    /* ===== اسکرول‌بار ===== */
    ::-webkit-scrollbar {
        width: 8px;
        background: #f0f2f5;
    }
    
    ::-webkit-scrollbar-track { 
        background: #f0f2f5; 
    }
    
    ::-webkit-scrollbar-thumb { 
        background: #00d4ff; 
        border-radius: 4px; 
    }
    
    ::-webkit-scrollbar-thumb:hover { 
        background: #1e3c72; 
    }
    
    /* ===== بعنوان ===== */
    h1, h2, h3, h4, h5, h6 {
        color: #1e3c72 !important;
    }
    
    /* ===== توضیحات ===== */
    .caption {
        color: #8b9aad;
        font-size: 0.85rem;
        margin-top: 0.5rem;
        text-align: center;
    }
    
    /* ===== Responsive برای موبایل ===== */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .main-header {
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .metric-value {
            font-size: 1.8rem;
        }
        
        .metric-icon {
            font-size: 2rem;
        }
        
        .dashboard-bar {
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .dashboard-bar .item {
            font-size: 0.85rem;
            width: 100%;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px;
            font-size: 0.85rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== توابع کمکی ====================

@st.cache_data
def load_data(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, sheet_name='asli')
        numeric_cols = ['power', 'sen_trans', 'sen_tap_changer']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=['post_name'])
        return df
    except Exception as e:
        st.error(f"⚠️ خطا: {e}")
        return None

@st.cache_data
def create_summary_stats(df):
    stats = {
        'total': len(df),
        'avg_age': df['sen_trans'].mean() if not df['sen_trans'].isna().all() else 0,
        'max_age': df['sen_trans'].max() if not df['sen_trans'].isna().all() else 0,
        'min_age': df['sen_trans'].min() if not df['sen_trans'].isna().all() else 0,
        'median_age': df['sen_trans'].median() if not df['sen_trans'].isna().all() else 0,
        'avg_power': df['power'].mean() if not df['power'].isna().all() else 0,
        'total_power': df['power'].sum() if not df['power'].isna().all() else 0,
        'manufacturers': df['karkhaneh_transe'].nunique(),
        'regions': df['Umur'].nunique(),
        'old_transformers': len(df[df['sen_trans'] > 30]) if not df['sen_trans'].isna().all() else 0,
        'critical_transformers': len(df[df['sen_trans'] > 40]) if not df['sen_trans'].isna().all() else 0,
        'young_transformers': len(df[df['sen_trans'] < 10]) if not df['sen_trans'].isna().all() else 0,
    }
    return stats

# ==================== توابع گزارش ====================

def generate_health_index(df):
    df_temp = df.copy()
    # سن (60%): سن قدیمی‌تر = امتیاز پایین‌تر
    age_score = 100 - (df_temp['sen_trans'] / 60 * 100)
    
    # توان (25%): توان بیش‌تر = اهمیت بیش‌تر
    power_score = (df_temp['power'] / df_temp['power'].max() * 100) if df_temp['power'].max() > 0 else 0
    
    # سن تاب چنجر (15%)
    tap_score = 100 - (df_temp['sen_tap_changer'] / df_temp['sen_tap_changer'].max() * 100)
    
    df_temp['health_index'] = (age_score * 0.6 + power_score * 0.25 + tap_score * 0.15).clip(0, 100)
    return df_temp

def generate_risk_score(df):
    df_temp = df.copy()
    # احتمال خرابی = سن
    probability = (df_temp['sen_trans'] / 60) * 100
    
    # تأثیر = توان
    impact = (df_temp['power'] / df_temp['power'].max() * 100) if df_temp['power'].max() > 0 else 0
    
    df_temp['risk_score'] = (probability * 0.6 + impact * 0.4).clip(0, 100)
    df_temp['risk_level'] = pd.cut(
        df_temp['risk_score'], 
        bins=[0, 30, 60, 100], 
        labels=['پایین', 'متوسط', 'بالا']
    )
    return df_temp

# ==================== توابع نمودار ====================

def create_modern_histogram(data, title, color='#00d4ff'):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=data, nbinsx=20, marker_color=color, opacity=0.8))
    fig.update_layout(
        title=dict(text=title, font=dict(family='Vazirmatn', size=14, color='#1e3c72')),
        xaxis_title="مقدار",
        yaxis_title="تعداد",
        height=350,
        template='plotly_white',
        font=dict(family='Vazirmatn', color='#2c3e50'),
        hovermode='x unified',
        showlegend=False
    )
    return fig

def create_modern_donut(values, labels, title, colors=None):
    if colors is None:
        colors = ['#00d4ff', '#1e3c72', '#2a5298', '#00b4d8', '#90e0ef']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.5,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(family='Vazirmatn', size=11, color='#ffffff'),
        hoverinfo='label+value+percent'
    )])
    fig.update_layout(
        title=dict(text=title, font=dict(family='Vazirmatn', size=14, color='#1e3c72')),
        height=350,
        template='plotly_white',
        font=dict(family='Vazirmatn', color='#2c3e50')
    )
    return fig

def create_modern_bar(x, y, title, xlabel, ylabel, color='#00d4ff'):
    fig = go.Figure(go.Bar(
        x=x, y=y, 
        marker=dict(color=color),
        hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family='Vazirmatn', size=14, color='#1e3c72')),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        height=350,
        template='plotly_white',
        font=dict(family='Vazirmatn', color='#2c3e50'),
        hovermode='x unified',
        showlegend=False
    )
    return fig

# ==================== تابع اصلی ====================

def main():
    # هدر
    st.markdown("""
    <div class="main-header">
        <h1>⚡ داشبورد مدیریت ترانسفورماتورها</h1>
        <p>تحلیل هوشمند و گزارشگری برای تصمیم‌گیری مدیریتی</p>
    </div>
    """, unsafe_allow_html=True)

    # وضعیت سشن
    if 'uploaded' not in st.session_state:
        st.session_state.uploaded = False

    # سایدبار
    with st.sidebar:
        st.markdown("### 📂 مدیریت فایل")
        if not st.session_state.uploaded:
            uploaded_file = st.file_uploader(
                "فایل Excel را انتخاب کنید",
                type=['xlsx'],
                help="فایل شامل شیت 'asli' باشد"
            )
            if uploaded_file:
                df = load_data(uploaded_file)
                if df is not None:
                    st.session_state.df = df
                    st.session_state.uploaded = True
                    st.success("✅ بارگذاری موفق!")
                    st.rerun()
        else:
            st.info("✅ فایل فعال است")
            if st.button("🔄 تغییر فایل", use_container_width=True):
                st.session_state.uploaded = False
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 اطلاعات سیستم")
        st.markdown(f"**نسخه**: 2.0 Premium")
        st.markdown(f"**تاریخ**: {datetime.now().strftime('%Y-%m-%d')}")

    if not st.session_state.uploaded:
        # صفحه خوش‌آمدگویی
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="info-card">
                <h4>📊 تحلیل دقیق</h4>
                <p>ارزیابی جامع وضعیت ناوگان بر اساس معیارهای استاندارد</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="info-card">
                <h4>🎯 گزارشات عملیاتی</h4>
                <p>گزارش‌های تخصصی برای تصمیم‌گیری مدیریتی</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="info-card">
                <h4>📱 واسط دوستانه</h4>
                <p>طراحی بهینه برای دسکتاپ، تبلت و موبایل</p>
            </div>
            """, unsafe_allow_html=True)
        return

    df = st.session_state.df
    stats = create_summary_stats(df)

    # نوار اطلاعات
    st.markdown(f"""
    <div class="dashboard-bar">
        <div class="item">📊 کل: <strong>{stats['total']}</strong></div>
        <div class="item">📅 میانگین سن: <strong>{stats['avg_age']:.1f}yr</strong></div>
        <div class="item">⚡ مجموع توان: <strong>{stats['total_power']:,.0f}MVA</strong></div>
        <div class="item">🏭 سازندگان: <strong>{stats['manufacturers']}</strong></div>
        <div class="item">⚠️ فرسوده: <div class="badge">{stats['old_transformers']}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # کارت‌های معیار
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">📊</span>
            <div class="metric-value">{stats['total']:,}</div>
            <div class="metric-label">تعداد کل</div>
            <div class="metric-sub">{stats['regions']} منطقه</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">📅</span>
            <div class="metric-value">{stats['avg_age']:.0f}</div>
            <div class="metric-label">میانگین سن (سال)</div>
            <div class="metric-sub">میانه: {stats['median_age']:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">⚡</span>
            <div class="metric-value">{stats['total_power']:,.0f}</div>
            <div class="metric-label">مجموع توان (MVA)</div>
            <div class="metric-sub">میانگین: {stats['avg_power']:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        pct_old = (stats['old_transformers'] / stats['total'] * 100) if stats['total'] > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">⚠️</span>
            <div class="metric-value">{pct_old:.0f}%</div>
            <div class="metric-label">درصد فرسوده</div>
            <div class="metric-sub">{stats['old_transformers']} ترانس</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # هشدار و پیام
    if stats['old_transformers'] > stats['total'] * 0.25:
        st.markdown(f"""
        <div class="warning-card">
            <h4>⚠️ هشدار: ناوگان فرسوده</h4>
            <p><strong>{stats['old_transformers']}</strong> ترانس ({pct_old:.1f}%) بیش از 30 سال سن دارند.</p>
            <p>بر اساس CIGRE و ISO، برنامه نوسازی فوری توصیه می‌شود.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-card">
            <h4>✅ وضعیت مطلوب</h4>
            <p>وضعیت کلی ناوگان قابل قبول است ({pct_old:.1f}% فرسوده)</p>
        </div>
        """, unsafe_allow_html=True)

    # جستجو
    st.markdown("### 🔍 جستجو سریع")
    search_term = st.text_input(
        "",
        placeholder="جستجو: نام پست، منطقه، سازنده...",
        key="search"
    )
    
    if search_term:
        mask = pd.Series(False, index=df.index)
        for col in ['post_name', 'Umur', 'karkhaneh_transe']:
            if col in df.columns:
                mask = mask | df[col].astype(str).str.contains(search_term, na=False)
        
        if mask.any():
            st.success(f"✅ {mask.sum()} نتیجه")
            st.dataframe(
                df[mask][['post_name', 'Umur', 'power', 'sen_trans', 'karkhaneh_transe']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("⚠️ نتیجه‌ای یافت نشد")
    
    st.markdown("---")

    # تب‌های اصلی
    tabs = st.tabs([
        "📊 نمای کلی",
        "🏭 تحلیل سازندگان",
        "📍 توزیع جغرافیایی",
        "⚠️ تحلیل ریسک",
        "📋 جدول جامع"
    ])

    # تب 1: نمای کلی
    with tabs[0]:
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            fig = create_modern_histogram(df['sen_trans'].dropna(), '📊 توزیع سن ترانسفورماتورها')
            st.plotly_chart(fig, use_container_width=True, key="age_hist")
        
        with col2:
            age_groups = pd.cut(df['sen_trans'], bins=[0, 10, 20, 30, 100], 
                                labels=['<10 سال', '10-20 سال', '20-30 سال', '>30 سال'])
            fig = create_modern_donut(
                age_groups.value_counts().values,
                age_groups.value_counts().index,
                '🎯 گروه‌های سنی'
            )
            st.plotly_chart(fig, use_container_width=True, key="age_donut")
    
    # تب 2: سازندگان
    with tabs[1]:
        man_counts = df['karkhaneh_transe'].value_counts().head(10)
        fig = create_modern_bar(
            man_counts.index, man_counts.values,
            '🏭 10 سازنده برتر',
            'سازنده', 'تعداد', '#00d4ff'
        )
        st.plotly_chart(fig, use_container_width=True, key="man_bar")
        
        st.markdown("### 📋 آمار سازندگان")
        man_stats = df.groupby('karkhaneh_transe').agg({
            'trans_no': 'count',
            'power': 'sum',
            'sen_trans': 'mean'
        }).round(1).sort_values('trans_no', ascending=False)
        man_stats.columns = ['تعداد', 'توان کل', 'میانگین سن']
        st.dataframe(man_stats, use_container_width=True)
    
    # تب 3: توزیع جغرافیایی
    with tabs[2]:
        region_power = df.groupby('Umur')['power'].sum().sort_values(ascending=False).head(10)
        fig = create_modern_bar(
            region_power.index, region_power.values,
            '⚡ توان در مناطق برتر',
            'منطقه', 'توان (MVA)', '#2a5298'
        )
        st.plotly_chart(fig, use_container_width=True, key="region_bar")
        
        st.markdown("### 📋 آمار مناطق")
        region_stats = df.groupby('Umur').agg({
            'trans_no': 'count',
            'power': 'sum',
            'sen_trans': 'mean'
        }).round(1).sort_values('power', ascending=False)
        region_stats.columns = ['تعداد', 'توان کل', 'میانگین سن']
        st.dataframe(region_stats, use_container_width=True)
    
    # تب 4: تحلیل ریسک
    with tabs[3]:
        df_risk = generate_risk_score(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            risk_counts = df_risk['risk_level'].value_counts()
            colors = {'پایین': '#27ae60', 'متوسط': '#f39c12', 'بالا': '#e74c3c'}
            color_map = [colors[x] for x in risk_counts.index]
            fig = create_modern_donut(
                risk_counts.values,
                risk_counts.index,
                '⚠️ سطح ریسک',
                color_map
            )
            st.plotly_chart(fig, use_container_width=True, key="risk_donut")
        
        with col2:
            high_risk = df_risk[df_risk['risk_level'] == 'بالا'].sort_values('risk_score', ascending=False).head(10)
            if len(high_risk) > 0:
                fig = create_modern_bar(
                    high_risk['post_name'],
                    high_risk['risk_score'],
                    '🔴 10 ترانس با بالاترین ریسک',
                    'ترانس', 'امتیاز ریسک', '#e74c3c'
                )
                st.plotly_chart(fig, use_container_width=True, key="risk_bar")
        
        # جدول ریسک
        st.markdown("### 📋 جدول تفصیلی ریسک")
        st.dataframe(
            df_risk[['post_name', 'Umur', 'sen_trans', 'power', 'risk_score', 'risk_level']]
            .sort_values('risk_score', ascending=False)
            .head(20),
            use_container_width=True,
            hide_index=True
        )
    
    # تب 5: جدول جامع
    with tabs[4]:
        df_display = df[['post_name', 'Umur', 'power', 'sen_trans', 'karkhaneh_transe', 
                         'sathe_voltage', 'sen_tap_changer']].copy()
        df_display = df_display.sort_values('sen_trans', ascending=False)
        
        st.markdown("### 📊 لیست کامل ترانسفورماتورها")
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # دانلود
        csv = df_display.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            "📥 دانلود فایل اکسل",
            data=csv,
            file_name=f"transformers_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

if __name__ == "__main__":
    main()
