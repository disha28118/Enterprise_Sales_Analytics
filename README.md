# Enterprise Sales Analytics Dashboard

An enterprise-grade sales analytics dashboard built using Python and Streamlit, designed to mirror Power BI–style executive dashboards.
This project delivers key business KPIs, revenue trends, and performance insights using real-world sales data.

## Project Overview

The goal of this project is to provide decision-makers and analysts with a single-screen view of sales performance, enabling them to quickly understand:
Overall revenue health
Sales trends over time
Regional and product-level performance
Key drivers of business growth
The dashboard follows real MNC BI design standards — clean layout, neutral KPIs, and clear storytelling.

## Key Features

Executive KPI Cards
Total Revenue
Average Order Value
Total Orders
Revenue Trend Analysis
Time-series line chart with markers for clear trend interpretation
Performance Breakdowns
Revenue by Region
Revenue by Product Category
Interactive Filters
Date range
Region
Product category
Business Insights Section
Top-performing region
Top-performing product
Total records analyzed

## Tech Stack

Python
Streamlit
Pandas
Matplotlib

## Project Structure
Enterprise_Sales_Analytics/
│
├── app.py               # Streamlit dashboard application
├── sales_data.csv       # Sales dataset (CSV)
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation

## How to Run the Project

Clone the repository:

git clone https://github.com/your-username/enterprise-sales-analytics.git
cd enterprise-sales-analytics

## Install dependencies:
pip install -r requirements.txt
Run the Streamlit app:
streamlit run app.py
The dashboard will open automatically in your browser.

