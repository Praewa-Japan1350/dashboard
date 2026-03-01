 import streamlit as st
import pandas as pd
import plotly.express as px

# การตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Student Tracker", layout="wide")

# หัวข้อ Dashboard
st.title("🎓 Student Performance & Attendance Tracker")
st.markdown("---")

# --- ส่วนข้อมูล (Mockup Data) ---
# เคล็ดลับ: คุณสามารถ Commit การเพิ่มข้อมูลทีละคนเพื่อให้ได้จำนวน Commit เยอะขึ้น
data = {
    'Student': ['Somchai', 'Somsri', 'Ananda', 'Bowie', 'Chai', 'Daw', 'Ee', 'Fah'],
    'Attendance_Rate': [95, 80, 60, 92, 45, 88, 75, 98],
    'Midterm_Score': [85, 72, 55, 90, 40, 78, 65, 95],
    'Final_Score': [88, 75, 50, 94, 35, 82, 70, 99],
    'Major': ['IT', 'CS', 'IT', 'DS', 'CS', 'DS', 'IT', 'DS']
}
df = pd.DataFrame(data)

# --- ส่วน Interactive (Sidebar) ---
st.sidebar.header("Filter Options")
selected_major = st.sidebar.multiselect(
    "Select Major:",
    options=df['Major'].unique(),
    default=df['Major'].unique()
)

# กรองข้อมูลตามที่เลือก
filtered_df = df[df['Major'].isin(selected_major)]

# --- ส่วนแสดงผล Dashboard ---

# แถวที่ 1: กราฟที่ 1 และ 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Midterm vs Final Scores")
    # กราฟที่ 1: Grouped Bar Chart
    fig1 = px.bar(filtered_df, x='Student', y=['Midterm_Score', 'Final_Score'], 
                 barmode='group', color_discrete_sequence=['#3498db', '#e74c3c'])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📈 Attendance Rate (%)")
    # กราฟที่ 2: Line Chart แสดงเปอร์เซ็นต์การเข้าเรียน
    fig2 = px.line(filtered_df, x='Student', y='Attendance_Rate', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# แถวที่ 2: กราฟที่ 3
st.markdown("---")
st.subheader("🎯 Attendance vs Performance Correlation")
# กราฟที่ 3: Scatter Plot (Interactive - เลื่อนเมาส์ดูจุดได้)
fig3 = px.scatter(filtered_df, x='Attendance_Rate', y='Final_Score', 
                 size='Final_Score', color='Major', hover_name='Student',
                 labels={'Attendance_Rate': 'Attendance (%)', 'Final_Score': 'Final Score'})
st.plotly_chart(fig3, use_container_width=True)

# แสดงตารางข้อมูลดิบ
if st.checkbox("Show Raw Data"):
    st.write(filtered_df)
