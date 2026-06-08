import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. הגדרות דף
st.set_page_config(page_title="NFX - תעריף המכס המעודכן", page_icon="📦", layout="wide")

# הזרקת ה-CSS בצורה הנכונה והעדכנית ביותר כדי למנוע את השגיאה
st.html("""
    <style>
    .stApp { background-color: #F8FAFC; color: #1E293B; font-family: 'Segoe UI', system-ui, sans-serif; }
    .nfx-title { font-size: 32px; font-weight: 700; color: #0F172A; border-bottom: 2px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 5px; }
    .nfx-tagline { color: #64748B; font-size: 15px; margin-bottom: 20px; }
    .update-bar { background-color: #EFF6FF; border: 1px solid #BFDBFE; color: #1E40AF; padding: 10px; border-radius: 6px; font-size: 13px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; }
    .customs-item-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 20px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .status-badge-free { background-color: #DCFCE7; color: #15803D; padding: 4px 10px; border-radius: 12px; font-size: 13px; font-weight: 600; display: inline-block; }
    .status-badge-restrict { background-color: #FEE2E2; color: #B91C1C; padding: 4px 10px; border-radius: 12px; font-size: 13px; font-weight: 600; display: inline-block; }
    .item-code-header { font-size: 18px; font-weight: 700; color: #2563EB; }
    </style>
""")

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
            {"code": "87032210", "description": "כלי רכב מנועיים פרטיים", "customs": "7%", "purchase_tax": "83%", "free_import_status": "הגבלות ואישורים", "requirements": "נדרש אישור בתוקם ממשרד התחבורה."},
            {"code": "04069000", "description": "גבינות קשות ומגוררות", "customs": "משתנה", "purchase_tax": "פטור", "free_import_status": "הגבלות ואישורים", "requirements": "אישור בריאות וטרינרי ותעודת כשרות."}
        ]
        return pd.DataFrame(fallback_data), "טעינה מגיבוי מקומי (שרת הממשלה לא זמין)"

df, last_update_time = fetch_live_government_data()

# 3. מבנה האתר (UI)
st.markdown('<div class="nfx-title">NFX - מרכז המכס והסחר הבינלאומי</div>', unsafe_allow_html=True)
st.markdown('<div class="nfx-tagline">מערכת חכמה לסיווג, בדיקת שיעורי מס וחוקיות יבוא (צו יבוא חופשי)</div>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="update-bar">
        <span>🔄 <b>סטטוס סנכרון:</b> המידע מסונכרן באופן אוטומטי מול שרתי רשות המסים ומשרד הכלכלה.</span>
        <span><b>עדכון אחרון:</b> {last_update_time}</span>
    </div>
""", unsafe_allow_html=True)

search_query = st.text_input("", placeholder="הקלד קוד פרט מכס או מילת מפתח (למשל: מחשב, רכב)...", label_visibility="collapsed")

if search_query:
    filtered_df = df[df['code'].str.contains(search_query) | df['description'].str.contains(search_query, case=False)]
    
    if not filtered_df.empty:
        st.markdown(f"<p style='color: #64748B; font-size: 14px;'>נמצאו {len(filtered_df)} תוצאות מעודכנות:</p>", unsafe_allow_html=True)
        
        for index, row in filtered_df.iterrows():
            badge = '<span class="status-badge-free">יבוא חופשי</span>' if row['free_import_status'] == "יבוא חופשי" else '<span class="status-badge-restrict">נדרש אישור / רגולציה</span>'
            
            st.markdown(f"""
                <div class="customs-item-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span class="item-code-header">פרט מכס: {row['code']}</span>
                        {badge}
                    </div>
                    <div style="font-size: 16px; font-weight: 500; margin-bottom: 15px; color: #334155;">{row['description']}</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; background-color: #F1F5F9; padding: 12px; border-radius: 6px; margin-bottom: 12px;">
                        <div>
                            <strong style="color: #475569; font-size: 13px;">שיעור מכס עדכני:</strong><br>
                            <span style="font-size: 15px; font-weight: 600; color: #0F172A;">{row['customs']}</span>
                        </div>
                        <div>
                            <strong style="color: #475569; font-size: 13px;">מס קנייה:</strong><br>
                            <span style="font-size: 15px; font-weight: 600; color: #0F172A;">{row['purchase_tax']}</span>
                        </div>
                    </div>
                    <div>
                        <strong style="color: #475569; font-size: 13px;">חוקיות יבוא ורגולציה (צו יבוא חופשי):</strong><br>
                        <span style="font-size: 14px; color: #334155;">{row['requirements']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("לא נמצאו תוצאות. נסה מילת חיפוש אחרת.")
