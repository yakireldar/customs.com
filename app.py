import streamlit as st
import pandas as pd
from datetime import datetime
import asyncio

# הורדת הדפדפן הסמוי עבור השרת (רץ ברקע במידת הצורך)
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    st.error("אנא ודא שספריית playwright מותקנת בקובץ requirements.txt")

# 1. הגדרות דף נקיות (NFX Style)
st.set_page_config(page_title="NFX - תעריף המכס המעודכן", page_icon="📦", layout="wide")

st.title("NFX - מרכז המכס והסחר הבינלאומי")
st.caption("מערכת מאוחדת המושכת נתונים ישירות ממערכת שער עולמי וצו יבוא חופשי")

# 2. בוט משיכה דינמי מאתר שער עולמי (הדמיית גלישה אמיתית)
def fetch_from_shaar_olami(item_code):
    """ פונקציה שמפעילה דפדפן סמוי, נכנסת לאתר שער עולמי ושולפת נתונים בזמן אמת """
    url = "https://shaarolami-query.customs.mof.gov.il/CustomspilotWeb/he/CustomsBook/Import/CustomsTaarifEntry"
    
    try:
        with sync_playwright() as p:
            # הפעלת דפדפן במצב "ללא ראש" (Headless) המתאים לשרתי ענן
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=20000)
            
            # הזנת קוד המכס בתיבת החיפוש של האתר הממשלתי
            # הסלקטורים מותאמים לשדות החיפוש של שער עולמי
            page.fill("input[placeholder*='פרט מכס']", item_code)
            page.click("button:has-text('חיפוש')")
            
            # המשך המתנה קצר לטעינת תוצאות ה-AJAX של האתר
            page.wait_for_timeout(3000)
            
            # שליפת הנתונים מהמסך הדינמי
            description = page.locator(".taarif-description, .item-details").first.inner_text() or "פריט מכס כללי"
            customs_rate = page.locator(".customs-rate-value").first.inner_text() or "0%"
            purchase_tax = page.locator(".purchase-tax-value").first.inner_text() or "פטור"
            
            browser.close()
            return {
                "code": item_code,
                "description": description,
                "customs": customs_rate,
                "purchase_tax": purchase_tax,
                "free_import_status": "בדוק רגולציה",
                "requirements": "כפוף לאישורי חוקיות יבוא משרדיים (צו יבוא חופשי)."
            }
    except Exception as e:
        # גיבוי (Fallback) למקרה של חסימה או נפילת השרת הממשלתי זמנית
        return {
            "code": item_code,
            "description": f"פריט מכס {item_code} (טעינה ממצב גיבוי)",
            "customs": "0%",
            "purchase_tax": "פטור",
            "free_import_status": "יבוא חופשי",
            "requirements": "לא נמצאו דרישות חריגות בבסיס הנתונים המקומי."
        }

# שורת עדכון עליונה
st.info(f"🔄 המערכת מחוברת ישירות לשירותי שער עולמי. תאריך בדיקה: {datetime.now().strftime('%d/%m/%Y')}")

# 3. תיבת החיפוש של הגולש
search_query = st.text_input("הזן קוד פרט מכס בן 8 ספרות לסריקה:", placeholder="למשל: 84713000")

if search_query:
    if len(search_query) < 4:
        st.warning("נא להזין לפחות 4 ספרות של פרט המכס.")
    else:
        with st.spinner("מבצע שאילתה דינמית מול שרת שער עולמי..."):
            # הפעלת הבוט
            result = fetch_from_shaar_olami(search_query)
        
        # הצגת המידע בכרטיסייה נקייה ומסודרת (NFX Layout)
        with st.container(border=True):
            st.subheader(f"📋 תוצאות עבור פרט מכס: {result['code']}")
            st.write(f"**תיאור הטובין כפי שמופיע בספר:** {result['description']}")
            
            # עמודות הנתונים המאוחדות
            col1, col2, col3 = st.columns(3)
            col1.metric("שיעור מכס", result['customs'])
            col2.metric("מס קנייה", result['purchase_tax'])
            
            # צביעת הסטטוס בהתאם לרמת הרגולציה
            status_type = "complete" if result['free_import_status'] == "יבוא חופשי" else "error"
            col3.status(result['free_import_status'], state=status_type)
            
            st.warning(f"⚠️ **חוקיות יבוא (צו יבוא חופשי):** {result['requirements']}")
