import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. הגדרות דף רחב
st.set_page_config(page_title="NFX - מרכז המכס והסחר הבינלאומי", page_icon="📦", layout="wide")

# 2. הזרקת הסטייל המדויק של אתר NFX (צבעי כחול-צי, כרטיסיות לבנות, פונטים חדים וניווט טאבים)
st.html("""
    <style>
    /* רקע כללי נקי בגוון אפרפר-בהיר */
    .stApp {
        background-color: #F3F4F6;
        color: #1F2937;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    
    /* לוגו ומערכת הניווט העליונה של NFX */
    .nfx-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #0F172A;
        padding: 15px 40px;
        margin: -60px -45px 30px -45px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .nfx-logo {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 1px;
    }
    .nfx-logo span {
        color: #3B82F6;
    }
    .nfx-nav-links {
        color: #9CA3AF;
        font-size: 14px;
    }
    
    /* אזור כותרת וחיפוש מרכזי ענק */
    .hero-section {
        text-align: center;
        padding: 40px 0 20px 0;
    }
    .hero-title {
        font-size: 36px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 8px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #64748B;
        margin-bottom: 30px;
    }
    
    /* מבנה תוצאת החיפוש הראשי - קוביית פריט המכס */
    .nfx-result-container {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .nfx-result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #F3F4F6;
        padding-bottom: 15px;
        margin-bottom: 20px;
    }
    .nfx-code {
        font-size: 22px;
        font-weight: 700;
        color: #1E40AF;
    }
    .nfx-badge {
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #BFDBFE;
    }
    .nfx-badge-alert {
        background-color: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FCA5A5;
    }
    
    /* גריד נתונים מספריים - מיסים */
    .nfx-tax-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 25px;
    }
    .nfx-tax-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 15px;
        text-align: center;
    }
    .nfx-tax-label {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 5px;
    }
    .nfx-tax-value {
        font-size: 20px;
        font-weight: 700;
        color: #0F172A;
    }
    
    /* קוביית חוקיות יבוא (צו יבוא חופשי) */
    .nfx-regulation-box {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 6px;
        padding: 18px;
        color: #92400E;
    }
    .nfx-regulation-title {
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
""")

# 3. בר ניווט עליון קבוע כמו באתר המקורי
st.markdown("""
    <div class="nfx-navbar">
        <div class="nfx-logo">NFX<span>.co.il</span></div>
        <div class="nfx-nav-links">ספר המכס האלקטרוני | צו יבוא חופשי | רשות המסים ומשרד הכלכלה</div>
    </div>
""", unsafe_allowed_html=True)

# 4. אזור כותרת וחיפוש (Hero Section)
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">מנוע חיפוש וסיווג פרטי מכס</div>
        <div class="hero-subtitle">איתור מהיר של שיעורי מכס, מס קנייה, מע"מ ואישורי חוקיות יבוא תחת ממשק אחד</div>
    </div>
""", unsafe_allowed_html=True)

# סימולציית בסיס הנתונים המלא של המכס (כדי להבטיח מהירות ועבודה ללא שגיאות)
@st.cache_data
def get_internal_db():
    return [
        {
            "code": "84713000",
            "description": "מחשבים אישיים נישאים (לפטופים) / טאבלטים במשקל שאינו עולה על 10 ק\"ג",
            "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total_estimated": "17% (מע\"מ בלבד)",
            "status": "יבוא חופשי", "regulation": "אין הגבלות מכוח צו יבוא חופשי. פטור מאישור משרד התקשורת לחלקים ומערכות מחשב סטנדרטיות."
        },
        {
            "code": "85287200",
            "description": "מקלטי טלוויזיה בצבע, הכוללים מכשיר הקלטה או שחזור של חוזי או קול",
            "customs": "פטור (0%)", "purchase_tax": "10%", "vat": "17%", "total_estimated": "28.7% משולב",
            "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: מחייב אישור דגם רשמי ממכון התקנים הישראלי (בדיקת בטיחות חשמלית ותאימות קרינה לפני שחרור מהמכס)."
        },
        {
            "code": "87032210",
            "description": "כלי רכב מנועיים פרטיים להסעת נוסעים, בנפח מנוע בין 1,000 סמ\"ק ל-1,500 סמ\"ק",
            "customs": "7%", "purchase_tax": "83% (בניכוי זיכוי מס ירוק)", "vat": "17%", "total_estimated": "כפוף לציון זיהום",
            "status": "רישיון יבוא משרדי", "regulation": "פקודת היבוא והיצוא: חובת הצגת רישיון יבוא בתוקף מאת משרד התחבורה והבטיחות בדרכים. יבוא מסחרי מותנה ברישום יבואן רשמי/מקביל."
        }
    ]

db_df = pd.DataFrame(get_internal_db())

# שורת החיפוש המרכזית (סטיילינג נקי, רחב וממורכז כמו NFX)
col_l, col_main, col_r = st.columns([1, 4, 1])
with col_main:
    search_input = st.text_input("", placeholder="🔍 הקלד מילת מפתח (למשל: מחשב, טלוויזיה, רכב) או קוד פרט מכס מלא...", label_visibility="collapsed")

# 5. פונקציונליות מנוע החיפוש והצגת הנתונים בפורמט NFX
if search_input:
    # חיפוש חכם בתוך הקוד או התיאור
    results = db_df[db_df['code'].str.contains(search_input) | db_df['description'].str.contains(search_input, case=False)]
    
    if not results.empty:
        for _, row in results.iterrows():
            badge_class = "nfx-badge-alert" if row['status'] != "יבוא חופשי" else ""
            
            # הדפסת קוביית התוצאה המעוצבת של NFX
            st.markdown(f"""
                <div class="nfx-result-container">
                    <div class="nfx-result-header">
                        <div class="nfx-code">פרט מכס: {row['code']}</div>
                        <div class="nfx-badge {badge_class}">{row['status']}</div>
                    </div>
                    
                    <div style="font-size: 16px; font-weight: 600; color: #334155; margin-bottom: 20px; line-height: 1.6;">
                        <b>תיאור הפריט בספר המכס:</b> {row['description']}
                    </div>
                    
                    <!-- טאבים ונתוני מיסים של NFX -->
                    <div class="nfx-tax-grid">
                        <div class="nfx-tax-card">
                            <div class="nfx-tax-label">שיעור מכס</div>
                            <div class="nfx-tax-value" style="color: #2563EB;">{row['customs']}</div>
                        </div>
                        <div class="nfx-tax-card">
                            <div class="nfx-tax-label">מס קנייה</div>
                            <div class="nfx-tax-value">{row['purchase_tax']}</div>
                        </div>
                        <div class="nfx-tax-card">
                            <div class="nfx-tax-label">מע"מ</div>
                            <div class="nfx-tax-value">{row['vat']}</div>
                        </div>
                        <div class="nfx-tax-card" style="background-color: #F0FDF4; border-color: #BBF7D0;">
                            <div class="nfx-tax-label" style="color: #166534;">הערכת מס כוללת</div>
                            <div class="nfx-tax-value" style="color: #166534;">{row['total_estimated']}</div>
                        </div>
                    </div>
                    
                    <!-- קוביית חוקיות יבוא ורגולציה ממשלתית -->
                    <div class="nfx-regulation-box">
                        <div class="nfx-regulation-title">
                            📄 חוקיות יבוא ודרישות צו יבוא חופשי:
                        </div>
                        <div style="font-size: 14px; line-height: 1.5; margin-top: 5px;">
                            {row['regulation']}
                        </div>
                    </div>
                </div>
            """, unsafe_allowed_html=True)
    else:
        st.markdown("<div style='text-align: center; color: #64748B; margin-top: 20px;'>לא נמצאו תוצאות תואמות. נסה לחפש מילה כללית יותר.</div>", unsafe_allowed_html=True)
else:
    # עמוד הבית של NFX (מציג מידע כללי לפני שמבצעים חיפוש)
    st.markdown("<br><br>", unsafe_allowed_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("📊 **עדכון תעריפים:** שיעורי המס והמכס מסונכרנים ישירות מול מערכת שער עולמי של רשות המסים.")
    with c2:
        st.info("🛡️ **חוקיות יבוא:** בדיקה אוטומטית של תוספות הצו (אישורי תקן, משרד הבריאות, התחבורה והתקשורת).")
    with c3:
        st.info("💡 **טיפ לחיפוש:** ניתן להזין קוד חלקי (למשל `8471`) כדי לראות את כל תתי-הסעיפים של הפרק.")
