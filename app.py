import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="FinOps Dashboard", layout="wide")

st.title("📊 FinOps Action Dashboard")

# Load data
with open("data/action_plan.json") as f:
    data = json.load(f)

df = pd.DataFrame(data["action_items"])

# KPIs
total_savings = df["estimated_monthly_savings"].sum()
high_priority = len(df[df["priority"] == "high"])
total_issues = len(df)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Savings", f"${total_savings}")
col2.metric("🔥 High Priority Issues", high_priority)
col3.metric("📦 Total Issues", total_issues)

st.divider()

# Table
st.subheader("Action Items")
st.dataframe(df)

st.divider()

# Savings by driver
st.subheader("Savings by Cost Driver")
driver_chart = df.groupby("driver")["estimated_monthly_savings"].sum()
st.bar_chart(driver_chart)

# Priority breakdown
st.subheader("Priority Distribution")
priority_chart = df["priority"].value_counts()
st.bar_chart(priority_chart)
