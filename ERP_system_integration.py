import pandas as pd
import streamlit as st

# Load the dataset
file_path = 'Final_product_dataset.csv'
data = pd.read_csv(file_path)

# Streamlit App
def main():
    st.title("LogistiQ")

    menu = ["Home", "Manage Inventory", "View Data"]
    choice = st.sidebar.selectbox("Menu", menu)
    st.sidebar.header("Inventory & Alert Settings")


    # Sidebar: Select alert types
    alert_types = [ "Risk","Inventory", ]
    selected_alerts = st.sidebar.multiselect("Choose alert types to view:", alert_types, default=alert_types)
    
    # Sidebar thresholds for alerts
    risk_threshold = st.sidebar.slider("Risk Factor Threshold", min_value=0, max_value=10, value=5)
    inventory_threshold = st.sidebar.slider("Inventory Level Threshold (%)", min_value=0, max_value=100, value=20)
    supplier_threshold = st.sidebar.slider("Supplier Reliability Threshold", min_value=0, max_value=10, value=5)
    transportation_threshold = st.sidebar.slider("Transportation Risk Threshold", min_value=0, max_value=10, value=5)



    if choice == "Home":
        st.write(
            """
            ### Milestone 3: 
            Designed an  **ERP System with Integrated Alerts** to streamline inventory management and supply chain monitoring by providing real-time alerts and detailed product status updates. It allows users to actively monitor risk factors, inventory levels, supplier reliability, and transportation risks, with customizable thresholds for each type of alert. The system generates automatic alerts when these thresholds are exceeded or breached, ensuring that businesses can respond to issues promptly and prevent potential disruptions in their operations. With an intuitive interface, users can select and manage product details, and analyze risk factors associated with each item, making it a powerful tool for proactive inventory optimization and supply chain management.

            ### Key Features
            - **Customizable Alerts**: Choose from multiple alert types such as Risk, Inventory, Supplier, and Transportation to suit business needs.
            - **Threshold Management**: Set adjustable thresholds for each alert type to trigger notifications when conditions are met.
            - **Real-time Inventory Monitoring**: Select individual products to check their current inventory status and potential risks.
            - **Automated Alert Generation**: Receive alerts instantly when inventory levels fall below defined thresholds or when risk factors exceed acceptable limits.
            - **Detailed Product Data**: View comprehensive details for each product, including inventory level, supplier reliability, and transportation risk.
            - **User-friendly Interface**: Easy-to-navigate dashboard and sidebar for quick access to alert management and product details.
            """
        )
        st.subheader("Dashboard Overview")
        
        # Generate alerts based on selected types and thresholds
        alerts = generate_alerts(data, {
            "Risk": risk_threshold,
            "Inventory": inventory_threshold,
            "Supplier": supplier_threshold,
            "Transportation": transportation_threshold
        }, selected_alerts)

        st.subheader("Alerts Summary")
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("No alerts triggered for the selected types.")

    elif choice == "Manage Inventory":
        st.subheader("Manage Inventory")

        # Product Selection
        product_names = data['product_name'].unique()
        selected_product = st.selectbox("Select a product to view its status:", product_names)

        # Display selected product status
        product_status = data[data['product_name'] == selected_product]
        st.write(f"Details for **{selected_product}**:")
        st.dataframe(product_status)

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

    elif choice == "View Data":
        st.subheader("View All Data")
        st.dataframe(data)

# Function to generate alerts
def generate_alerts(df, thresholds, selected_alerts):
    alerts = []

    for _, row in df.iterrows():
        if "Risk" in selected_alerts and row['Risk Factor'] > thresholds['Risk']:
            alerts.append(f"High risk factor detected for {row['product_name']} (Risk Factor: {row['Risk Factor']})")
        if "Inventory" in selected_alerts and row['Inventory Level (%)'] < thresholds['Inventory']:
            alerts.append(f"Low inventory for {row['product_name']} (Inventory Level: {row['Inventory Level (%)']}%)")
        if "Supplier" in selected_alerts and row['Supplier Reliability'] < thresholds['Supplier']:
            alerts.append(f"Low supplier reliability for {row['product_name']} (Reliability: {row['Supplier Reliability']})")
        if "Transportation" in selected_alerts and row['Transportation Risk'] > thresholds['Transportation']:
            alerts.append(f"High transportation risk for {row['product_name']} (Transportation Risk: {row['Transportation Risk']})")
    return alerts

if __name__ == "__main__":
    main()
