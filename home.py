import datetime
import streamlit as st
import pandas as pd
import numpy as np
import pandas_datareader as web

st.title("📈 Stock Performance Viewer")

# -- Fetch stock data from stooq API --
def get_stock_data(symbol, start_date, end_date):
    st.toast('📡 Fetching stock data...')
    try:
        df = web.DataReader(symbol, 'stooq', start=start_date, end=end_date)

        if df.empty:
            st.toast("⚠️ No data found. Check symbol or date range.")
            st.error("Empty or invalid data received.")
            return None

        df = (
            df[["Close"]]
            .rename(columns={"Close": "price"})
            .sort_index(ascending=False)
        )
        df["return(%)"] = np.log(df["price"]).diff() * 100

        st.toast("✅ Data ready!", icon="📊")
        return df

    except Exception as e:
        st.toast("❌ Failed to fetch data")
        st.error(f"Error: {e}")
        return None


# -- Plot charts for price and return --
def plot_price_and_return(df):
    st.subheader("📉 Price and Log Return")
    st.line_chart(df[["price"]], x_label="Date", color=["#7cc1b8"])
    st.line_chart(df[["return(%)"]], x_label="Date", color=["#c17ca8"])


# -- User input section --
symbol = st.text_input("🔍 Enter Stock or Index Symbol (e.g., AAPL)")

today = datetime.date.today()
start_default = datetime.date(today.year - 1, 1, 1)

start_date = st.date_input("Start Date", start_default, format="YYYY-MM-DD")
end_date = st.date_input("End Date", today, format="YYYY-MM-DD")

# -- Trigger data fetch and plot --
if st.button("Get Data", icon="📥"):
    df = get_stock_data(symbol, start_date, end_date)
    if df is not None:
        st.write(f"Showing results for: **{symbol.upper()}**")
        st.dataframe(df)
        plot_price_and_return(df)
