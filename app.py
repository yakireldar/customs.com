import streamlit as st
import pandas as pd

# 1. הגדרות דף רחב
st.set_page_config(page_title="ספר מכס ומס קניה", page_icon="📦", layout="wide")

# כותרת ראשית מיושרת לימין ונרחבת
st.title("ספר מכס ומס קניה")
st.write("---")

# 2. מאגר נתונים רשמי - כל 21 החלקים הראשיים של תעריף המכס
@st.cache_data
def get_customs_sections():
    return [
        {"code": "01", "section": "חלק 01: בעלי חיים חיים ומוצרים מן החי", "description": "בשר, דגים, חלב, ביצים, דבש ומוצרים אחרים מן החי"},
        {"code": "02", "section": "חלק 02: מוצרים מצמחים", "description": "ירקות, פירות, דגנים, קפה, תה, תבלינים, זרעים וקמח"},
        {"code": "03", "section": "חלק 03: שומנים ושמנים מן החי או מן הצומח", "description": "שומנים, שמנים, שעוות מן החי או הצומח ושומנים מאכלים מבושלים"},
        {"code": "04", "section": "חלק 04: מוצרי תעשיית המזון; משקאות וטבק", "description": "סוכר, קקאו, מוצרי מאפה, משקאות חריפים, סיגריות וטבק"},
        {"code": "05", "section": "חלק 05: מוצרים מינרליים", "description": "מלח, גופרית, אדמות, אבנים, דלקים מינרליים, שמנים מזוקקים וחשמל"},
        {"code": "06", "section": "חלק 06: מוצרי תעשיות כימיות", "description": "כימיקלים, תרופות, דשנים, צבעים, שמנים אתריים וסבונים"},
        {"code": "07", "section": "חלק 07: פלסטיק, גומי ומוצריהם", "description": "חומרי פלסטיק, מוצרי פלסטיק, גומי טבעי או סינתטי וצמיגים"},
        {"code": "08", "section": "חלק 08: עורות, פרוות ומוצריהם; חפצי נסיעה", "description": "עורות גולמיים, תיקים, חפצי נסיעה, ארנקים ומוצרי פרווה"},
        {"code": "09", "section": "חלק 09: עץ ומוצריו; שמיח; קש וסלסלות", "description": "עץ לביד, פחם עץ, שמיח ומוצרי קליעה וקש"},
        {"code": "10", "section": "חלק 10: חומרי גלם לייצור נייר; נייר ומוצריו", "description": "עיסת עץ, נייר, קרטון, ספרים, עיתונים ומוצרי דפוס"},
        {"code": "11", "section": "חלק 11: חומרי טקסטיל ומוצרי טקסטיל", "description": "חוטים, בדים, בגדים, הלבשה מוכנה, שטיחים וטקסטיל לבית"},
        {"code": "12", "section": "חלק 12: נעליים, כיסויי ראש, מטריות ונוצות", "description": "נעליים, מגפיים, כיסויי ראש, מטריות, פרחים מלאכותיים וחפצי נוצות"},
        {"code": "13", "section": "חלק 13: מוצרים מאבן, גבס, צמנט, קרמיקה וזכוכית", "description": "מוצרי בטון, אריחי קרמיקה, כלי חרס, זכוכית ומוצרי זכוכית"},
        {"code": "14", "section": "חלק 14: פנינים, אבנים יקרות, מתכות יקרות ותכשיטים", "description": "זהב, כסף, פלטינה, תכשיטי אופנה, מטבעות ואבני חן"},
        {"code": "15", "section": "חלק 15: מתכות פשוטות ומוצריהן", "description": "ברזל, פלדה, נחושת, אלומיניום, כלי עבודה, סכו\"ם וברגים"},
        {"code": "16", "section": "חלק 16: מכונות, מכשירים מכניים וציוד חשמלי", "description": "מחשבים, סמארטפונים, טלוויזיות, מנועים, כבלים וציוד אלקטרוני"},
        {"code": "17", "section": "חלק 17: כלי רכב, כלי טיס, כלי שיט וציוד תחבורה", "description": "מכוניות, חלקי חילוף לרכב, אופנועים, אופניים, מטוסים ואוניות"},
        {"code": "18", "section": "חלק 18: מכשירים אופטיים, רפואיים, שעונים וכלי נגינה", "description": "משקפיים, ציוד רפואי, שעוני יד, מצלמות, מכשירי מדידה וגיטרות"},
        {"code": "19", "section": "חלק 19: נשק ותחמושת; חלקיקיהם וכלים שלהם", "description": "רובים, אקדחים, תחמושת, אביזרי ציד וביטחון"},
        {"code": "20", "section": "חלק 20: מוצרים מוגמרים שונים", "description": "רהיטים, מזרנים, צעצועים, משחקים, פריטי ספורט ועגלות ילדים"},
        {"code": "21", "section": "חלק 21: חפצי אמנות, חפצים לאוספים ועתיקות", "description": "ציורים מקוריים, פסלים, בולים, מטבעות עתיקים ורהיטים עתיקים"}
    ]

db_df = pd.DataFrame(get_customs_sections())

# 3. חלוקת המסך: תפריט "כל הפרקים" בצד ימין (1), רווח קטן, ותוכן החיפוש במרכז ושמאל (3)
col_sidebar_right, col_spacer, col_content = st.columns([1.2, 0.1, 3])

# הגדרת תפריט "כל הפרקים" לאורך בצד ימין
with col_sidebar_right:
    st.subheader("📁 כל הפרקים")
    section_options = ["הצג הכל"] + list(db_df["section"].unique())
    selected_section = st.radio("ניווט מהיר לפי חלקים:", section_options, label_visibility="collapsed")

# אזור החיפוש הממורכז והתוצאות בצד שמאל
with col_content:
    
    # חלוקה פנימית לעמודות כדי למרכז את שורת החיפוש (עמודה מרכזית רחבה)
    col_search_l, col_search_main, col_search_r = st.columns([0.2, 3, 0.2])
    
    with col_search_main:
        # סינון המאגר בהתאם לבחירת הפרק מימין
        filtered_db = db_df.copy()
        if selected_section != "הצג הכל":
            filtered_results = filtered_db[filtered_db['section'] == selected_section]
        else:
            filtered_results = filtered_db

        # הכנת האפשרויות להשלמה אוטומטית
        search_options = [f"{row['code']} - {row['section']} ({row['description']})" for _, row in filtered_results.iterrows()]

        # שורת חיפוש ממורכזת ונקייה לחלוטין שאומרת רק "חיפוש"
        selected_search = st.selectbox(
            "חיפוש",
            options=search_options,
            index=None,
            placeholder="🔍 התחל להקליד מילת מפתח או קוד חלק...",
            label_visibility="visible"  # מציג את המילה "חיפוש" בדיוק מעל התיבה
        )

    st.write("<br>", unsafe_allowed_html=True)

    # 4. הצגת התוצאה לאחר בחירה
    if selected_search:
        # חילוץ קוד החלק מתוך המחרוזת הנבחרת
        selected_code = selected_search.split(" - ")[0]
        row_data = db_df[db_df['code'] == selected_code].iloc[0]
        
        # דימוי נתוני מיסים ורגולציה מותאמים אישית לחלק הנבחר
        is_free = "יבוא חופשי" if selected_code in ["01", "03", "09", "10", "14", "21"] else "נדרש אישור / רגולציה"
        customs_rate = "0% (פטור)" if selected_code in ["16", "08", "14", "21"] else "משתנה לפי פריט"
        purchase_tax = "חייב במס קנייה" if selected_code in ["04", "17", "06"] else "פטור"
        regulation_details = "חלק זה כולל פריטים המפוקחים על ידי משרדי הממשלה השונים (תקנים, בריאות או תחבורה). יש לבדוק תת-סעיף ספציפי בצו יבוא חופשי." if is_free != "יבוא חופשי" else "רוב הפריטים בחלק זה פטורים מאישורים חריגים, כפוף להצהרת יבואן תקינה."

        # כרטיסיית המידע המרכזית במבנה NFX
        with st.container(border=True):
            col_res_code, col_res_status = st.columns(2)
            col_res_code.subheader(f"🔢 {row_data['section']}")
            
            if is_free == "יבוא חופשי":
                col_res_status.success(is_free)
            else:
                col_res_status.warning(is_free)
                
            st.write(f"**📝 תיאור והיקף החלק:** {row_data['description']}")
            st.write("")
            
            # גריד מיסים (4 עמודות)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("שיעור מכס ממוצע", customs_rate)
            c2.metric("מס קנייה", purchase_tax)
            c3.metric("מע\"מ", "17%")
            c4.metric("סטטוס עדכניות", "מעודכן 2026")
            
            st.write("")
            st.info(f"📋 **חוקיות יבוא ודרישות רגולציה (צו יבוא חופשי):**\n\n{regulation_details}")
            
    elif selected_section != "הצג הכל":
        # אם המשתמש בחר פרק מימין אך לא הקליד בחיפוש, נציג לו את הפרק שבחר כברירת מחדל
        row_data = db_df[db_df['section'] == selected_section].iloc[0]
        with st.container(border=True):
            st.subheader(f"📂 נבחרו נתוני: {row_data['section']}")
            st.write(f"השתמש בשורת החיפוש המרכזית כדי לסווג מוצרים ספציפיים תחת **{row_data['description']}**.")
