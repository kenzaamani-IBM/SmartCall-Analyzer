import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 Daily Insights Dashboard", layout="wide")

st.title("📊 Daily Supervisor Dashboard")
st.markdown("This dashboard displays insights from all analyzed customer service calls.")

try:
    df = pd.read_csv('daily_insights.csv')

    if df.empty:
        st.warning("No insights available yet. Please analyze some calls first.")
    else:
        st.dataframe(df, use_container_width=True)

        st.subheader("📞 Recent Calls Summary")
        for i, row in df.iterrows():
            with st.expander(f"Call {i+1} — {row['DateTime']}"):
                st.markdown(f"**📝 Summary:** {row['Summary']}")
                st.markdown(f"**👤 Employee Feedback:** {row['EmployeeFeedback']}")
                st.markdown(f"**😊 Sentiment:** {row['Sentiment']}")
                st.markdown(f"**💡 Recommendations:** {row['Recommendations']}")

except FileNotFoundError:
    st.error("⚠️ No insights file found. Run the main app (`app.py`) and analyze at least one call.")
