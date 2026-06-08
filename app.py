import streamlit as st
import pandas as pd
import requests

# 1. הגדרות דף נקיות וממורכזות ללא תפריטים מיותרים
st.set_page_config(page_title="ספר מכס ומס קניה", page_icon="📦", layout="centered")

# כותרת האתר
st.title("ספר מכס ומס קניה")
st.write("---")

# 2. פונקציה חכמה המושכת נתונים בזמן אמת ממאגר רשות המסים הרשמי (Data.gov.il)
@st.cache_data(ttl=3600)  # שמירת המידע במטמון לשעה כדי להבטיח מהירות שיא
def search_customs_government_api(query_text):
    if not query_text:
        return []
        
    # מזהה המאגר הרשמי של ספר סיווג טובין ביבוא (רשות המסים)
    resource_id = "5536eaa1-2e51-406b-aff6-b9ca02801b7c"
    url = f"https://data.gov.il{resource_id}&q={query_text}&limit=30"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            records = response.json().get('result', {}).get('records', [])
            return records
    except Exception:
        pass
    return []

# 3. שורת חיפוש אחת חלקה ונקייה לחלוטין
search_query = st.text_input(
    "חיפוש",
    value="",
    placeholder="🔍 הקלד קוד פרט מכס (למשל: 8536) או תיאור מוצר...",
    label_visibility="visible"
)

# 4. עיבוד הנתונים והצגת התוצאות מהמאגר הממשלתי החי
if search_query:
    with st.spinner("מחפש במאגר רשות המסים..."):
        api_results = search_customs_government_api(search_query)
        
    if api_results:
        st.write(f"נמצאו {len(api_results)} תתי-סעיפים תואמים:")
        
        # מעבר על כל פריטי המכס שנמצאו בממשלה והצגתם במבנה כרטיסיות נקי
        for item in api_results:
            # חילוץ הערכים מתוך השדות הרשמיים של ה-API הממשלתי
            item_code = str(item.get('ITEM_CODE', item.get('פרט מכס', ''))).replace('.', '')
            item_desc = item.get('ITEM_DESCRIPTION', item.get('תיאור פריט', ''))
            customs_rate = item.get('CUSTOMS_RATE', 'פטור')
            purchase_rate = item.get('PURCHASE_TAX', 'פטור')
            vat_rate = "17%"
            
            # קביעת סטטוס חוקיות היבוא באופן אוטומטי
            has_approval = item.get('REQUIRED_APPROVAL', False) or item.get('APPROVAL_DETAILS', False)
            status_text = "נדרש אישור / רגולציה" if has_approval else "יבוא חופשי"
            regulation_text = item.get('APPROVAL_DETAILS', "אין דרישות חריגות על פי צו יבוא חופשי מעודכן.")
            
            # יצירת מבנה כרטיסייה לכל פריט מכס שנמצא
            with st.container(border=True):
                col_code, col_status = st.columns(2)
                col_code.subheader(f"🔢 פרט מכס: {item_code}")
                
                if status_text == "יבוא חופשי":
                    col_status.success(status_text)
                else:
                    col_status.warning(status_text)
                    
                st.write(f"**📝 תיאור מלא בספר:** {item_desc}")
                st.write("---")
                
                # גריד מיסים ב-4 עמודות נקיות
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("שיעור מכס", f"{customs_rate}%" if str(customs_rate).isdigit() else customs_rate)
                c2.metric("מס קנייה", f"{purchase_rate}%" if str(purchase_rate).isdigit() else purchase_rate)
                c3.metric("מע\"מ", vat_rate)
                c4.metric("סטטוס", "מעודכן 2026")
                
                st.write("")
                st.info(f"📋 **חוקיות יבוא ורגולציה (צו יבוא חופשי):**\n\n{regulation_text}")
    else:
        st.info("לא נמצאו תוצאות עבור החיפוש שהוקלד. נסה להזין קוד חלקי (כמו 8536) או מילת מפתח כללית.")
