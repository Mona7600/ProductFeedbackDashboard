import streamlit as st
import pandas as pd

from database import (
    get_feedback,
    get_category_summary,
    get_product_area_summary,
    get_sentiment_summary,
    
    get_total_feedback,
    
    get_top_categories,
    get_top_product_areas,
    get_severity_summary,
    get_critical_feedback,
    get_unhappy_features
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Product Feedback Aggregator",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 Product Feedback Aggregator")

st.write(
    "A product analytics dashboard for monitoring customer feedback, "
    "product issues, sentiment, and severity."
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

feedback = get_feedback()

category_summary = get_category_summary()
product_area_summary = get_product_area_summary()
sentiment_summary = get_sentiment_summary()
severity_summary = get_severity_summary()
category_data = get_top_categories()
product_area_data = get_top_product_areas()
critical_feedback = get_critical_feedback()
unhappy_features = get_unhappy_features()

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------

total_feedback = get_total_feedback()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Feedback",
        total_feedback
    )

with col2:
    st.metric(
        "Critical Issues",
        len(critical_feedback)
    )

with col3:
    st.metric(
        "Product Areas",
        feedback["product_area"].nunique()
    )

with col4:
    st.metric(
        "Categories",
        feedback["category"].nunique()
    )

#---------------------------------------------------
# PM Question 1
#---------------------------------------------------
st.subheader("Q1:What are users complaining about the most?")

st.bar_chart(category_data.set_index("category")["feedback_count"])
top_category = category_data.iloc[0]["category"]
top_count = category_data.iloc[0]["feedback_count"]

st.info(
    f"Most common feedback category: {top_category} "
    f"({top_count} records)")  

#---------------------------------------------------
#PM question 2
#---------------------------------------------------
st.subheader("Q2: Which product areas have the most problems?")

st.bar_chart(
    product_area_data.set_index("product_area")["feedback_count"])
top_product_area = product_area_data.iloc[0]["product_area"]
top_product_area_count = product_area_data.iloc[0]["feedback_count"]

st.info(
    f"Product area with the most feedback: "
    f"{top_product_area} "
    f"({top_product_area_count} records)"
)

#---------------------------------------------------
#PM Question 3
#---------------------------------------------------
severity_data = get_severity_summary()
st.subheader("Q3: Which issues are most urgent?")
st.bar_chart(
    severity_data.set_index("severity")["issue_count"]
)
critical_count = severity_data.loc[
    severity_data["severity"] == "Critical",
    "issue_count"
].sum()

high_count = severity_data.loc[
    severity_data["severity"] == "High",
    "issue_count"
].sum()

urgent_count = critical_count + high_count
st.metric(
    "Critical Issues",
    critical_count
)

st.metric(
    "High Issues",
    high_count
)

st.metric(
    "Critical + High Issues",
    urgent_count
)
st.warning(
    f"There are {urgent_count} Critical/High severity issues "
    f"requiring attention."
)
st.write("### Critical issues")

st.dataframe(
    critical_feedback,
    use_container_width=True
)

#---------------------------------------------------
#PM Question 4
#---------------------------------------------------

st.subheader("Q4:Are users unhappy with a particular detail?")

# Combine product area and category into one readable label
unhappy_features["feature_detail"] = (
    unhappy_features["product_area"].astype(str)
    + " - "
    + unhappy_features["category"].astype(str)
)

# Show a bar chart of negative feedback percentages
st.bar_chart(
    unhappy_features.set_index("feature_detail")["negative_percentage"]
)

# Show the complete data table
st.dataframe(
    unhappy_features,
    use_container_width=True
)

# Display an automatic PM insight, if results exist
if not unhappy_features.empty:
    most_unhappy_feature = unhappy_features.iloc[0]["feature_detail"]
    most_unhappy_percentage = unhappy_features.iloc[0]["negative_percentage"]

    st.warning(
        f"Users appear most unhappy with {most_unhappy_feature}: "
        f"{most_unhappy_percentage}% of its feedback is negative."
    )
else:
    st.info(
        "No product-area and category combinations have at least "
        "5 feedback records."
    )
# --------------------------------------------------
# CATEGORY ANALYSIS
# --------------------------------------------------

st.subheader("Feedback by Category")

st.bar_chart(
    category_summary.set_index("category")["feedback_count"]
)


# --------------------------------------------------
# PRODUCT AREA ANALYSIS
# --------------------------------------------------

st.subheader("Feedback by Product Area")

st.bar_chart(
    product_area_summary.set_index("product_area")["feedback_count"]
)


# --------------------------------------------------
# SENTIMENT ANALYSIS
# --------------------------------------------------

st.subheader("Sentiment Distribution")

st.bar_chart(
    sentiment_summary.set_index("sentiment")["feedback_count"]
)


# --------------------------------------------------
# severity ANALYSIS
# --------------------------------------------------

st.subheader("severity Distribution")

st.bar_chart(
    severity_summary.set_index("severity_bucket")["feedback_count"]
)


# --------------------------------------------------
# RAW FEEDBACK
# --------------------------------------------------

st.subheader("Customer Feedback")

st.dataframe(
    feedback,
    use_container_width=True
)

#---------------------------------------------------
#Which specific product-area/category combinations are users most unhappy with?
#---------------------------------------------------
st.subheader("Are users unhappy with a particular feature?")

st.dataframe(
    unhappy_features,
    use_container_width=True
)