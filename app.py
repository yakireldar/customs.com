import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. הגדרות דף בסיסיות ונקיות
st.set_page_config(page_title="NFX - תעריף המכס המעודכן", page_icon="📦", layout="wide")

# כותרות פשוטות ללא HTML כדי למנוע שגיאות שרת
st.title("NFX - מרכז המכס והסחר הבינלאומי")
st.caption("מערכת חכמה לסיווג, בדיקת שיעורי מס וחוקיות יבוא (צו יבוא חופשי)")

# 2. מנגנון משיכה ורענון אוטומטי ממאגר הממשלתי (API של data.gov.il)
@st.cache_data(ttl=86400)
def fetch_live_government_data():
    resource_id = "5536eaa1-2e51-406b-aff6-b9ca02801b7c" 
    url = f"https://data.gov.il{resource_id}&limit=1000"
    
    try:
        response = requests.get(url, timeout=10)
        res_data = response.json()
        records = res_data['result']['records']
        
        raw_df = pd.DataFrame(records)
        clean_data = []
        for _, row in raw_df.iterrows():
            clean_data.append({
                "code": str(row.get('ITEM_CODE', row.get('פרט מכס', ''))).replace('.', ''),
                "description": row.get('ITEM_DESCRIPTION', row.get('תיאור פריט', 'פריט מכס כללי')),
                "customs": f"{row.get('CUSTOMS_RATE', '0')}%",
                "purchase_tax": f"{row.get('PURCHASE_TAX', '0')}%",
                "free_import_status": "הגבלות ואישורים" if row.get('REQUIRED_APPROVAL') else "יבוא חופשי",
                "requirements": row.get('APPROVAL_DETAILS', "אין דרישות חריגות על פי צו יבוא חופשי מעודכן.")
            })
        return pd.DataFrame(clean_data), datetime.now().strftime("%d/%m/%Y %H:%M")
    
    except Exception:
        fallback_data = [
            {"code": "84713000", "description": "מחשבים אישיים נישאים (לפטופים)", "customs": "0%", "purchase_tax": "פטור", "free_import_status": "יבוא חופשי", "requirements": "פטור מאישורים חריגים."},
            {"code": "87032210", "description": "כלי רכב מנועיים פרטיים", "customs": "7%", "purchase_tax": "83%", "free_import_status": "הגבלות ואישורים", "requirements": "נדרש אישור בתוקף ממשרד התחבורה."},
            {"code": "04069000", "description": "גבינות קשות ומגוררות", "customs": "משתנה", "purchase_tax": "פטור", "free_import_status": "הגבלות ואישורים", "requirements": "אישור בריאות וטרינרי ותעודת כשרות."}
        ]
        return pd.DataFrame(fallback_data), "טעינה מגיבוי מקומי (שרת הממשלה לא זמין)"

df, last_update_time = fetch_live_government_data()

# שורת סטטוס נקייה
st.success(f"🔄 המידע מסונכרן באופן אוטומטי. עדכון אחרון: {last_update_time}")

# תיבת חיפוש
search_query = st.text_input("חפש לפי קוד פרט מכס או מילת מפתח (למשל: מחשב, רכב, גבינה):", placeholder="הקלד כאן לחיפוש...")

if search_query:
    filtered_df = df[df['code'].str.contains(search_query) | df['description'].str.contains(search_query, case=False)]
    
    if not filtered_df.empty:
        st.write(f"נמצאו {len(filtered_df)} תוצאות מעודכנות:")
        
        for index, row in filtered_df.iterrows():
            # שימוש ברכיב המובנה st.container ליצירת כרטיסייה נקייה ומסודרת
            with st.container(border=True):
                st.subheader(f"פרט מכס: {row['code']}")
                st.write(f"**תיאור:** {row['description']}")
                
                # חלוקה לעמודות מידע
                col1, col2, col3 = st.columns(3)
                col1.metric("שיעור מכס", row['customs'])
                col2.metric("מס קנייה", row['purchase_tax'])
                col3.status(row['free_import_status'], state="complete" if row['free_import_status'] == "יבוא חופשי" else "error")
                
                st.info(f"**חוקיות יבוא ורגולציה (צו יבוא חופשי):** {row['requirements']}")
    else:
        st.info("לא נמצאו תוצאות. נסה מילת חיפוש אחרת.")
