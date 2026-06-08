import streamlit as st
import pandas as pd

# 1. הגדרות דף נקיות
st.set_page_config(page_title="ספר מכס ומס קניה", page_icon="📦", layout="centered")

# כותרת האתר
st.title("ספר מכס ומס קניה")
st.write("---")

# 2. מאגר הנתונים המלא
@st.cache_data
def get_clean_db():
    return [
        {
            "code": "8536", 
            "description": "ציוד למיתוג, להגנה או לחיבור של מעגלים חשמליים (למשל: מפסקים, ממסרים, נתיכים, תקעים, ביתי נורה)",
            "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total_estimated": "17% (מע\"מ בלבד)",
            "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: פריטים תחת קוד 8536 מחייבים בדיקת התאמה לתקן רשמי (מכון התקנים) בנושא בטיחות חשמלית ואביזרי מיתוג לפני השחרור מהמכס."
        },
        {
            "code": "8471", 
            "description": "מכונות אוטומטיות לעיבוד נתונים ויחידות שלהן; קוראים מגנטיים או אופטיים (מחשבים, לפטופים, שרתים)",
            "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total_estimated": "17% (מע\"מ בלבד)",
            "status": "יבוא חופשי", "regulation": "אין הגבלות מכוח צו יבוא חופשי. פטור מאישור משרד התקשורת לציוד מחשוב סטנדרטי ביבוא מסחרי."
        },
        {
            "code": "8703", 
            "description": "מכוניות נוסעים וכלי רכב מנועיים אחרים המיועדים בעיקר להסעת בני אדם (כולל רכבי סטיישן ומרוץ)",
            "customs": "7%", "purchase_tax": "83% (בניכוי זיכוי מס ירוק)", "vat": "17%", "total_estimated": "משתנה לפי זיהום",
            "status": "רישיון יבוא משרדי", "regulation": "פקודת היבוא והיצוא: חובת הצגת רישיון יבוא בתוקף מאת משרד התחבורה. יבוא מסחרי מותנה ברישום יבואן רשמי או מקביל."
        },
        {
            "code": "8528", 
            "description": "מסכים ומקרנים, שאינם כוללים מכשיר לקליטת טלוויזיה; מקלטי טלוויזיה בצבע (מסכי מחשב וטלוויזיות)",
            "customs": "פטור (0%)", "purchase_tax": "10%", "vat": "17%", "total_estimated": "28.7% משולב",
            "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: מחייב אישור דגם רשמי ממכון התקנים הישראלי לבטיחות קרינה וחשמל."
        },
        {
            "code": "0406", 
            "description": "גבינות מכל הסוגים וקריש גבינה (גבינות קשות, רכות, מגוררות או באבקה)",
            "customs": "מכס קצוב לק\"ג", "purchase_tax": "פטור (0%)", "vat": "17%", "total_estimated": "לפי מכסות",
            "status": "אישורים ורגולציה חמורה", "regulation": "צו יבוא חופשי: מחייב הצגת תעודת בריאות וטרינרית ותעודת כשרות מקורית. כפוף לאישור משרד הבריאות (תחנת הסגר)."
        }
    ]

db_df = pd.DataFrame(get_clean_db())

# 3. הכנת האפשרויות לשורת החיפוש
search_options = [f"{row['code']} - {row['description'][:80]}..." for _, row in db_df.iterrows()]

# 4. שורת חיפוש אחת נקייה וממורכזת
selected_search = st.selectbox(
    "חיפוש",
    options=search_options,
    index=None,
    placeholder="🔍 הקלד קוד פרט מכס (למשל: 8536) או שם מוצר...",
    label_visibility="visible"
)

st.write("")

# 5. הצגת נתוני הפריט שנבחר מהחיפוש
if selected_search:
    extracted_code = selected_search.split(" - ")[0]  # חילוץ קוד המספר בצורה בטוחה
    matching_rows = db_df[db_df['code'] == extracted_code]
    
    if not matching_rows.empty:
        row = matching_rows.iloc[0]  # שליפה יציבה של השורה הראשונה
        
        # כרטיסיית התוצאה הנקייה
        with st.container(border=True):
            col_code, col_status = st.columns(2)
            col_code.subheader(f"🔢 פרט מכס: {row['code']}")
            
            if row['status'] == "יבוא חופשי":
                col_status.success(row['status'])
            else:
                col_status.warning(row['status'])
                
            st.write(f"**📝 תיאור מלא:** {row['description']}")
            st.write("")
            
            # נתוני המיסים ב-4 עמודות נקיות
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("שיעור מכס", row['customs'])
            c2.metric("מס קנייה", row['purchase_tax'])
            c3.metric("מע\"מ", row['vat'])
            c4.metric("הערכת מס כוללת", row['total_estimated'])
            
            st.write("")
            st.info(f"📋 **חוקיות יבוא ורגולציה (צו יבוא חופשי):**\n\n{row['regulation']}")
