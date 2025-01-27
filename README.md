<H1>LogistiQ- AI Driven Supply Chain Disruption Predictor and Inventory Optimization System</H1>

## Overview

A Python-based system designed to streamline supply chain operations and optimize inventory management. This project incorporates **machine learning models** for predicting supply chain risks and analyzing inventory data to ensure efficient decision-making. The system uses **PostgreSQL** as the database and **Streamlit** for an interactive web dashboard. It also provide real time inventory and supply chain risk alerts over Slack.

![LogistiQ Dashboard](https://github.com/SK-21-D3v/LogistiQ-Infosys_Project_1/blob/main/Screenshot%20(1436).png?raw=true)<br>

## Outcome

● Accurate prediction of supply chain disruptions through analysis of news, supplier data, and transportation trends.<br>

● Dynamic inventory level optimization based on predicted supply chain reliability and disruption risks.<br>

● Real-time notifications and ERP integration for immediate inventory adjustments and reordering recommendations. <br>

● Significant reduction in supply chain-related losses and improved operational efficiency through proactive risk management.<br>

## Features  

- **Data Fetching**: Incorporates APIs for fetching external supply chain-related data.
- **Database Integration**: Stores and retrieves supply chain data from a **PostgreSQL** database.
- **Interactive Dashboard**: Provides a visual representation of supply chain insights using **Streamlit**.
- **Inventory Analysis**: Analyzes inventory levels, demand patterns, and trends for better inventory control.  
- **Risk Prediction**: Integrates machine learning models to predict risks in the supply chain.    


## Technology Stack  

- **Python**: The primary programming language used for developing the core logic and machine learning models.
- **Frontend**: Streamlit used to create the frontend to display dynamic web applications.
- **PostgreSQL**: A relational database used to store supply chain data, including product details, inventory levels, and risk factors.
- **Machine Learning**: Various algorithms used for supply chain optimization, including classification, regression, and time-series forecasting.
- **APIs**: Integration with external data sources such as the NewsAPI for fetching real-time supply chain-related news.
- **Visualization**: Plotly, Matplotlib were used for Graphical Visualitzations of the data. 
- **Environment Management**: Python-dotenv was created with necessary libraries. 

## Installation

### Prerequisites

Before setting up the project, ensure you have the following installed:  
- Python 3.12.6  
- PostgreSQL database  
- Required Python libraries (specified in `requirements.txt`)  

### Step-by-Step Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/SK-21-D3v/LogistiQ-Infosys_Project_1.git
   cd LogistiQ-Infosys_Project_1

2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up the PostgreSQL database:
   - Ensure PostgreSQL is installed and running.
   - Create a database and configure your credentials in the `.env` file.

4. Run the project:
   ```bash
   python app.py

## Usage

Once the project is up and running, you can interact with the supply chain management system via the user interface. The system provides options for:
- Fetching real-time supply chain news.
- Analyzing stock levels and inventory data.
- Receiving risk predictions for supply chain disruptions.
- Receiving real time alerts on Slack.

## Future Work

- **Advanced Analytics**: Implement additional machine learning models to enhance risk prediction and inventory management.
- **User Interface Improvements**: Enhance the frontend for a better user experience.
- **Integration with ERP Systems**: Enable integration with ERP systems for a more seamless flow of data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
