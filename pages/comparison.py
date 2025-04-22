import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_tags import st_tags
import datetime

st.title('Stock Comparison')
# 0983254077

# -- input --
st_stocks = st_tags(label="Enter stock (Max 5 stocks)",
                    text="Press enter to add more",
                    value=['AAPL', 'IBM', 'MSFT'],
                    maxtags=5)


today = datetime.date.today()
start_default = datetime.date(today.year - 1, 1, 1)

start_date = st.date_input("Start Date", start_default, format="YYYY-MM-DD")
end_date = st.date_input("End Date", today, format="YYYY-MM-DD")

def generate_graph(st_stocks, start_date, end_date):
    st.subheader('Cumulative performance')

    ticker_list = st_stocks
    data = pd.DataFrame(columns=ticker_list)
    
    for ticker in ticker_list:
        data[ticker] = yf.download(
            ticker, start_date, end_date, auto_adjust=True)['Close']
        data[ticker] = data[ticker].pct_change()
        data[ticker] = np.cumprod(data[ticker] + 1)
        
        # st.write(f"{ticker}: {((data[ticker].iloc[-1] - 1) * 100).round(2)}%")

    # -- plot --
    st.line_chart(data)

    final_return = (data.iloc[-1, :] - 1).round(5) * 100 
    final_return.name = "Return (%)"
    st.write(final_return)
    st.write(f"Period: {start_date} to {end_date}")


# button to run stock analysis
if st.button("get data", icon=":material/mood:"):
    generate_graph(st_stocks, start_date, end_date)







