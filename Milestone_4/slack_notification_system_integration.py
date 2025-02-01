import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Get the Slack Webhook URL from environment variables
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


# Tabs for Navigation
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

# Add yellow shade to the sidebar using custom CSS
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color:#FFDB58 ;
        }
    </style>
    """,
    unsafe_allow_html=True
)

tab = st.sidebar.radio(
    "Main Menu",
    ["Home", "Global Monitoring", "Predictive Modeling", "Inventory Optimization", "Manage Inventory", "Real-Time Alerts", "Reporting"],
)

# Function to send Slack notifications
def send_slack_notification(message, webhook_url):
    payload = {"text": message}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        if response.status_code != 200:
            st.error(f"Failed to send notification. Slack returned: {response.status_code}, {response.text}")
    except Exception as e:
        st.error(f"Error while sending Slack notification: {e}")

# Function to generate alerts
def generate_alerts(df, thresholds, selected_alerts):
    alerts = []
    for _, row in df.iterrows():
        if "Risk" in selected_alerts and row['Risk Factor'] > thresholds['Risk']:
            alert = f"🚨 High risk factor detected for {row['product_name']} (Risk Factor: {row['Risk Factor']})"
            alerts.append(alert)
            send_slack_notification(alert, SLACK_WEBHOOK_URL)

        if "Inventory" in selected_alerts and row['Inventory Level (%)'] < thresholds['Inventory']:
            alert = f"⚠️ Low inventory for {row['product_name']} (Inventory Level: {row['Inventory Level (%)']}%)"
            alerts.append(alert)
            send_slack_notification(alert, SLACK_WEBHOOK_URL)

        if "Supplier" in selected_alerts and row['Supplier Reliability'] < thresholds['Supplier']:
            alert = f"📉 Low supplier reliability for {row['product_name']} (Reliability: {row['Supplier Reliability']})"
            alerts.append(alert)
            send_slack_notification(alert, SLACK_WEBHOOK_URL)

        if "Transportation" in selected_alerts and row['Transportation Risk'] > thresholds['Transportation']:
            alert = f"🚧 High transportation risk for {row['product_name']} (Transportation Risk: {row['Transportation Risk']})"
            alerts.append(alert)
            send_slack_notification(alert, SLACK_WEBHOOK_URL)

    return alerts

# Sidebar: Upload Dataset
uploaded_file = st.sidebar.file_uploader("Upload Your Dataset (CSV or Excel)", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        dataset = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        dataset = pd.read_excel(uploaded_file)
    st.sidebar.success("Dataset uploaded successfully!")
else:
    data_path = 'Final_product_dataset.csv'
    dataset = pd.read_csv(data_path)

# Preprocess data for different modules
global_data = dataset[["product_name", "Supplier", "Supplier Reliability", "Transportation Risk", "Risk Factor"]]
global_data = global_data.rename(columns={
    "product_name": "Product Name",
    "Supplier Reliability": "Reliability",
    "Transportation Risk": "Transport Risk",
    "Risk Factor": "Risk Factor"
})

risk_predictions = dataset[["product_name", "Risk Factor"]]
risk_predictions = risk_predictions.rename(columns={
    "product_name": "Product",
    "Risk Factor": "Risk Score"
})
risk_predictions["Probability"] = (risk_predictions["Risk Score"] / 10).clip(0, 1)

inventory_data = dataset[["product_name", "quantity", "Inventory Level (%)"]]
inventory_data = inventory_data.rename(columns={
    "product_name": "Item",
    "quantity": "Current Stock",
    "Inventory Level (%)": "Inventory Level"
})

# Page Descriptions
if tab == "Home":
    st.title("LogistiQ : AI-Driven Supply Chain Disruption Prediction & Inventory Optimization Dashboard!")
    st.write("""
    This dashboard provides insights and predictions into supply chain risks and inventory optimization.
    
    Navigate through the different sections using the sidebar:
    - **Global Monitoring**: Analyze global supply chain trends and risks.
    - **Predictive Modeling**: View disruption predictions and probabilities.
    - **Inventory Optimization**: Assess inventory levels and make adjustments.
    - **Manage Inventory**: Allows selective alerts based on product needs.
    - **Real-Time Alerts**: Receive critical alerts for supply chain risks.
    - **Reporting**: Visualize overall risk distribution across your supply chain.
    """)
    st.caption("Supply Chain Management System Dashboard" )

elif tab == "Global Monitoring":
    st.header("Global Data Monitoring and Analysis")
    st.write("""
    This section monitors global supply chain data to identify potential risk factors.
    """)
    st.dataframe(global_data)

elif tab == "Predictive Modeling":
    st.header("Predictive Disruption Modeling")
    st.write("""
    This section predicts potential disruptions, providing risk scores and probabilities for better decision-making.
    """)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(risk_predictions, x="Product", y="Probability", color="Risk Score", title="Disruption Probability")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(risk_predictions)

elif tab == "Inventory Optimization":
    st.header("Inventory Optimization")
    st.write("""
    This section recommends inventory adjustments based on predictive analysis.
    """)
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(inventory_data, x="Item", y="Current Stock", color="Inventory Level", title="Current Stock vs Inventory Level")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(inventory_data)

elif tab == "Manage Inventory":
        st.header("Manage Inventory")
        st.write("""
    This section provides real-time alerts for critical supply chain risks and inventory issues.
    """)

        # Product Selection
        product_names = dataset['product_name'].unique()
        selected_product = st.selectbox("Select a product to view its status:", product_names)

        # Display selected product status
        product_status = dataset[dataset['product_name'] == selected_product]
        st.write(f"Details for **{selected_product}**:")
        st.dataframe(product_status)

        # Sidebar: Select alert types
        alert_types = ["Risk", "Inventory", "Supplier", "Transportation"]
        selected_alerts = st.sidebar.multiselect("Choose alert types to view:", alert_types, default=alert_types)
    
        # Sidebar thresholds for alerts
        risk_threshold = st.sidebar.slider("Risk Factor Threshold", min_value=0, max_value=10, value=5)
        inventory_threshold = st.sidebar.slider("Inventory Level Threshold (%)", min_value=0, max_value=100, value=20)
        supplier_threshold = st.sidebar.slider("Supplier Reliability Threshold", min_value=0, max_value=10, value=5)
        transportation_threshold = st.sidebar.slider("Transportation Risk Threshold", min_value=0, max_value=10, value=5)

        # Display inventory alerts for the selected product
        st.subheader(f"Alerts for {selected_product}")
        product_alerts = generate_alerts(product_status, {
            "Risk": risk_threshold,
            "Inventory": inventory_threshold,
            "Supplier": supplier_threshold,
            "Transportation": transportation_threshold
        }, selected_alerts)
        
        if product_alerts:
            for alert in product_alerts:
                st.warning(alert)
        else:
            st.success(f"No alerts triggered for {selected_product}.")

elif tab == "Real-Time Alerts":
    st.header("Real-Time Alerts and Notifications")
    st.write("""
    This section provides real-time alerts for critical supply chain risks and inventory issues.
    """)
    alert_types = ["Risk", "Inventory", "Supplier", "Transportation"]
    selected_alerts = st.sidebar.multiselect("Choose alert types to view:", alert_types, default=alert_types)
    thresholds = {
        "Risk": st.sidebar.slider("Risk Factor Threshold", min_value=0, max_value=10, value=5),
        "Inventory": st.sidebar.slider("Inventory Level Threshold (%)", min_value=0, max_value=100, value=20),
        "Supplier": st.sidebar.slider("Supplier Reliability Threshold", min_value=0, max_value=10, value=5),
        "Transportation": st.sidebar.slider("Transportation Risk Threshold", min_value=0, max_value=10, value=5),
    }
    alerts = generate_alerts(dataset, thresholds, selected_alerts)
    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("No alerts triggered for the selected types.")

elif tab == "Reporting":
    st.header("Reporting Dashboard")
    st.write("""
    This section visualizes the overall risk distribution in your supply chain.
    """)
    report_data = dataset["Risk Factor"].value_counts(bins=[0, 3, 6, 10], sort=False).reset_index()
    report_data.columns = ["Risk Level", "Count"]
    report_data["Risk Level"] = report_data["Risk Level"].astype(str)
    fig_report = px.pie(report_data, names="Risk Level", values="Count", title="Supply Chain Risk Distribution")
    st.plotly_chart(fig_report, use_container_width=True)

