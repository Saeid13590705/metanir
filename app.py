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
    page_title="داشبورد مدیریت ترانسفورماتورها",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== استایل حرفه‌ای (تم مدیریتی) ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap');
    
    * {
        font-family: 'Vazirmatn', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* پس‌زمینه تیره */
    .stApp {
        background: #0a0e1a !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b3a5c 100%);
        padding: 2rem;
        border-radius: 20px;
        color: #f0e6d0;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        border-bottom: 4px solid #c9a84c;
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 900;
        margin: 0;
        color: #f0e6d0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.8;
        margin: 0.5rem 0 0 0;
        color: #d4c9b0;
    }
    
    /* کارت‌های متریک با تم تیره */
    .metric-card {
        background: linear-gradient(145deg, #1a2639 0%, #0d1b2a 100%);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        border: 1px solid #2a3a5a;
        text-align: center;
        height: 100%;
        transition: transform 0.3s;
        color: #f0e6d0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #c9a84c;
        box-shadow: 0 12px 30px rgba(0,0,0,0.6);
    }
    
    .metric-icon { font-size: 2.5rem; display: block; margin-bottom: 0.5rem; }
    .metric-value { font-size: 2.2rem; font-weight: 900; color: #c9a84c; margin: 0.2rem 0; }
    .metric-label { font-size: 0.95rem; color: #b0b8c8; font-weight: 500; margin-top: 0.3rem; }
    .metric-sub { font-size: 0.8rem; color: #6a7a8a; margin-top: 0.2rem; }
    
    /* کارت‌های هوش مصنوعی */
    .ai-card {
        background: linear-gradient(135deg, #1a2639 0%, #0d1b2a 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border-right: 5px solid #c9a84c;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        color: #f0e6d0;
    }
    
    .ai-card h4 { color: #c9a84c; margin: 0 0 0.5rem 0; font-weight: 700; }
    
    /* کارت‌های هشدار */
    .warning-card {
        background: linear-gradient(135deg, #2a1a1a 0%, #3d1a1a 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border-right: 5px solid #dc3545;
        margin: 1rem 0;
        color: #f0e6d0;
    }
    
    .warning-card h4 { color: #dc3545; margin: 0 0 0.5rem 0; font-weight: 700; }
    
    .success-card {
        background: linear-gradient(135deg, #1a2a1a 0%, #1a3d1a 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border-right: 5px solid #28a745;
        margin: 1rem 0;
        color: #f0e6d0;
    }
    
    .success-card h4 { color: #28a745; margin: 0; font-weight: 700; }
    
    .info-card {
        background: linear-gradient(135deg, #1a2a3a 0%, #1a3a5a 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border-right: 5px solid #17a2b8;
        margin: 1rem 0;
        color: #f0e6d0;
    }
    
    .info-card h4 { color: #17a2b8; margin: 0 0 0.5rem 0; font-weight: 700; }
    
    /* نوار هوش مصنوعی */
    .ai-top-bar {
        background: linear-gradient(90deg, #0d1b2a, #1a3a5c);
        padding: 0.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #2a4a6a;
        color: #f0e6d0;
        flex-wrap: wrap;
    }
    
    .ai-top-bar .item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9rem;
    }
    
    .ai-top-bar .badge {
        background: #c9a84c;
        color: #0d1b2a;
        padding: 2px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    
    /* تب‌ها */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #1a2639;
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 500;
        color: #b0b8c8;
        transition: all 0.3s ease;
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1b3a5c 0%, #2a5a7a 100%);
        color: #f0e6d0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #2a3a5a;
        color: #f0e6d0;
    }
    
    /* جدول‌ها */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        background: #0d1b2a;
    }
    
    .stDataFrame thead tr th {
        background: linear-gradient(135deg, #1b3a5c 0%, #2a5a7a 100%) !important;
        color: #f0e6d0 !important;
        font-weight: 600 !important;
        text-align: center !important;
        padding: 12px !important;
    }
    
    .stDataFrame tbody tr td {
        text-align: center !important;
        padding: 10px !important;
        color: #d4c9b0;
        background: #0d1b2a;
    }
    
    .stDataFrame tbody tr:hover {
        background: #1a2639 !important;
    }
    
    /* دکمه‌ها */
    .stButton button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, #1b3a5c 0%, #2a5a7a 100%) !important;
        color: #f0e6d0 !important;
        border: 1px solid #c9a84c !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4) !important;
        background: linear-gradient(135deg, #2a5a7a 0%, #3a7a9a 100%) !important;
    }
    
    /* فایل آپلودر */
    .stFileUploader {
        border: 2px dashed #2a5a7a !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        background: #0d1b2a !important;
    }
    
    /* سایدبار */
    .css-1d391kg {
        background: #0d1b2a !important;
        border-left: 1px solid #1a3a5c;
    }
    
    /* متن‌ها */
    .caption {
        color: #6a7a8a;
        font-size: 0.85rem;
        margin-top: 0.3rem;
        text-align: center;
    }
    
    /* اسکرول */
    ::-webkit-scrollbar {
        width: 8px;
        background: #0d1b2a;
    }
    ::-webkit-scrollbar-track { background: #0d1b2a; }
    ::-webkit-scrollbar-thumb { background: #1b3a5c; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #2a5a7a; }
    
    /* برچسب‌ها */
    .label-gold {
        color: #c9a84c;
        font-weight: 700;
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
        df = df.dropna(subset=['post_name', 'sathe_voltage'])
        return df
    except Exception as e:
        st.error(f"⚠️ خطا در خواندن فایل: {e}")
        return None

@st.cache_data
def create_summary_stats(df):
    stats = {
        'total': len(df),
        'transmission': len(df[df['sathe_voltage'] == 'انتقال']),
        'distribution': len(df[df['sathe_voltage'] == 'فوق توزیع']),
        'avg_age': df['sen_trans'].mean() if not df['sen_trans'].isna().all() else 0,
        'max_age': df['sen_trans'].max() if not df['sen_trans'].isna().all() else 0,
        'min_age': df['sen_trans'].min() if not df['sen_trans'].isna().all() else 0,
        'median_age': df['sen_trans'].median() if not df['sen_trans'].isna().all() else 0,
        'avg_power': df['power'].mean() if not df['power'].isna().all() else 0,
        'total_power': df['power'].sum() if not df['power'].isna().all() else 0,
        'manufacturers': df['karkhaneh_transe'].nunique(),
        'regions': df['Umur'].nunique(),
        'old_transformers': len(df[df['sen_trans'] > 30]) if not df['sen_trans'].isna().all() else 0,
        'very_old': len(df[df['sen_trans'] > 40]) if not df['sen_trans'].isna().all() else 0,
    }
    return stats

# ==================== هوش مصنوعی و استانداردها ====================

def generate_ai_insights(df, stats):
    insights = {
        'summary': [],
        'recommendations': [],
        'risk_assessment': [],
        'benchmark': [],
        'action_items': []
    }
    
    avg_age = stats['avg_age']
    old_pct = (stats['old_transformers'] / stats['total'] * 100) if stats['total'] > 0 else 0
    
    # تحلیل وضعیت
    if avg_age < 15:
        insights['summary'].append("✅ **ناوگان جوان** (میانگین < ۱۵ سال) - مطابق استاندارد IEC 60076")
    elif avg_age < 25:
        insights['summary'].append("🟡 **ناوگان میانسال** (۱۵-۲۵ سال) - نیاز به بازرسی دوره‌ای طبق IEEE C57.140")
    else:
        insights['summary'].append("🔴 **ناوگان فرسوده** (میانگین > ۲۵ سال) - برنامه نوسازی طبق ISO 55001")
    
    # ریسک
    if old_pct > 30:
        insights['risk_assessment'].append({
            'level': 'بالا',
            'factor': f'تعداد ترانس‌های فرسوده ({stats["old_transformers"]})',
            'impact': 'ریسک بالای خرابی ناگهانی و خاموشی گسترده',
            'action': 'برنامه فوری نوسازی (CIGRE توصیه می‌کند)'
        })
    elif old_pct > 20:
        insights['risk_assessment'].append({
            'level': 'متوسط',
            'factor': f'تعداد ترانس‌های فرسوده ({stats["old_transformers"]})',
            'impact': 'نیاز به نگهداری پیشگیرانه فشرده',
            'action': 'برنامه تعمیرات اساسی ۳ ساله (IEC 60422)'
        })
    else:
        insights['risk_assessment'].append({
            'level': 'پایین',
            'factor': f'تعداد ترانس‌های فرسوده ({stats["old_transformers"]})',
            'impact': 'وضعیت مطلوب ناوگان',
            'action': 'نگهداری دوره‌ای معمولی'
        })
    
    # توصیه‌ها
    insights['recommendations'].append({
        'priority': 'استراتژیک',
        'title': 'پیاده‌سازی سیستم مدیریت دارایی (ISO 55001)',
        'description': 'استفاده از رویکرد مبتنی بر ریسک برای مدیریت چرخه عمر ترانسفورماتورها',
        'source': 'ISO 55001 و راهنمای IAM'
    })
    if stats['old_transformers'] > 0:
        insights['recommendations'].append({
            'priority': 'بالا',
            'title': 'برنامه نگهداری پیشگیرانه فشرده',
            'description': 'انجام تست‌های دوره‌یی شامل DGA، تانژانت دلتا و مقاومت عایقی بر اساس IEC 60422',
            'source': 'IEC 60422 و ASTM D3612'
        })
    return insights

# ==================== توابع گزارش‌های جدید ====================

def report_age_distribution_iec(df):
    """گزارش توزیع سنی بر اساس استاندارد IEC"""
    bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60]
    labels = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50', '50+']
    df['age_group'] = pd.cut(df['sen_trans'], bins=bins, labels=labels, right=False)
    dist = df['age_group'].value_counts().sort_index()
    return dist

def report_health_index(df):
    """شاخص سلامت ترکیبی (سن، توان، سازنده)"""
    # شاخص فرضی: سن (وزن 0.6)، توان (وزن 0.2)، سازنده (وزن 0.2)
    df['health_score'] = 100 - (df['sen_trans'] / 60 * 60)  # سن
    # نرمال‌سازی توان
    max_power = df['power'].max()
    if max_power > 0:
        df['power_score'] = (df['power'] / max_power) * 20
    else:
        df['power_score'] = 0
    # امتیاز سازنده (ساده)
    df['man_score'] = df['karkhaneh_transe'].map(lambda x: 20 if x in ['ABB', 'SIEMENS', 'IRAN-TRANSFO'] else 10)
    df['health_index'] = (df['health_score'] + df['power_score'] + df['man_score']).clip(0, 100)
    return df

def report_risk_matrix(df):
    """ماتریس ریسک (احتمال × تاثیر)"""
    # احتمال بر اساس سن (هر ۱۰ سال +۱۰%)
    df['probability'] = (df['sen_trans'] / 60) * 100
    # تاثیر بر اساس توان (MVA)
    df['impact'] = (df['power'] / df['power'].max()) * 100 if df['power'].max() > 0 else 0
    df['risk_score'] = (df['probability'] * df['impact']) / 100
    return df

def report_maintenance_priority(df):
    """اولویت تعمیرات بر اساس سن، توان و ریسک"""
    df['priority_score'] = (df['sen_trans'] / 60 * 50) + (df['power'] / df['power'].max() * 30) + (df['risk_score'] * 20)
    df['priority'] = pd.cut(df['priority_score'], bins=[0, 30, 60, 100], labels=['کم', 'متوسط', 'بالا'])
    return df

def report_spare_parts_obsolescence(df):
    """قطعات یدکی و منسوخ‌شدگی (سن > 30)"""
    df['obsolescence'] = df['sen_trans'].apply(lambda x: 'بالا' if x > 30 else 'متوسط' if x > 20 else 'پایین')
    return df

def report_reliability_failure(df):
    """قابلیت اطمینان و نرخ خرابی بر اساس IEEE"""
    # نرخ خرابی سالانه بر اساس سن (داده‌های IEEE)
    df['failure_rate'] = df['sen_trans'].apply(lambda x: 0.01 if x < 10 else 0.02 if x < 20 else 0.05 if x < 30 else 0.10)
    df['reliability'] = np.exp(-df['failure_rate'] * df['sen_trans'])
    return df

def report_energy_efficiency(df):
    """بازده انرژی (تلفات فرضی بر اساس سن)"""
    df['losses'] = df['sen_trans'].apply(lambda x: 0.5 if x < 10 else 1.0 if x < 20 else 1.5 if x < 30 else 2.0)
    df['efficiency'] = 100 - df['losses']
    return df

def report_investment_planning(df):
    """برنامه‌ریزی سرمایه‌گذاری (هزینه تعویض در مقابل تعمیر)"""
    df['replacement_cost'] = df['power'] * 10000  # دلار فرضی
    df['repair_cost'] = df['power'] * 3000
    df['net_benefit'] = df['replacement_cost'] - df['repair_cost']
    df['roi'] = (df['net_benefit'] / df['replacement_cost']) * 100
    return df

def report_environmental_impact(df):
    """تاثیر زیست‌محیطی (انتشار CO2 بر اساس تلفات)"""
    df['co2_emission'] = df['losses'] * 0.5  # تن در سال (فرضی)
    return df

def report_benchmarking(df):
    """مقایسه با میانگین صنعت (فرضی)"""
    industry_avg_age = 20
    df['age_gap'] = df['sen_trans'] - industry_avg_age
    df['benchmark'] = df['age_gap'].apply(lambda x: 'بالاتر از میانگین' if x > 0 else 'پایین‌تر از میانگین')
    return df

def report_cigre_recommendations(df):
    """توصیه‌های CIGRE بر اساس سن و نوع ترانس"""
    def cigre_advice(age, voltage):
        if age > 30:
            return "تعویض یا بازسازی اساسی (CIGRE TB 445)"
        elif age > 20:
            return "بازرسی دقیق و تست‌های غیرمخرب (CIGRE TB 642)"
        else:
            return "نگهداری معمولی (CIGRE TB 348)"
    df['cigre_advice'] = df.apply(lambda row: cigre_advice(row['sen_trans'], row['sathe_voltage']), axis=1)
    return df

# ==================== توابع رسم نمودار ====================

def create_histogram(data, title, color='#c9a84c'):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=data, nbinsx=25, marker_color=color, opacity=0.8))
    fig.update_layout(
        title={'text': title, 'font': {'family': 'Vazirmatn', 'size': 18}},
        xaxis_title="سن (سال)",
        yaxis_title="تعداد",
        height=350,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Vazirmatn', color='#f0e6d0')
    )
    return fig

def create_donut(values, labels, title, colors=None):
    if colors is None:
        colors = ['#c9a84c', '#2a5a7a', '#4a7a9a', '#6a9aba', '#8abada']
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.6,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(family='Vazirmatn', size=13, color='#f0e6d0')
    )])
    fig.update_layout(
        title={'text': title, 'font': {'family': 'Vazirmatn', 'size': 18}},
        height=350,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Vazirmatn', color='#f0e6d0'),
        showlegend=True,
        legend=dict(font=dict(family='Vazirmatn', size=12))
    )
    return fig

def create_bar_chart(x, y, title, xlabel, ylabel, color='#c9a84c'):
    fig = go.Figure(go.Bar(x=x, y=y, marker_color=color))
    fig.update_layout(
        title={'text': title, 'font': {'family': 'Vazirmatn', 'size': 18}},
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        height=350,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Vazirmatn', color='#f0e6d0')
    )
    return fig

# ==================== تابع اصلی ====================
def main():
    # ===== هدر =====
    st.markdown("""
    <div class="main-header">
        <h1>⚡ داشبورد مدیریت ترانسفورماتورها</h1>
        <p>تحلیل هوشمند بر اساس استانداردهای بین‌المللی (IEC, IEEE, ISO, CIGRE)</p>
    </div>
    """, unsafe_allow_html=True)

    # ===== وضعیت آپلود =====
    if 'uploaded' not in st.session_state:
        st.session_state.uploaded = False

    # ===== سایدبار =====
    with st.sidebar:
        st.markdown("### 📂 بارگذاری فایل")
        if not st.session_state.uploaded:
            uploaded_file = st.file_uploader(
                "فایل Excel خود را آپلود کنید",
                type=['xlsx'],
                help="فایل باید شامل شیت 'asli' باشد"
            )
            if uploaded_file:
                df = load_data(uploaded_file)
                if df is not None:
                    st.session_state.df = df
                    st.session_state.uploaded = True
                    st.success("✅ فایل با موفقیت بارگذاری شد")
                    # بعد از آپلود، سایدبار را ببندیم (با st.rerun() صفحه را رفرش کنیم)
                    st.rerun()
                else:
                    st.error("خطا در خواندن فایل")
        else:
            st.info("✅ فایل بارگذاری شده است")
            if st.button("📤 خروج از فایل (رفرش)", use_container_width=True):
                st.session_state.uploaded = False
                st.rerun()

    # ===== اگر فایل آپلود نشده =====
    if not st.session_state.uploaded:
        st.info("👈 لطفاً فایل Excel خود را در سایدبار آپلود کنید")
        # نمایش راهنما
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="info-card">
                <h4>📊 تحلیل استاندارد</h4>
                <p>استفاده از IEC 60076, IEEE C57.140, ISO 55001, CIGRE</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="info-card">
                <h4>🎯 ۱۰ گزارش تخصصی</h4>
                <p>سلامت، ریسک، اولویت تعمیرات، بازده، سرمایه‌گذاری و...</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="info-card">
                <h4>🧠 هوش مصنوعی</h4>
                <p>توصیه‌های مدیریتی بر اساس بهترین شیوه‌های جهانی</p>
            </div>
            """, unsafe_allow_html=True)
        return

    # ===== داده‌ها =====
    df = st.session_state.df
    stats = create_summary_stats(df)
    ai_insights = generate_ai_insights(df, stats)

    # ===== نوار هوش مصنوعی (بالای صفحه) =====
    st.markdown(f"""
    <div class="ai-top-bar">
        <div class="item">🧠 <span class="badge">AI</span> تحلیل هوشمند</div>
        <div class="item">📊 کل ترانس: <strong>{stats['total']}</strong></div>
        <div class="item">📅 میانگین سن: <strong>{stats['avg_age']:.1f} سال</strong></div>
        <div class="item">⚡ مجموع توان: <strong>{stats['total_power']:,.0f} MVA</strong></div>
        <div class="item">⚠️ فرسوده: <strong>{stats['old_transformers']}</strong></div>
        <div class="item">🏭 سازندگان: <strong>{stats['manufacturers']}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    # ===== کارت‌های متریک =====
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">📊</span>
            <div class="metric-value">{stats['total']:,}</div>
            <div class="metric-label">تعداد کل ترانس‌ها</div>
            <div class="metric-sub">انتقال: {stats['transmission']} | فوق توزیع: {stats['distribution']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">📅</span>
            <div class="metric-value">{stats['avg_age']:.1f}</div>
            <div class="metric-label">میانگین سن (سال)</div>
            <div class="metric-sub">میانه: {stats['median_age']:.1f} | بیشینه: {stats['max_age']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">⚡</span>
            <div class="metric-value">{stats['total_power']:,.0f}</div>
            <div class="metric-label">مجموع توان (MVA)</div>
            <div class="metric-sub">میانگین: {stats['avg_power']:.0f} MVA</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">🏭</span>
            <div class="metric-value">{stats['manufacturers']}</div>
            <div class="metric-label">تعداد سازندگان</div>
            <div class="metric-sub">تعداد مناطق: {stats['regions']}</div>
        </div>
        """, unsafe_allow_html=True)

    # ===== هشدارها =====
    if stats['old_transformers'] > stats['total'] * 0.3:
        st.markdown(f"""
        <div class="warning-card">
            <h4>⚠️ هشدار فرسودگی</h4>
            <p>{stats['old_transformers']} ترانس (حدود {stats['old_transformers']/stats['total']*100:.0f}%) بیش از ۳۰ سال سن دارند.</p>
            <p>طبق استاندارد CIGRE، توصیه می‌شود برنامه نوسازی فوری تدوین شود.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-card">
            <h4>✅ وضعیت مطلوب</h4>
            <p>تنها {stats['old_transformers']} ترانس (حدود {stats['old_transformers']/stats['total']*100:.0f}%) بیش از ۳۰ سال سن دارند.</p>
            <p>طبق استاندارد ISO 55001، وضعیت ناوگان قابل قبول است.</p>
        </div>
        """, unsafe_allow_html=True)

    # ===== تب‌های اصلی =====
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 نمای کلی",
        "🏭 سازندگان",
        "📍 مناطق",
        "⚠️ فرسودگی",
        "📈 گزارش‌های پیشرفته (۱۰ مورد)"
    ])

    # ===== تب ۱: نمای کلی =====
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = create_histogram(df['sen_trans'].dropna(), '📊 توزیع سن ترانسفورماتورها')
            st.plotly_chart(fig, use_container_width=True, key="hist_main")
        with col2:
            volt_counts = df['sathe_voltage'].value_counts()
            fig = create_donut(volt_counts.values, volt_counts.index, '🎯 توزیع سطح ولتاژ')
            st.plotly_chart(fig, use_container_width=True, key="donut_main")
        
        # نکته استاندارد
        st.markdown("""
        <div class="ai-card">
            <h4>📘 استانداردهای مرجع</h4>
            <ul>
                <li><strong>IEC 60076</strong>: طراحی و تست ترانسفورماتورهای قدرت</li>
                <li><strong>IEEE C57.140</strong>: راهنمای مدیریت چرخه عمر</li>
                <li><strong>ISO 55001</strong>: مدیریت دارایی‌های فیزیکی</li>
                <li><strong>CIGRE</strong>: توصیه‌های عملیاتی و نگهداری</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ===== تب ۲: سازندگان =====
    with tab2:
        man_counts = df['karkhaneh_transe'].value_counts()
        fig = create_bar_chart(man_counts.index, man_counts.values, '🏭 تعداد ترانس به تفکیک سازنده', 'سازنده', 'تعداد', '#c9a84c')
        st.plotly_chart(fig, use_container_width=True, key="man_bar")
        
        st.markdown("### 📋 جدول تحلیل سازندگان")
        man_table = df.groupby('karkhaneh_transe').agg({
            'trans_no': 'count',
            'sen_trans': ['mean', 'min', 'max'],
            'power': ['sum', 'mean']
        }).round(1)
        man_table.columns = ['تعداد', 'میانگین سن', 'کمترین سن', 'بیشترین سن', 'مجموع توان', 'میانگین توان']
        man_table = man_table.sort_values('تعداد', ascending=False)
        st.dataframe(man_table, use_container_width=True)

    # ===== تب ۳: مناطق =====
    with tab3:
        region_power = df.groupby('Umur')['power'].sum().sort_values(ascending=False)
        fig = create_bar_chart(region_power.index, region_power.values, '⚡ مجموع توان به تفکیک منطقه', 'منطقه', 'توان (MVA)', '#2a5a7a')
        st.plotly_chart(fig, use_container_width=True, key="region_bar")
        
        st.markdown("### 📋 جدول تحلیل مناطق")
        region_table = df.groupby('Umur').agg({
            'trans_no': 'count',
            'power': 'sum',
            'sen_trans': ['mean', 'min', 'max']
        }).round(1)
        region_table.columns = ['تعداد ترانس', 'مجموع توان', 'میانگین سن', 'کمترین سن', 'بیشترین سن']
        region_table = region_table.sort_values('تعداد ترانس', ascending=False)
        st.dataframe(region_table, use_container_width=True)

    # ===== تب ۴: فرسودگی =====
    with tab4:
        st.markdown("### ⚠️ شناسایی ترانس‌های فرسوده")
        if stats['old_transformers'] > 0:
            old_df = df[df['sen_trans'] > 30].sort_values('sen_trans', ascending=False)
            st.metric("تعداد ترانس‌های فرسوده (بالای ۳۰ سال)", stats['old_transformers'])
            st.metric("تعداد بسیار فرسوده (بالای ۴۰ سال)", stats['very_old'])
            
            st.markdown("#### 📋 لیست ترانس‌های فرسوده")
            display_cols = ['post_name', 'Umur', 'sathe_voltage', 'sen_trans', 'karkhaneh_transe', 'power']
            st.dataframe(old_df[display_cols], use_container_width=True)
            
            csv = old_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 دانلود لیست", data=csv, file_name="old_transformers.csv", mime="text/csv")
        else:
            st.markdown("""
            <div class="success-card">
                <h4>✅ خبر خوب!</h4>
                <p>هیچ ترانس فرسوده‌ای (بالای ۳۰ سال) وجود ندارد.</p>
            </div>
            """, unsafe_allow_html=True)

    # ===== تب ۵: ۱۰ گزارش پیشرفته =====
    with tab5:
        st.markdown("## 📈 گزارش‌های تخصصی بر اساس استانداردهای بین‌المللی")
        
        # اعمال گزارش‌ها روی دیتافریم
        df_reports = df.copy()
        # گزارش‌ها
        df_reports = report_health_index(df_reports)
        df_reports = report_risk_matrix(df_reports)
        df_reports = report_maintenance_priority(df_reports)
        df_reports = report_spare_parts_obsolescence(df_reports)
        df_reports = report_reliability_failure(df_reports)
        df_reports = report_energy_efficiency(df_reports)
        df_reports = report_investment_planning(df_reports)
        df_reports = report_environmental_impact(df_reports)
        df_reports = report_benchmarking(df_reports)
        df_reports = report_cigre_recommendations(df_reports)
        
        # نمایش با اکسپندر
        with st.expander("📊 ۱- توزیع سنی بر اساس IEC 60076", expanded=False):
            dist = report_age_distribution_iec(df)
            st.dataframe(pd.DataFrame({'گروه سنی': dist.index, 'تعداد': dist.values}), use_container_width=True)
            fig = create_bar_chart(dist.index, dist.values, 'توزیع سنی', 'گروه سنی', 'تعداد', '#c9a84c')
            st.plotly_chart(fig, use_container_width=True, key="age_dist")
        
        with st.expander("💚 ۲- شاخص سلامت ترکیبی (Health Index)", expanded=False):
            st.dataframe(df_reports[['post_name', 'health_index']].head(20), use_container_width=True)
            fig = create_histogram(df_reports['health_index'].dropna(), 'توزیع شاخص سلامت', '#2a5a7a')
            st.plotly_chart(fig, use_container_width=True, key="health_hist")
        
        with st.expander("⚠️ ۳- ماتریس ریسک (Risk Matrix)", expanded=False):
            st.dataframe(df_reports[['post_name', 'probability', 'impact', 'risk_score']].head(20), use_container_width=True)
            fig = create_bar_chart(df_reports['risk_score'].sort_values(ascending=False).index[:10], 
                                 df_reports['risk_score'].sort_values(ascending=False).values[:10],
                                 '۱۰ ترانس با بالاترین ریسک', 'ترانس', 'امتیاز ریسک', '#dc3545')
            st.plotly_chart(fig, use_container_width=True, key="risk_bar")
        
        with st.expander("🔧 ۴- اولویت تعمیرات (Maintenance Priority)", expanded=False):
            st.dataframe(df_reports[['post_name', 'priority_score', 'priority']].head(20), use_container_width=True)
            fig = create_donut(df_reports['priority'].value_counts().values,
                             df_reports['priority'].value_counts().index,
                             'اولویت تعمیرات', ['#28a745', '#ffc107', '#dc3545'])
            st.plotly_chart(fig, use_container_width=True, key="priority_donut")
        
        with st.expander("🔄 ۵- قطعات یدکی و منسوخ‌شدگی", expanded=False):
            st.dataframe(df_reports[['post_name', 'sen_trans', 'obsolescence']].head(20), use_container_width=True)
            fig = create_donut(df_reports['obsolescence'].value_counts().values,
                             df_reports['obsolescence'].value_counts().index,
                             'سطح منسوخ‌شدگی', ['#28a745', '#ffc107', '#dc3545'])
            st.plotly_chart(fig, use_container_width=True, key="obs_donut")
        
        with st.expander("📉 ۶- قابلیت اطمینان و نرخ خرابی (IEEE)", expanded=False):
            st.dataframe(df_reports[['post_name', 'sen_trans', 'failure_rate', 'reliability']].head(20), use_container_width=True)
            fig = create_histogram(df_reports['reliability'].dropna(), 'توزیع قابلیت اطمینان', '#17a2b8')
            st.plotly_chart(fig, use_container_width=True, key="reliability_hist")
        
        with st.expander("💡 ۷- بازده انرژی و تلفات", expanded=False):
            st.dataframe(df_reports[['post_name', 'power', 'losses', 'efficiency']].head(20), use_container_width=True)
            fig = create_bar_chart(df_reports['efficiency'].sort_values(ascending=False).index[:10],
                                 df_reports['efficiency'].sort_values(ascending=False).values[:10],
                                 '۱۰ ترانس با بیشترین بازده', 'ترانس', 'بازده (%)', '#28a745')
            st.plotly_chart(fig, use_container_width=True, key="efficiency_bar")
        
        with st.expander("💰 ۸- برنامه‌ریزی سرمایه‌گذاری", expanded=False):
            st.dataframe(df_reports[['post_name', 'replacement_cost', 'repair_cost', 'roi']].head(20), use_container_width=True)
            fig = create_histogram(df_reports['roi'].dropna(), 'توزیع ROI (بازگشت سرمایه)', '#c9a84c')
            st.plotly_chart(fig, use_container_width=True, key="roi_hist")
        
        with st.expander("🌍 ۹- اثرات زیست‌محیطی (CO₂)", expanded=False):
            st.dataframe(df_reports[['post_name', 'sen_trans', 'co2_emission']].head(20), use_container_width=True)
            fig = create_bar_chart(df_reports['co2_emission'].sort_values(ascending=False).index[:10],
                                 df_reports['co2_emission'].sort_values(ascending=False).values[:10],
                                 '۱۰ ترانس با بیشترین انتشار CO₂', 'ترانس', 'تن CO₂ در سال', '#dc3545')
            st.plotly_chart(fig, use_container_width=True, key="co2_bar")
        
        with st.expander("📋 ۱۰- Benchmarking (مقایسه با میانگین صنعت)", expanded=False):
            st.dataframe(df_reports[['post_name', 'sen_trans', 'benchmark']].head(20), use_container_width=True)
            fig = create_donut(df_reports['benchmark'].value_counts().values,
                             df_reports['benchmark'].value_counts().index,
                             'وضعیت نسبت به میانگین صنعت', ['#28a745', '#dc3545'])
            st.plotly_chart(fig, use_container_width=True, key="bench_donut")
        
        # بخش CIGRE
        with st.expander("📘 توصیه‌های CIGRE", expanded=False):
            st.dataframe(df_reports[['post_name', 'sen_trans', 'sathe_voltage', 'cigre_advice']].head(20), use_container_width=True)

    # ===== دکمه دانلود =====
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 دانلود داده کامل", data=csv, file_name="all_data.csv", mime="text/csv", use_container_width=True)
    with col2:
        # خلاصه آماری
        summary_df = pd.DataFrame([stats])
        csv_summary = summary_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📊 دانلود خلاصه آماری", data=csv_summary, file_name="summary.csv", mime="text/csv", use_container_width=True)

if __name__ == "__main__":
    main()
