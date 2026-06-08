import streamlit as st
import pandas as pd

# 1. הגדרות דף רחב ונקי
st.set_page_config(page_title="ספר מכס ומס קניה", page_icon="📦", layout="wide")

# כותרת ראשית נקייה וממוקדת
st.title("ספר מכס ומס קניה")
st.write("---")

# 2. בסיס נתונים מובנה ומהיר
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

# 3. חלוקת הדף הראשי: תוכן במרכז, תפריט "כל הפרקים" מצד שמאל
col_content, col_spacer, col_sidebar_left = st.columns([3, 0.2, 1])

# הגדרת תפריט "כל הפרקים" בצד שמאל
with col_sidebar_left:
    st.markdown("<h3 style='color: #0F172A; font-weight: 700; margin-bottom: 15px;'>📁 כל הפרקים</h3>", unsafe_allowed_html=True)
    chapter_options = ["כל הפרקים"] + list(db_df["chapter"].unique())
    selected_chapter = st.radio("בחר ענף/פרק לדפדוף מהיר:", chapter_options, label_visibility="collapsed")

# אזור החיפוש והתוצאות במרכז הדף
with col_content:
    # 4. הכנת רשימת אפשרויות להשלמה אוטומטית בהתאם לפרק שנבחר משמאל
    filtered_db_for_search = db_df.copy()
    if selected_chapter != "כל הפרקים":
        filtered_db_for_search = filtered_db_for_search[filtered_db_for_search['chapter'] == selected_chapter]

    search_options = [f"{row['code']} - {row['description']}" for _, row in filtered_db_for_search.iterrows()]

    # 5. תיבת חיפוש נקייה לחלוטין עם השלמה אוטומטית (ללא כיתובים מעליה)
    selected_search = st.selectbox(
        "",
        options=search_options,
        index=0 if search_options else None,
        placeholder="🔍 הקלד מילת מפתח או קוד פרט מכס...",
        label_visibility="collapsed"
    )

    # 6. הצגת הנתונים עבור הפריט שנבחר מההשלמה האוטומטית
    if selected_search:
        selected_code = selected_search.split(" - ")[0]
        row = db_df[db_df['code'] == selected_code].iloc[0]
        
        # הצגת התוצאה בכרטיסייה יציבה ומסודרת
        with st.container(border=True):
            col_code, col_status = st.columns(2)
            col_code.subheader(f"🔢 פרט מכס: {row['code']}")
            
            if row['status'] == "יבוא חופשי":
                col_status.success(row['status'])
            else:
                col_status.warning(row['status'])
                
            st.write(f"**📂 קטגוריה:** {row['chapter']}")
            st.write(f"**📝 תיאור הפריט:** {row['description']}")
            st.write("")
            
            # גריד מיסים (4 עמודות)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("שיעור מכס", row['customs'])
            c2.metric("מס קנייה", row['purchase_tax'])
            c3.metric("מע\"מ", row['vat'])
            c4.metric("הערכת מס כוללת", row['total_estimated'])
            
            st.write("")
            st.info(f"📋 **חוקיות יבוא ודרישות צו יבוא חופשי:**\n\n{row['regulation']}")
            
    elif not search_options:
        st.info("אין פריטים זמינים בפרק שנבחר.")
