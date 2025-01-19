# Project Workflow:

**Current Milestone 3 Dashboard**

![ERP_System_Dashboard](https://github.com/SK-21-D3v/LogistiQ-Infosys_Project_1/blob/main/Screenshot%20(1421).png?raw=true)<br>

![Alert Mechanism](https://github.com/SK-21-D3v/LogistiQ-Infosys_Project_1/blob/main/Screenshot%20(1422).png?raw=true)<br>

![Inventory Management](https://github.com/SK-21-D3v/LogistiQ-Infosys_Project_1/blob/main/Screenshot%20(1423).png?raw=true)<br>

## Milestone 1 : Global Data Monitoring and Analysis Engine

- `save_to_excel.py` : Collected data via API calls and collected them and stored them on the local storage in excel format <br>

- `main.py`- Fetched and stored data in json format alongside storing it in the PostgreSql database.<br>

- `nasdaq_data.json` : Stored the data generated in json format.<br>

- `database_integration.py` : Analyzed the data stored in the PostgreSQL database to gain insights.<br>

- `app.py` : Displayed the analysed data over an interactive UI Dashboard with the help of Streamlit.<br>

## Milestone 2 : Predictive Disruption Modeling System

- `ml_training.ipynb` : ML model (XGBoost) was trained over the dataset (`Electronics Data.csv`). <br>

- `product_risk_integration.ipynb` : Dummy risk factors were integrated within the already existing dataset (`Electronics Data.csv`) further stored as `Final_product_dataset.csv`, after which the model was retrained alongside the risk and sentiments and stored within `xgboost_risk_prediction_model.pkl` pickle file. <br>

- `xgboost_risk_prediction_model.pkl` : Pickle file generated upon model training.<br>

## Milestone 3 : ERP Integration and Inventory Adjustment Module

- `alert_generation.ipynb` : Consists of sample code with respect to alert generations based on `Final_product_dataset.csv`.<br>

- `ERP_system_integration.py` : Consists of a Streamlit Dashboard where a sample ERP System is designed and the Alert mechanism is integrated for automated alert notifications and inventory management functioning.


## Milestone 4 : Real-Time Alert and Reporting Dashboard 
*Yet to be executed*



