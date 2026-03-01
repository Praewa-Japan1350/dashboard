import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Professional Student Tracker", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Student Performance Analytics Dashboard")
st.markdown("วิเคราะห์ผลการเรียนและพฤติกรรมการเข้าเรียนแบบ Real-time")

data = {
    'Student': ['Somchai', 'Somsri', 'Ananda', 'Bowie', 'Chai', 'Daw', 'Ee', 'Fah', 'Gai', 'Hana'],
    'Attendance_Rate': [95, 80, 60, 92, 45, 88, 75, 98, 82, 91],
    'Midterm_Score': [85, 72, 55, 90, 40, 78, 65, 95, 70, 88],
    'Final_Score': [88, 75, 50, 94, 35, 82, 70, 99, 75, 92],
    'Major': ['IT', 'CS', 'IT', 'DS', 'CS', 'DS', 'IT', 'DS', 'CS', 'IT']
}
df = pd.DataFrame(data)

with st.sidebar:
    st.header("🔍 Filter Options")
    selected_major = st.multiselect(
        "Select Department:",
        options=df['Major'].unique(),
        default=df['Major'].unique()
    )
    
    if st.button("Reset Filters"):
        st.rerun()

filtered_df = df[df['Major'].isin(selected_major)]

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Total Students", len(filtered_df))
with col_m2:
    st.metric("Avg Attendance", f"{filtered_df['Attendance_Rate'].mean():.1f}%")
with col_m3:
    st.metric("Avg Midterm", f"{filtered_df['Midterm_Score'].mean():.1f}")
with col_m4:
    st.metric("Avg Final", f"{filtered_df['Final_Score'].mean():.1f}")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Performance Comparison")
    fig1 = px.bar(filtered_df, x='Student', y=['Midterm_Score', 'Final_Score'], 
                 barmode='group', 
                 color_discrete_map={'Midterm_Score': '#5dade2', 'Final_Score': '#ec7063'},
                 template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📈 Attendance Trend")
    fig2 = px.area(filtered_df, x='Student', y='Attendance_Rate', 
                  markers=True, line_shape="spline",
                  color_discrete_sequence=['#48c9b0'])
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("🎯 Insights: Attendance vs. Final Grade")
fig3 = px.scatter(filtered_df, x='Attendance_Rate', y='Final_Score', 
                 size='Final_Score', color='Major', 
                 hover_name='Student', trendline="ols",
                 color_discrete_sequence=px.colors.qualitative.Safe)
st.plotly_chart(fig3, use_container_width=True)

with st.expander("📋 View Detailed Student Records"):
    st.dataframe(filtered_df.sort_values(by='Final_Score', ascending=False), use_container_width=True)
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV Report", data=csv, file_name="student_report.csv", mime="text/csv")
