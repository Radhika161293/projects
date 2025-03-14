import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Database connection
db_url = "mysql+pymysql://3p4fdyCt9Bzwfkh.root:w38mCpM1dvOB8CGL@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/PROJECT?ssl_verify_cert=false"
engine = create_engine(db_url)

# Streamlit UI
st.title("Sales Data Analysis Dashboard")

# Sidebar for navigation
options = [
    "Top 10 High Revenue Items",
    "Top 5 Cities by Profit Margins",
    "Total Discount per Category",
    "Average Sale Price per Category",
    "Region with Highest Average Sale Price",
    "Total Profit per Category",
    "Top 3 High Quantity Order Segments",
    "Average Discount Percentage per Region",
    "Highest Profit Product Category",
    "Total Revenue per Year"
]

selection = st.sidebar.selectbox("Select Analysis", options)

# Query execution function
def fetch_data(query):
    return pd.read_sql(query, con=engine)

# Query dictionary
queries = {
    "Top 10 High Revenue Items": """
        SELECT sub_category, SUM(sale_price * quantity) AS calc_price 
        FROM sales_data 
        GROUP BY sub_category 
        ORDER BY calc_price DESC 
        LIMIT 10;
    """,
    "Top 5 Cities by Profit Margins": """
        SELECT city, SUM(profit) AS total_profit,
        (SUM(profit) / NULLIF(SUM(sale_price), 0)) * 100 AS profit_margin
        FROM sales_data 
        GROUP BY city 
        ORDER BY profit_margin DESC 
        LIMIT 5;
    """,
    "Total Discount per Category": """
        SELECT category, SUM(discount) AS total_discount 
        FROM sales_data 
        GROUP BY category 
        ORDER BY total_discount DESC;
    """,
    "Average Sale Price per Category": """
        SELECT category, AVG(sale_price) AS avg_sale_price 
        FROM sales_data 
        GROUP BY category 
        ORDER BY avg_sale_price DESC;
    """,
    "Region with Highest Average Sale Price": """
        SELECT region, AVG(sale_price) AS avg_sale_price 
        FROM sales_data 
        GROUP BY region 
        ORDER BY avg_sale_price DESC 
        LIMIT 1;
    """,
    "Total Profit per Category": """
        SELECT category, SUM(profit) AS total_profit 
        FROM sales_data 
        GROUP BY category 
        ORDER BY total_profit DESC;
    """,
    "Top 3 High Quantity Order Segments": """
        SELECT segment, SUM(quantity) AS total_quantity 
        FROM sales_data 
        GROUP BY segment 
        ORDER BY total_quantity DESC 
        LIMIT 3;
    """,
    "Average Discount Percentage per Region": """
        SELECT region, AVG(discount_percent) AS avg_discount_percentage 
        FROM sales_data 
        GROUP BY region 
        ORDER BY avg_discount_percentage DESC;
    """,
    "Highest Profit Product Category": """
        SELECT category, SUM(profit) AS total_profit 
        FROM sales_data 
        GROUP BY category 
        ORDER BY total_profit DESC 
        LIMIT 1;
    """,
    "Total Revenue per Year": """
        SELECT YEAR(order_date) AS year, SUM(sale_price * quantity) AS total_revenue 
        FROM sales_data 
        GROUP BY year 
        ORDER BY year ASC;
    """
}


with st.sidebar.expander("View SQL Query"):# Display the SQL query in the sidebar within an expander
    st.code(queries[selection], language='sql')

def fetch_data(query):
    return pd.read_sql(query, con=engine)

if selection in queries:
    df = fetch_data(queries[selection])
    st.subheader(selection)
    st.dataframe(df)
