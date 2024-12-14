import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Connect to the database
def create_connection():
        connection = psycopg2.connect(
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

my_queries={}
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
