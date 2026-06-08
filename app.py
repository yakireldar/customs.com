import streamlit as st

# 1. הגדרות דף נקי וממורכז
st.set_page_config(page_title="ספר מכס ומס קניה", page_icon="📦", layout="centered")

# כותרת האתר
st.title("ספר מכס ומס קניה")
st.write("---")

# 2. מאגר הנתונים המלא והמדויק לפי צילום המסך שלך (קודים מלאים בני 10 ספרות)
customs_db = {
    "8536000000": {
        "description": "מכשירים חשמליים למיתוג, להגנה או לחיבור של מעגלים חשמליים או לביצוע חיבורים",
        "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total": "17% (מע\"מ בלבד)",
        "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: מחייב בדיקת התאמה לתקן רשמי של מכון התקנים הישראלי לאביזרי מיתוג וחיבור."
    },
    "8536100000": {
        "description": "נתיכים (ציוד למיתוג והגנה)",
        "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total": "17% (מע\"מ בלבד)",
        "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: כפוף לבדיקת בטיחות רשמית של מכון התקנים לנתיכים ומפסקי זרם."
    },
    "8536101000": {
        "description": "המתכננים להתקנה במבנה או עליו; מכשירים המתכננים להתקנה מחוץ למבנה (OUT DOORS)",
        "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total": "17%",
        "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: חובת אישור בטיחות חשמלית לציוד חוץ ומבנים."
    },
    "8536109000": {
        "description": "נתיכים - אחרים",
        "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total": "17%",
        "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: בדיקת מעבדה מאושרת לפי קטגוריית נתיכים כללית."
    },
    "8536109100": {
        "description": "שמשקל כל אחד אינו עולה על 150 גרם",
        "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total": "17%",
        "status": "יבוא חופשי", "regulation": "מאושר לשחרור מהיר תחת תנאי משקל קל, כפוף להצהרת תאימות בסיסית."
    }
}

# 3. הכנת רשימת האפשרויות לשורת החיפוש
search_options = [f"{code} - {data['description']}" for code, data in customs_db.items()]

# 4. שורת חיפוש אחת נקייה וממורכזת
selected_item = st.selectbox(
    "חיפוש",
    options=search_options,
    index=None,
    placeholder="🔍 הקלד קוד פרט מכס (למשל: 8536) או שם מוצר...",
    label_visibility="visible"
)

st.write("")

# 5. הצגת התוצאה בצורה מאובטחת ותקינה (מתוקן לחלוטין!)
if selected_item:
    # התיקון הקריטי: חילוץ קוד המפתח המדויק כטקסט נקי ולא כרשימה
    item_key = selected_item.split(" - ")[0]
    
    # שליפת המידע בצורה בטוחה
    if item_key in customs_db:
        item_data = customs_db[item_key]
        
        # כרטיסיית התוצאה הנקייה
        with st.container(border=True):
            col_code, col_status = st.columns(2)
            col_code.subheader(f"🔢 פרט מכס: {item_key}")
            
            if item_data['status'] == "יבוא חופשי":
                col_status.success(item_data['status'])
            else:
                col_status.warning(item_data['status'])
                
            st.write(f"**📝 תיאור מלא בספר:** {item_data['description']}")
            st.write("---")
            
            # גריד מיסים ב-4 עמודות נקיות
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("שיעור מכס", item_data['customs'])
            c2.metric("מס קנייה", item_data['purchase_tax'])
            c3.metric("מע\"מ", item_data['vat'])
            c4.metric("הערכת מס כוללת", item_data['total'])
            
            st.write("")
            st.info(f"📋 **חוקיות יבוא ורגולציה (צו יבוא חופשי):**\n\n{item_data['regulation']}")
