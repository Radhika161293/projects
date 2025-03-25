import pandas as pd

from sqlalchemy import create_engine
db_url = "mysql+pymysql://3p4fdyCt9Bzwfkh.root:w38mCpM1dvOB8CGL@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/PROJECT?ssl_verify_cert=false"

engine = create_engine(db_url)



def myfunction():
    print("hello")
    df = pd.read_csv('orders.csv')

    new_df = df.dropna()#to drop null values

    # print(new_df.to_string())
    df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)# to rename col names if space is found
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)# trim text fields if there is spaces
    df["discount"] = df["list_price"] * df["discount_percent"] / 100  # Calculate discount
    df["sale_price"] = df["list_price"] - df["discount"]  # Sale price
    df["profit"] = df["sale_price"] - df["cost_price"]  # Profit
    # df.to_sql("sales_data", con=engine, if_exists="replace", index=False)
    df.to_sql("sales_data", con=engine, if_exists="replace", index=False)



#1.top 10 highest revenue generating items
query = """  SELECT sub_category, 
SUM(sale_price * quantity) AS calc_price FROM sales_data
GROUP BY sub_category
ORDER BY calc_price DESC;
"""
df_highrev_products= pd.read_sql(query, con=engine)
print(df_highrev_products)#have displayed the first 10 high revenue prods
#2 Find the top 5 cities with the highest profit margins
query = """
    SELECT city,SUM(profit) AS total_profit,
    (SUM(profit) / NULLIF(SUM(sale_price), 0)) * 100 AS profit_margin
    FROM sales_data
    GROUP BY city
    ORDER BY profit_margin DESC
    LIMIT 5;
    """
df_top_cities = pd.read_sql(query, con=engine)
#print("\n Top 5 Cities with the Highest Profit Margins:")
print(df_top_cities)
#3.disc for each category
query = """
    SELECT category, SUM(discount) AS total_discount
    FROM sales_data
    GROUP BY category
    ORDER BY total_discount DESC;
    """
df_discount = pd.read_sql(query, con=engine)
print(df_discount)
#4. Find the average sale price per product category
query = """
    SELECT category,
    AVG(sale_price) AS avg_sale_price
    FROM sales_data
    GROUP BY category
    ORDER BY avg_sale_price DESC;
    """
    
df_avg_price = pd.read_sql(query, con=engine)
print(df_avg_price)
#5.Find the region with the highest average sale price
query = """
    SELECT region, AVG(sale_price) AS avg_sale_price
    FROM sales_data
    GROUP BY region
    ORDER BY avg_sale_price DESC
    LIMIT 1;
    """
df_regionhigh = pd.read_sql(query, con=engine)
print(df_regionhigh)
#6.Find the total profit per category
query = """
    SELECT category, SUM(profit) AS total_profit
    FROM sales_data
    GROUP BY category
    ORDER BY total_profit DESC;
    """
df_profit_per_category = pd.read_sql(query, con=engine)
print(df_profit_per_category)
#7.high quantity orders
query = """
    SELECT segment, SUM(quantity) AS total_quantity
    FROM sales_data
    GROUP BY segment
    ORDER BY total_quantity DESC
    LIMIT 3;
    """
df_top_segments = pd.read_sql(query, con=engine)
print(df_top_segments)
#8.Determine the average discount percentage given per region
query = """
    SELECT region, AVG(discount_percent) AS avg_discount_percentage
    FROM sales_data
    GROUP BY region
    ORDER BY avg_discount_percentage DESC;
    """
df_avg_discount = pd.read_sql(query, con=engine)
print(df_avg_discount)
#9. Find the product category with the highest total profit
query = """
    SELECT category,SUM(profit) AS total_profit
    FROM sales_data
    GROUP BY category
    ORDER BY total_profit DESC
    LIMIT 1;
    """
df_highest_profit = pd.read_sql(query, con=engine)
print(df_highest_profit)
#10.Calculate the total revenue generated per year
query = """
    SELECT YEAR(order_date) AS year,SUM(sale_price * quantity) AS total_revenue
    FROM sales_data
    GROUP BY year
    ORDER BY year ASC;
    """
df_total_revenue=pd.read_sql(query,con=engine)
print(df_total_revenue)
# Total Sales per Product Category:

query= """
SELECT DATE_FORMAT(sd.order_date, '%Y-%m') AS month, SUM(sd.sale_price * sd.quantity) AS total_sales
FROM sales_data sd
GROUP BY month
ORDER BY month ASC;
"""
    
df_total_sales=pd.read_sql(query,con=engine)
print(df_total_sales)
    
    



