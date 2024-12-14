import streamlit as st
import pg8000
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Connect to the database
def create_connection():
        connection = pg8000.connect(
            host="orders.ch2k6ywge94l.ap-south-1.rds.amazonaws.com",
            database="postgres",
            user="postgres",
            password="asdf1234567890",
            port="5432"
        )
        return connection
    
def run_query(query):
    connection=create_connection()
    if connection is None:
        return None
    try:
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        connection.close()
    
# Streamlit app for running SQL queries
def main():
    st.sidebar.title("Retail Order Data Analysis ")

guvi_queries = {
    "Top 10 highest revenue generating products": 
        'select sub_category, sum(sale_price*quantity) as total_revenue from orders group by sub_category order by total_revenue desc limit 10;',
    "Top 5 cities with the highest profit margins": 
        'select city, sum((sale_price-cost_price)/sale_price)*100 as total_profit from orders where sale_price>0 group by city order by total_profit desc limit 5;',
    "Total discount given for each category": 
        'select sub_category,sum(discount) as total_discount from orders group by sub_category order by total_discount desc;',
    "Average sales price per product category": 
        'select category, avg(sale_price) as average_sale_price from orders group by category order by average_sale_price desc;',
    "The highest average sale price":
        'select region, avg(sale_price) as average_sale_price from orders group by region order by average_sale_price desc limit 1;',
    "Total profit per category": 
        'select category, sum(profit) as total_profit from orders group by category order by total_profit desc;',
    "Top 3 segments with the highest quantity of orders": 
        'select segment,sum(quantity) as total_quantity from orders group by segment order by total_quantity desc limit 3',
    "Average discount percentage given per region": 
        'select region,avg(discount_percent) as avg_discount_per from orders group by region order by avg_discount_per desc;',
    "Product category with the highest total profit": 
        'select sub_category, sum(profit) as total_profit from orders group by sub_category order by total_profit desc;',
    "Total revenue generated per year": 
        'select extract (YEAR FROM order_date::DATE) as sale_year, sum(sale_price) as total_revenue from orders group by sale_year order by total_revenue desc;',

}

my_queries={
    "1. Top 5 Products with the Highest Quantity of Orders": """
        SELECT o.product_id, COUNT(o.order_id) AS total_orders
        FROM orders o
        GROUP BY o.product_id
        ORDER BY total_orders DESC
        LIMIT 5;
    """,

    "2. Total Revenue by Region": """
        SELECT o.region, SUM(o.sale_price) AS total_revenue
        FROM orders o
        GROUP BY o.region
        ORDER BY total_revenue DESC;
    """,

    "3. Product Categories with the Most Orders": """
        SELECT o.category, COUNT(o.order_id) AS total_orders
        FROM orders o
        GROUP BY o.category
        ORDER BY total_orders DESC;
    """,

    "4. Average Profit per Order by Region": """
        SELECT o.region, AVG(o.profit) AS avg_profit
        FROM orders o
        GROUP BY o.region
        ORDER BY avg_profit DESC;
    """,

    "5. Top 3 Regions with the Most Discounted Sales": """
        SELECT o.region, SUM(o.discount) AS total_discount
        FROM orders o
        WHERE o.discount > 0
        GROUP BY o.region
        ORDER BY total_discount DESC
        LIMIT 3;
    """,

    "6. Total Profit by Product ID per Year": """
        SELECT o.product_id, EXTRACT(YEAR FROM order_date::timestamp) AS year, SUM(o.profit) AS total_profit
        FROM orders o
        GROUP BY o.product_id, year
        ORDER BY year, total_profit DESC;
    """,

    "7. Total Sales by Product Category and Region": """
        SELECT o.category, o.region, SUM(o.sale_price) AS total_sales
        FROM orders o
        GROUP BY o.category, o.region
        ORDER BY total_sales DESC;
    """,

    "8. Year-over-Year Profit Growth for Each Region": """
        SELECT o.region, 
               EXTRACT(YEAR FROM order_date::timestamp) AS year, 
               SUM(o.profit) AS total_profit,
               SUM(o.profit) - LAG(SUM(o.profit)) OVER (PARTITION BY o.region ORDER BY EXTRACT(YEAR FROM order_date::timestamp)) AS profit_growth
        FROM orders o
        GROUP BY o.region, year
        ORDER BY o.region, year;
    """,

    "9. Top 10 Products with the Highest Discounts": """
        SELECT o.product_id, SUM(o.discount) AS total_discount
        FROM orders o
        GROUP BY o.product_id
        ORDER BY total_discount DESC
        LIMIT 10;
    """,

    "10. Total Revenue by Product ID and Category": """
        SELECT o.product_id, o.category, SUM(o.sale_price) AS total_revenue
        FROM orders o
        GROUP BY o.product_id, o.category
        ORDER BY total_revenue DESC;
    """
}


# Navigation options
nav = st.sidebar.radio("Select Query Section",["Guvi Queries" , "My Queries"])

# Query selection based on navigation
if nav == "Guvi Queries":
    st.subheader("Guvi Queries")
    query = st.selectbox("Select a query to visualize:", list(guvi_queries.keys()))
    selected_query_set = guvi_queries
elif nav == "My Queries":
    st.subheader("My Queries")
    query = st.selectbox("Select a query to visualize:", list(my_queries.keys()))
    selected_query_set = my_queries
else:
    query = None

# Execute and visualize selected query
if query:
    result_df = run_query(selected_query_set[query])
    if result_df is not None:
        st.dataframe(result_df)
