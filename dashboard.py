import streamlit as st
import pandas as pd
import plotly.express as px

# הגדרת כיוון הטקסט מימין לשמאל
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    body {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# בדיקת אתחול נתונים
if "metrics" not in st.session_state:
    st.session_state.metrics = pd.DataFrame({
        'מדד': ["חשיפה כללית", "עוקבים חדשים", "תגובות לפוסטים", "לידים חדשים", "הרשמות לשיעור ניסיון", "מכירות חדשות"],
        'יעד': [10000, 200, 500, 50, 20, 10],
        'תוצאה': [8500, 180, 600, 45, 25, 12]
    })

if "weekly_content" not in st.session_state:
    st.session_state.weekly_content = pd.DataFrame({
        'יום': ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"],
        'נושא': ["סיפור השראה", "טיפ מקצועי", "מאחורי הקלעים", "תוכן חינוכי", "מוצר/שירות", "סיכום שבועי"],
        'אחראי': ["בעלים", "שוחי", "שוחי", "בעלים", "שוחי", "בעלים"],
        'סטטוס': ["הושלם", "הושלם", "בתהליך", "ממתין", "ממתין", "ממתין"]
    })

if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame({
        'משימה': ["הכנת תוכן לשבוע הבא", "בדיקת ביצועי קמפיינים", "ניתוח נתונים והפקת תובנות", "פגישת צוות שיווק", "עדכון אסטרטגיה"],
        'הושלם': [True, True, False, False, False]
    })

# פונקציה להצגת הדשבורד
def display_dashboard():
    st.title("דשבורד שיווק - Studio")
    
    # מדדי ביצועים
    st.subheader("מדדי ביצועים")
    for index, row in st.session_state.metrics.iterrows():
        delta = row['תוצאה'] - row['יעד']
        delta_color = "inverse" if delta >= 0 else "normal"
        st.metric(label=row['מדד'], value=row['תוצאה'], delta=delta, delta_color=delta_color)
    
    # גרף מדדי ביצועים
    fig = px.bar(st.session_state.metrics, x='מדד', y='תוצאה', color='מדד', title="תוצאות מול יעדים")
    st.plotly_chart(fig, use_container_width=True)
    
    # תכנון תוכן שבועי
    st.subheader("תכנון תוכן שבועי")
    st.table(st.session_state.weekly_content)
    
    # משימות שבועיות
    st.subheader("משימות שבועיות")
    for index, row in st.session_state.tasks.iterrows():
        status = "✅" if row['הושלם'] else "❌"
        st.write(f"{status} {row['משימה']}")

# פונקציה לעריכת נתונים
def edit_data():
    st.subheader("עריכת מדדי ביצועים")
    edited_metrics = st.data_editor(st.session_state.metrics, num_rows="dynamic")
    st.session_state.metrics = edited_metrics
    
    st.subheader("עריכת תכנון תוכן שבועי")
    edited_weekly_content = st.data_editor(st.session_state.weekly_content, num_rows="dynamic")
    st.session_state.weekly_content = edited_weekly_content
    
    st.subheader("עריכת משימות שבועיות")
    edited_tasks = st.data_editor(st.session_state.tasks, num_rows="dynamic")
    st.session_state.tasks = edited_tasks

# יצירת טאבים
tab1, tab2 = st.tabs(["תצוגת דשבורד", "עריכת נתונים"])

with tab1:
    display_dashboard()

with tab2:
    edit_data()
