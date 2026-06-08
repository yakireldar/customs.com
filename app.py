import streamlit as st
import pandas as pd

# 1. הגדרות דף רחב ונקי
st.set_page_config(page_title="ספר מכס ומס קניה", page_icon="📦", layout="wide")

# כותרת ראשית נקייה
st.title("ספר מכס ומס קניה")
st.write("---")

# 2. בסיס נתונים אמיתי עם קודי המכס בני 4 ספרות
@st.cache_data
def get_real_customs_db():
    return [
        {
            "code": "8536", "chapter": "פרק 85 - מכשירים חשמליים, טלוויזיות וציוד שמע",
            "description": "ציוד למיתוג, להגנה או לחיבור של מעגלים חשמליים (למשל: מפסקים, ממסרים, נתיכים, תקעים, ביתי נורה)",
            "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total_estimated": "17% (מע\"מ בלבד)",
            "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: פריטים תחת קוד 8536 מחייבים בדיקת התאמה לתקן רשמי (מכון התקנים) בנושא בטיחות חשמלית ואביזרי מיתוג לפני השחרור מהמכס."
        },
        {
            "code": "8471", "chapter": "פרק 84 - מכשירים מכניים, מחשבים ואלקטרוניקה",
            "description": "מכונות אוטומטיות לעיבוד נתונים ויחידות שלהן; קוראים מגנטיים או אופטיים (מחשבים, לפטופים, שרתים)",
            "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total_estimated": "17% (מע\"מ בלבד)",
            "status": "יבוא חופשי", "regulation": "אין הגבלות מכוח צו יבוא חופשי. פטור מאישור משרד התקשורת לציוד מחשוב סטנדרטי ביבוא מסחרי."
        },
        {
            "code": "8703", "chapter": "פרק 87 - כלי רכב, רכיבים וציוד תחבורה",
            "description": "מכוניות נוסעים וכלי רכב מנועיים אחרים המיועדים בעיקר להסעת בני אדם (כולל רכבי סטיישן ומרוץ)",
            "customs": "7%", "purchase_tax": "83% (בניכוי זיכוי מס ירוק)", "vat": "17%", "total_estimated": "משתנה לפי זיהום",
            "status": "רישיון יבוא משרדי", "regulation": "פקודת היבוא והיצוא: חובת הצגת רישיון יבוא בתוקף מאת משרד התחבורה. יבוא מסחרי מותנה ברישום יבואן רשמי או מקביל."
        },
        {
            "code": "8528", "chapter": "פרק 85 - מכשירים חשמליים, טלוויזיות וציוד שמע",
            "description": "מסכים ומקרנים, שאינם כוללים מכשיר לקליטת טלוויזיה; מקלטי טלוויזיה בצבע (מסכי מחשב וטלוויזיות)",
            "customs": "פטור (0%)", "purchase_tax": "10%", "vat": "17%", "total_estimated": "28.7% משולב",
            "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: מחייב אישור דגם רשמי ממכון התקנים הישראלי לבטיחות קרינה וחשמל."
        },
        {
            "code": "0406", "chapter": "פרק 04 - מוצרי חלב, ביצים ומוצרים מן החי",
            "description": "גבינות מכל הסוגים וקריש גבינה (גבינות קשות, רכות, מגוררות או באבקה)",
            "customs": "מכס קצוב לק\"ג", "purchase_tax": "פטור (0%)", "vat": "17%", "total_estimated": "לפי מכסות",
            "status": "אישורים ורגולציה חמורה", "regulation": "צו יבוא חופשי: מחייב הצגת תעודת בריאות וטרינרית ותעודת כשרות מקורית. כפוף לאישור משרד הבריאות (תחנת הסגר)."
        }
    ]

db_df = pd.DataFrame(get_real_customs_db())

# 3. חלוקת הדף: תוכן החיפוש במרכז (3), תפריט "כל הפרקים" לאורך בצד ימין (1)
col_content, col_spacer, col_sidebar_right = st.columns([3, 0.2, 1.2])

# הגדרת תפריט "כל הפרקים" בצד ימין
with col_sidebar_right:
    st.subheader("📁 כל הפרקים")
    chapter_options = ["הצג הכל"] + list(db_df["chapter"].unique())
    selected_chapter = st.radio("ניווט מהיר לפי פרקים:", chapter_options, label_visibility="collapsed")

# אזור החיפוש והתוצאות במרכז המסך
with col_content:
    # 4. סינון רשימת האפשרויות לפי בחירת הפרק מימין
    filtered_db = db_df.copy()
    if selected_chapter != "הצג הכל":
        filtered_db = filtered_db[filtered_db['chapter'] == selected_chapter]

    # הכנת רשימת הצעות נקייה להשלמה האוטומטית
    search_options = [f"{row['code']} - {row['description'][:80]}..." for _, row in filtered_db.iterrows()]

    # 5. שורת חיפוש ממורכזת ונקייה לחלוטין (רשום רק "חיפוש")
    selected_search = st.selectbox(
        "חיפוש",
        options=search_options,
        index=None,
        placeholder="🔍 הקלד קוד פרט מכס (למשל: 8536) או מילת מפתח...",
        label_visibility="visible"
    )

    st.write("<br>", unsafe_allowed_html=True)

    # 6. הצגת הנתונים עבור הפריט שנבחר מההשלמה האוטומטית
    if selected_search:
        extracted_code = selected_search.split(" - ")[0]  # לוקח רק את קוד המספר הבודד
        matching_rows = db_df[db_df['code'] == extracted_code]
        
        if not matching_rows.empty:
            row = matching_rows.iloc[0]  # שליפה תקינה ומאובטחת לחלוטין של השורה
            
            # הצגת התוצאה בכרטיסייה מעוצבת
            with st.container(border=True):
                col_code, col_status = st.columns(2)
                col_code.subheader(f"🔢 פרט מכס: {row['code']}")
                
                if row['status'] == "יבוא חופשי":
                    col_status.success(row['status'])
                else:
                    col_status.warning(row['status'])
                    
                st.write(f"**📂 קטגוריה:** {row['chapter']}")
                st.write(f"**📝 תיאור מלא בספר המכס:** {row['description']}")
                st.write("")
                
                # גריד מיסים (4 עמודות)
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("שיעור מכס", row['customs'])
                c2.metric("מס קנייה", row['purchase_tax'])
                c3.metric("מע\"מ", row['vat'])
                c4.metric("הערכת מס כוללת", row['total_estimated'])
                
                st.write("")
                st.info(f"📋 **חוקיות יבוא ודרישות רגולציה (צו יבוא חופשי):**\n\n{row['regulation']}")
                
    elif selected_chapter != "הצג הכל":
        st.info(f"נבחרו נתוני: **{selected_chapter}**. השתמש בשורת החיפוש המרכזית כדי למצוא קודים ספציפיים.")
