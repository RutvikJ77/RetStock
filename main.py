import streamlit as st
import requests 
import yfinance as yf

Tickerdict = {"Gamestop":'GME',"Apple":'AAPL',"AMC Entertainment":'AMC',"Google":'GOOGL',"Microsoft":'MSFT'}
Duration = {"2 Weeks":'2wk',"1 Month":'1mo',"1 Year":'1y',"5 Years":'5y'}
st.title('RetStock')



st.markdown("## Retail Investment Analysis")

st.sidebar.header('Choose your company and duration')

selected_company = st.sidebar.selectbox("Select your company for analysis:",["Gamestop","Apple","AMC Entertainment","Google","Microsoft"])
tickerData = yf.Ticker(Tickerdict[selected_company])

day_range = st.sidebar.selectbox("Select Time duration for analysis:",["2 Weeks","1 Month","1 Year","5 Years"])


tickerDf = tickerData.history(period=Duration[day_range])
st.write("### " + selected_company + " Closing Price")
st.line_chart(tickerDf.Close)
