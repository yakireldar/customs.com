import streamlit as st

# 1. הגדרות דף נקי וממורכז
st.set_page_config(page_title="ספר מכס ומס קניה", page_icon="📦", layout="centered")

# כותרת האתר
st.title("ספר מכס ומס קניה")
st.write("---")

# 2. מאגר נתונים פשוט ומאובטח במבנה של מילון (Dictionary) - מונע שגיאות פנימיות
customs_db = {
    "8536": {
        "description": "ציוד למיתוג, להגנה או לחיבור של מעגלים חשמליים (למשל: מפסקים, ממסרים, נתיכים, תקעים, ביתי נורה)",
        "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total": "17% (מע\"מ בלבד)",
        "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: פריטים תחת קוד 8536 מחייבים בדיקת התאמה לתקן רשמי (מכון התקנים) בנושא בטיחות חשמלית ואביזרי מיתוג לפני השחרור מהמכס."
    },
    "8471": {
        "description": "מכונות אוטומטיות לעיבוד נתונים ויחידות שלהן; קוראים מגנטיים או אופטיים (מחשבים, לפטופים, שרתים)",
        "customs": "פטור (0%)", "purchase_tax": "פטור (0%)", "vat": "17%", "total": "17% (מע\"מ בלבד)",
        "status": "יבוא חופשי", "regulation": "אין הגבלות מכוח צו יבוא חופשי. פטור מאישור משרד התקשורת לציוד מחשוב סטנדרטי ביבוא מסחרי."
    },
    "8703": {
        "description": "מכוניות נוסעים וכלי רכב מנועיים אחרים המיועדים בעיקר להסעת בני אדם (כולל רכבי סטיישן ומרוץ)",
        "customs": "7%", "purchase_tax": "83% (בניכוי זיכוי מס ירוק)", "vat": "17%", "total": "משתנה לפי זיהום",
        "status": "רישיון יבוא משרדי", "regulation": "פקודת היבוא והיצוא: חובת הצגת רישיון יבוא בתוקף מאת משרד התחבורה. יבוא מסחרי מותנה ברישום יבואן רשמי או מקביל."
    },
    "8528": {
        "description": "מסכים ומקרנים, שאינם כוללים מכשיר לקליטת טלוויזיה; מקלטי טלוויזיה בצבע (מסכי מחשב וטלוויזיות)",
        "customs": "פטור (0%)", "purchase_tax": "10%", "vat": "17%", "total": "28.7% משולב",
        "status": "נדרש אישור תקן", "regulation": "צו יבוא חופשי: מחייב אישור דגם רשמי ממכון התקנים הישראלי לבטיחות קרינה וחשמל."
    },
    "0406": {
        "description": "גבינות מכל הסוגים וקריש גבינה (גבינות קשות, רכות, מגוררות או באבקה)",
        "customs": "מכס קצוב לק\"ג", "purchase_tax": "פטור (0%)", "vat": "17%", "total": "לפי מכסות חקלאיות",
        "status": "אישורים ורגולציה חמורה", "regulation": "צו יבוא חופשי: מחייב הצגת תעודת בריאות וטרינרית ותעודת כשרות מקורית. כפוף לאישור משרד הבריאות (תחנת הסגר)."
    }
}

# 3. הכנת רשימת אפשרויות חלקה עבור שורת החיפוש האחת
search_options = [f"{code} - {data['description'][:60]}..." for code, data in customs_db.items()]

# 4. שורת חיפוש אחת נקייה וממורכזת
selected_item = st.selectbox(
    "חיפוש",
    options=search_options,
    index=None,
    placeholder="🔍 הקלד קוד פרט מכס (למשל: 8536) או שם מוצר...",
    label_visibility="visible"
)

st.write("")

# 5. הצגת התוצאה בצורה מאובטחת ללא סיכוי לקריסה
if selected_item:
    # חילוץ קוד המפתח המדויק (4 הספרות הראשונות) בצורה בטוחה בטקסט נקי
    item_key = selected_item.split(" - ")[0]
    
    # שליפת המידע מתוך המילון
    if item_key in customs_db:
        item_data = customs_db[item_key]
        
        # כרטיסיית תוצאה נקייה ויציבה
        with st.container(border=True):
            col_code, col_status = st.columns(2)
            col_code.subheader(f"🔢 פרט מכס: {item_key}")
            
            if item_data['status'] == "יבוא חופשי":
                col_status.success(item_data['status'])
            else:
                col_status.warning(item_data['status'])
                
            st.write(f"**📝 תיאור מלא:** {item_data['description']}")
            st.write("---")
            
            # גריד מיסים (4 עמודות מוגדרות)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("שיעור מכס", item_data['customs'])
            c2.metric("מס קנייה", item_data['purchase_tax'])
            c3.metric("מע\"מ", item_data['vat'])
            c4.metric("הערכת מס כוללת", item_data['total'])
            
            st.write("")
            st.info(f"📋 **חוקיות יבוא ורגולציה (צו יבוא חופשי):**\n\n{item_data['regulation']}")
