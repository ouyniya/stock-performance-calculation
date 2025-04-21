import datetime
import time
import streamlit as st
import pandas as pd
import numpy as np
import pandas_datareader as web
import yfinance as yf

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
            .sort_index(ascending=True)
        )

        df["return"] = np.log(df["price"]).diff()
        df["return_percentChange"] = df["price"].pct_change()

        st.toast("✅ Data ready!", icon="📊")
        return df

    except Exception as e:
        st.toast("❌ Failed to fetch data")
        st.error(f"Error: {e}")
        return None


# get cumulative return
def get_cumulative_return(df):
    try:
        cumulative_return = np.cumprod(df["return_percentChange"] + 1)
        # st.write(cumulative_return)
        # print(type(cumulative_return))
        cumulative_return = pd.DataFrame(cumulative_return)

        cumulative_return = (
            cumulative_return[["return_percentChange"]]
            .rename(columns={"return_percentChange": "Cumulative return"})
        )

        # print(type(cumulative_return))
        st.subheader("📉 Cumulative Return")
        st.line_chart(
            cumulative_return[["Cumulative return"]], x_label="Date", color=["#38a4cf"])
        return cumulative_return
    except Exception as e:
        st.error(f"Error: {e}")


# get key ratio
def get_key_ratio(symbol):

    if not symbol.strip():
        st.warning("⚠️ Please enter a valid stock symbol.")
        return
    try:
        st.divider()
        # Set the ticker
        ticker = yf.Ticker(symbol)
        info = ticker.info
        # fetch the latest price to book ratio and price to earnings ratio
        # Check if info is empty or missing the key
        if not info or 'priceToBook' not in info:
            st.error("❌ Data not available. Please check if the symbol is correct.")
            return

        # define other info
        displayName = info['displayName']
        longBusinessSummary = info['longBusinessSummary']
        industry = info['industry']
        sector = info['sector']

        # define ratio
        pb_ratio = info['priceToBook']
        priceToSalesTrailing12Months = info['priceToSalesTrailing12Months']
        debtToEquity = info['debtToEquity']
        trailingAnnualDividendYield = info['trailingAnnualDividendYield']
        trailingPegRatio = info['trailingPegRatio']
        priceEpsCurrentYear = info['priceEpsCurrentYear']

        # define trading data
        symbol = info['symbol']
        shortName = info['shortName']
        market = info['market']
        financialCurrency = info['financialCurrency']
        fullExchangeName = info['fullExchangeName']
        exchangeTimezoneName = info['exchangeTimezoneName']
        averageDailyVolume3Month = info['averageDailyVolume3Month']
        averageDailyVolume3Month = "{:0,.2f}".format(float(averageDailyVolume3Month))

        epsCurrentYear = info['epsCurrentYear']
        fiftyDayAverageChangePercent = info['fiftyDayAverageChangePercent']
        twoHundredDayAverageChangePercent = info['twoHundredDayAverageChangePercent']
        fiftyTwoWeekChangePercent = info['fiftyTwoWeekChangePercent']
        averageAnalystRating = info['averageAnalystRating']


        # display data
        st.success(f"Stock: {displayName}")

        on = st.toggle("Show/Hide Description: ")
        if on:
            with st.container(border=True):
                st.write(longBusinessSummary)

        st.write(f"**Industry:** {industry}")
        st.write(f"**Sector:** {sector}")

        # Financial Ratios
        st.subheader("📊 Financial Ratios")
        fn_data = {
            "P/E": [priceEpsCurrentYear],
            "P/S": [priceToSalesTrailing12Months],
            "P/B": [pb_ratio],
            "Trailing Peg Ratio": [trailingPegRatio],
            "D/E": [debtToEquity],
            "Trailing Dividend Yield": [trailingAnnualDividendYield]
        }

        fn_df = pd.DataFrame(fn_data)
        # print(fn_df)
        st.write(fn_df)


        # Trading data
        st.subheader("📈 Trading data")

        right, left = st.columns(2, border=True)

        with right:
            st.write(f"**Symbol:** {symbol}")
            st.write(f"**Short Name:** {shortName}")
            st.write(f"**Market:** {market}")
            st.write(f"**Currency:** {financialCurrency}")
            st.write(f"**Exchange Name:** {fullExchangeName}")
            st.write(f"**Exchange Timezone:** {exchangeTimezoneName}")
            st.write(f"**Average Daily Volume - 3Month:** {financialCurrency} {averageDailyVolume3Month}")

        with left:
            st.write(f"**EPS Current Year:** {epsCurrentYear}")
            st.write(f"**50 Day Average %Change:** {fiftyDayAverageChangePercent}")
            st.write(f"**200 Day Average %Change:** {twoHundredDayAverageChangePercent}")
            st.write(f"**52 Weeks %Change:** {fiftyTwoWeekChangePercent}")
            st.write(f"**Average Analyst Rating:** {averageAnalystRating}")

    except Exception as e:
        st.error(f"🔴 Error fetching data: {e}")

# -- Plot charts for price and return --


def plot_price_and_return(df):
    st.subheader("📉 Price")
    st.line_chart(df[["price"]], x_label="Date", color=["#7cc1b8"])

    st.subheader("📉 Log Return")
    st.line_chart(df[["return"]], x_label="Date", color=["#c17ca8"])


# -- User input section --
symbol = st.text_input("🔍 Enter Stock or Index Symbol (e.g., AAPL)")

today = datetime.date.today()
start_default = datetime.date(today.year - 1, 1, 1)

start_date = st.date_input("Start Date", start_default, format="YYYY-MM-DD")
end_date = st.date_input("End Date", today, format="YYYY-MM-DD")


# -- Key ratio --
get_key_ratio(symbol)

# -- Trigger data fetch and plot --
if st.button("Stock Analysis", icon="📥"):
    df = get_stock_data(symbol, start_date, end_date)
    if df is not None:
        st.write(f"Showing results for: **{symbol.upper()}**")
        # st.dataframe(df)
        print(df.info())

        # cumulative return graph
        cum_df = get_cumulative_return(df)

        # period of data
        st.write(f"Period: {cum_df.index.min().strftime('%Y-%m-%d')} to {cum_df.index.max().strftime('%Y-%m-%d')}")
            
        # total no of trading days
        days = len(cum_df)

        # annualised return
        # 1y = 252 trading days
        ann_return = cum_df.iloc[-1]
        print(f"cum_df.iloc[-1]: {ann_return}")
        print(f"days: {days}")
        ann_return = (cum_df.iloc[-1] ** (252/days) - 1) * 100
    
        # annualised volatility
        ann_sd = np.std(df['return_percentChange']) * (252 ** 0.5) * 100



        # sharpe ratio
        # assume an avg annual risk-free rate is 1%
        risk_free_rate = 0.01 / 252
        sharpe_ratio = np.sqrt(252) * (np.mean(df['return_percentChange'])) / np.std(df['return_percentChange'])

        # maximum drawdown
        peak = np.maximum.accumulate(cum_df.dropna())
        peak[peak < 1] = 1

        drawdown = (cum_df) / peak - 1
        max_dd = drawdown.min() * 100

        # Sortino ratio

        # Beta


    # header
    st.subheader("📉 Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Annualized Return", f"{ann_return.iloc[0].round(2)}%")
    col2.metric("Annualized volatility", f"{ann_sd.round(2)}%")
    col3.metric("Shape Ratio", f"{sharpe_ratio.round(2)}")
    col4.metric("Maximum Drawdown", f"{max_dd.iloc[0].round(2)}%")
