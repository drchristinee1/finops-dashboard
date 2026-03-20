import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="FinOps Operating Dashboard", layout="wide")

st.title("📊 FinOps Operating Dashboard")
st.caption("Action-oriented visibility into cost drivers, ownership, priority, and savings opportunities.")

st.markdown("### From cost visibility → to engineering accountability")
# Load data
with open("data/action_plan.json") as f:
    data = json.load(f)

df = pd.DataFrame(data["action_items"])

# Add simple trend data for portfolio demo
trend_data = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "savings": [420, 510, 610, 720, 840, 970],
        "issues": [8, 7, 6, 5, 4, 3],
    }
)

# Sidebar filters
st.sidebar.header("Filters")

selected_driver = st.sidebar.multiselect(
    "Cost Driver",
    options=sorted(df["driver"].unique()),
    default=sorted(df["driver"].unique()),
)

selected_priority = st.sidebar.multiselect(
    "Priority",
    options=sorted(df["priority"].unique()),
    default=sorted(df["priority"].unique()),
)

selected_owner = st.sidebar.multiselect(
    "Owner",
    options=sorted(df["owner"].unique()),
    default=sorted(df["owner"].unique()),
)

filtered_df = df[
    df["driver"].isin(selected_driver)
    & df["priority"].isin(selected_priority)
    & df["owner"].isin(selected_owner)
]

# KPIs
total_savings = int(filtered_df["estimated_monthly_savings"].sum())
high_priority = int((filtered_df["priority"] == "high").sum())
total_issues = len(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Savings", f"${total_savings}")
col2.metric("🔥 High Priority Issues", high_priority)
col3.metric("📦 Total Issues", total_issues)

st.divider()

# Trend charts
left, right = st.columns(2)

with left:
    st.subheader("Savings Trend")
    savings_chart = trend_data.set_index("month")["savings"]
    st.line_chart(savings_chart)

with right:
    st.subheader("Issue Reduction Trend")
    issues_chart = trend_data.set_index("month")["issues"]
    st.line_chart(issues_chart)

st.divider()

# Action table
st.subheader("Action Items")
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
)
st.divider()

st.subheader("Recommended Actions")

for _, row in filtered_df.iterrows():

    # Build base text with OWNER
    action_text = (
        f"**{row['driver']} / {row['resource']}** "
        f"— Owner: {row['owner']} — "
    )

    # Driver-specific logic
    if row["driver"] == "EC2":
        action_text += (
            "Consider decommissioning or stopping the idle instance. "
        )

    elif row["driver"] == "RDS":
        action_text += (
            "Review database sizing and utilization. "
        )

    elif row["driver"] == "S3":
        action_text += (
            "Review lifecycle policy and remove unused storage. "
        )

    else:
        action_text += (
            "Review this item and assign remediation. "
        )

    # Add savings
    action_text += f"Estimated monthly savings: ${row['estimated_monthly_savings']}."

    # Display block (clean UI)
   with st.container():

    if row["priority"] == "high":
        st.error(action_text)
    elif row["priority"] == "medium":
        st.warning(action_text)
    else:
        st.info(action_text)

    st.button(
        f"Create Jira Ticket for {row['resource']}",
        key=f"jira_{row['resource']}"
    )

    st.divider()


# Breakdown charts
left2, right2 = st.columns(2)

with left2:
    st.subheader("Savings by Cost Driver")
    driver_chart = (
        filtered_df.groupby("driver")["estimated_monthly_savings"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(driver_chart)

with right2:
    st.subheader("Priority Distribution")
    priority_chart = filtered_df["priority"].value_counts()
    st.bar_chart(priority_chart)

st.divider()

# Ownership view
st.subheader("Savings by Owner")
owner_chart = (
    filtered_df.groupby("owner")["estimated_monthly_savings"]
    .sum()
    .sort_values(ascending=False)
)
st.bar_chart(owner_chart)
