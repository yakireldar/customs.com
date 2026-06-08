import streamlit as st
import pandas as pd

# 1. הגדרות דף רחב ונקי
st.set_page_config(page_title="NFX - מרכז המכס והסחר הבינלאומי", page_icon="📦", layout="wide")

# כותרת ראשית בעיצוב נקי
st.title("NFX - מרכז המכס והסחר הבינלאומי")
st.caption("ספר המכס האלקטרוני המאוחד ומערכת בדיקת חוקיות יבוא (צו יבוא חופשי)")
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

# 3. תפריט קטגוריות בצד (Sidebar)
st.sidebar.header("📁 ניווט לפי פרקים")
chapter_options = ["כל הפרקים"] + list(db_df["chapter"].unique())
selected_chapter = st.sidebar.radio("בחר ענף/פרק לדפדוף מהיר:", chapter_options)

# 4. שורת החיפוש המרכזית
search_input = st.text_input("🔍 חפש לפי קוד פרט מכס או מילת מפתח (מחשב, רכב, גבינה):", placeholder="הקלד כאן לחיפוש מהיר...")

# 5. לוגיקת סינון
filtered_results = db_df.copy()

if selected_chapter != "כל הפרקים":
    filtered_results = filtered_results[filtered_results['chapter'] == selected_chapter]

if search_input:
    filtered_results = filtered_results[
        filtered_results['code'].str.contains(search_input) | 
        filtered_results['description'].str.contains(search_input, case=False)
    ]

# 6. הצגת התוצאות בכרטיסיות מובנות ויציבות (עולה ברשת בשבריר שנייה)
if not filtered_results.empty:
    for _, row in filtered_results.iterrows():
        # יצירת קופסה לבנה (Card) עם מסגרת עדינה
        with st.container(border=True):
            
            # שורת כותרת הפריט
            col_code, col_status = st.columns([3, 1])
            col_code.subheader(f"🔢 פרט מכס: {row['code']}")
            
            # צביעת סטטוס חוקיות היבוא באופן אוטומטי
            if row['status'] == "יבוא חופשי":
                col_status.success(row['status'])
            else:
                col_status.warning(row['status'])
                
            st.write(f"**📂 קטגוריה:** {row['chapter']}")
            st.write(f"**📝 תיאור הפריט:** {row['description']}")
            st.write("")
            
            # גריד של 4 עמודות עבור נתוני המיסים (כמו ב-NFX)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("שיעור מכס", row['customs'])
            c2.metric("מס קנייה", row['purchase_tax'])
            c3.metric("מע\"מ", row['vat'])
            c4.metric("הערכת מס כוללת", row['total_estimated'])
            
            st.write("")
            # קוביית מידע מובנית עבור הרגולציה וצו יבוא חופשי
            st.info(f"📋 **חוקיות יבוא ודרישות צו יבוא חופשי:**\n\n{row['regulation']}")
else:
    st.info("לא נמצאו תוצאות תואמות. נסה לשנות את מילת החיפוש או לאפס את תפריט הצד ל-'כל הפרקים'.")
