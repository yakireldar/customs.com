import streamlit as st
import pandas as pd
from datetime import datetime

# 1. הגדרות דף רחב
st.set_page_config(page_title="NFX - מרכז המכס והסחר הבינלאומי", page_icon="📦", layout="wide")

# 2. הזרקת הסטייל המדויק של אתר NFX באמצעות st.html הבטוח
st.html("""
    <style>
    .stApp {
        background-color: #F3F4F6;
        color: #1F2937;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
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
    .hero-section {
        text-align: center;
        padding: 20px 0 10px 0;
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
        margin-bottom: 25px;
    }
    .nfx-result-container {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 25px;
        margin-bottom: 20px;
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

# 3. בר ניווט עליון
st.html("""
    <div class="nfx-navbar">
        <div class="nfx-logo">NFX<span>.co.il</span></div>
        <div class="nfx-nav-links">ספר המכס האלקטרוני | צו יבוא חופשי | רשות המסים ומשרד הכלכלה</div>
    </div>
""")

# 4. אזור כותרת מרכזית
st.html("""
    <div class="hero-section">
        <div class="hero-title">מנוע חיפוש וסיווג פרטי מכס</div>
        <div class="hero-subtitle">איתור מהיר של שיעורי מכס, מס קנייה, מע"מ ואישורי חוקיות יבוא תחת ממשק אחד</div>
    </div>
""")

# בסיס נתונים לדוגמה
@st.cache_data
def get_expanded_db():
    return [
        {
            "code": "84713000", "chapter": "פרק 84 - מכשירים מכניים, מחשבים ואלקטרוניקה",
            "description": "מחשבים אישיים נישאים (לפטופים) / טאבלטים במשקל שאינו עולה על 10 ק\"ג",
            "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total_estimated": "17% (מע\"מ בלבד)",
            "status": "יבוא חופשי", "regulation": "אין הגבלות מכוח צו יבוא חופשי. פטור מאישור משרד התקשורת לחלקים ומערכות מחשב סטנדרטיות."
        },
        {
            "code": "85287200", "chapter": "פרק 85 - מכשירים חשמליים, טלוויזיות וציוד שמע",
            "description": "מקלטי טלוויזיה בצבע, הכוללים מכשיר הקלטה או שחזור של חוזי או קול",
            "customs": "פטור (0%)", "purchase_tax": "10%", "vat": "17%", "total_estimated": "28.7% משולב",
            "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: מחייב אישור דגם רשמי ממכון התקנים הישראלי (בדיקת בטיחות חשמלית ותאימות קרינה לפני שחרור מהמכס)."
        },
        {
            "code": "87032210", "chapter": "פרק 87 - כלי רכב, רכיבים וציוד תחבורה",
            "description": "כלי רכב מנועיים פרטיים להסעת נוסעים, בנפח מנוע בין 1,000 סמ\"ק ל-1,500 סמ\"ק",
            "customs": "7%", "purchase_tax": "83% (בניכוי זיכוי מס ירוק)", "vat": "17%", "total_estimated": "כפוף לציון זיהום",
            "status": "רישיון יבוא משרדי", "regulation": "פקודת היבוא והיצוא: חובת הצגת רישיון יבוא בתוקף מאת משרד התחבורה והבטיחות בדרכים. יבוא מסחרי מותנה ברישום יבואן רשמי/מקביל."
        },
        {
            "code": "04069000", "chapter": "פרק 04 - מוצרי חלב, ביצים ומוצרים מן החי",
            "description": "גבינות אחרות, מגוררות או באבקה, מכל סוג",
            "customs": "סכומי מכס קצובים", "purchase_tax": "פטור (0%)", "vat": "17%", "total_estimated": "לפי מכסות חקלאיות",
            "status": "אישורים ורגולציה חמורה", "regulation": "צו יבוא חופשי: מחייב הצגת תעודת בריאות וטרינרית ותעודת כשרות מקורית. כפוף לחלוקת מכסות פטורות של משרד החקלאות."
        }
    ]

db_df = pd.DataFrame(get_expanded_db())

# 5. תפריט הצד
st.sidebar.markdown("<h3 style='color: #0F172A; font-weight: 700; margin-bottom: 15px;'>ספר המכס לפי פרקים</h3>", unsafe_allowed_html=True)
chapter_options = ["כל הפרקים"] + list(db_df["chapter"].unique())
selected_chapter = st.sidebar.radio("בחר ענף/פרק לדפדוף מהיר:", chapter_options)

# 6. שורת החיפוש
col_l, col_main, col_r = st.columns()
with col_main:
    search_input = st.text_input("", placeholder="🔍 הקלד מילת מפתח (למשל: מחשב, גבינה) או קוד פרט מכס מלא...", label_visibility="collapsed")

# 7. לוגיקת סינון
filtered_results = db_df.copy()

if selected_chapter != "כל הפרקים":
    filtered_results = filtered_results[filtered_results['chapter'] == selected_chapter]

if search_input:
    filtered_results = filtered_results[
        filtered_results['code'].str.contains(search_input) | 
        filtered_results['description'].str.contains(search_input, case=False)
    ]

# 8. הצגת התוצאות
if not filtered_results.empty:
    if search_input or selected_chapter != "כל הפרקים":
        st.markdown(f"<p style='color: #64748B; font-size: 14px; margin-bottom: 15px;'>נמצאו {len(filtered_results)} פריטים המקיימים את תנאי הסינון:</p>", unsafe_allowed_html=True)
    
    for _, row in filtered_results.iterrows():
        badge_class = "nfx-badge-alert" if row['status'] != "יבוא חופשי" else ""
        
        st.html(f"""
            <div class="nfx-result-container">
                <div class="nfx-result-header">
                    <div class="nfx-code">פרט מכס: {row['code']} <span style='font-size:13px; font-weight:400; color:#64748B; margin-right:15px;'>({row['chapter']})</span></div>
                    <div class="nfx-badge {badge_class}">{row['status']}</div>
                </div>
                
                <div style="font-size: 16px; font-weight: 600; color: #334155; margin-bottom: 20px; line-height: 1.6;">
                    <b>תיאור הפריט בספר המכס:</b> {row['description']}
                </div>
                
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
                
                <div class="nfx-regulation-box">
                    <div class="nfx-regulation-title">
                        📄 חוקיות יבוא ודרישות צו יבוא חופשי:
                    </div>
                    <div style="font-size: 14px; line-height: 1.5; margin-top: 5px;">
                        {row['regulation']}
                    </div>
                </div>
            </div>
        """)
else:
    st.markdown("<div style='text-align: center; color: #64748B; margin-top: 40px;'>לא נמצאו תוצאות תואמות לשילוב החיפוש והפרק הנבחר. נסה לאפס את תפריט הצד ל'כל הפרקים'.</div>", unsafe_allowed_html=True)
