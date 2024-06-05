#Harsha's Stock DashBoard Project:
#----import the necessary libraries----#
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import time
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
def display_typing_text(text, speed=0.1):
    placeholder = st.empty()
    typing_text = ""
    for char in text:
        typing_text += char
        placeholder.markdown(
            f"<div style='text-align: center; font-size: 40px; color: #ff6347; font-weight: bold;'>"
            f"<span style='font-size: 44px; color: white'>{typing_text[:6]}</span>{typing_text[6:]}<span style='font-size: 44px;'>{typing_text[28:]}</span></div>",
            unsafe_allow_html=True,
        )
        time.sleep(speed)

# @Streamlit for Webapplication development
# Title---
st.markdown("""
    <h1 style='text-align: center;'>
        <span style='color: #ff6347; font-size: 1.65em;'>Baleyg</span> - 
        Market Analyzer
    </h1>""", unsafe_allow_html=True)
st.markdown("""
    <style>
        .welcome-container {
            width: 100%;
            padding-left: 10px;
            padding-right: 10px;
        }
        .welcome-text {
            font-size: 1.2em;
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            text-align: left;
        }
        .highlight {
            color: #ff6347;
            font-weight: bold;
        }
    </style>
    <div class="welcome-container">
        <div class="welcome-text">
            Welcome to <span class="highlight">Baleyg</span>! Your one-stop destination for market data, 
            <span class="highlight">Analyze</span> and <span class="highlight">Visualize </span>Stock Information like never before. 
            Browse through our wide range of <span class="highlight">Technical indicators</span>, read through the 
            <span class="highlight">Fundamental Statements</span> and Keep Up-to-Date with our 
            Personalised <span class="highlight">Market news</span>!
        </div>
    </div>
""", unsafe_allow_html=True)



# Sidebar
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date:')
end_date = st.sidebar.date_input('End Date:')

# I have created a personal section for giving my information here-- feel free to change it as per your requirement:
st.sidebar.markdown("<h4 style='color: #ff6347;'>My Information</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<span style='color: #ff6347;'>**Name:**</span> Jonnalagadda Sri Harsha", unsafe_allow_html=True)
st.sidebar.markdown("<span style='color: #ff6347;'>**Education:**</span> IInd year CSE Data Science", unsafe_allow_html=True)
st.sidebar.markdown("<span style='color: #ff6347;'>**Location:**</span> Chennai, India", unsafe_allow_html=True)
st.sidebar.write("This dashboard aims to provide users with a comprehensive tool for analyzing stock market data. I've taken up this project as a challenge to develop a user-friendly web application for effective market analysis.")

# Check if ticker symbol is provided
if ticker:
    # Proceed with fetching data only if ticker is provided
    data = yf.download(ticker, start=start_date, end=end_date)

    if not data.empty:
        # Display price chart and other sections
        st.markdown("<h2 style='color: #ff6347;'>Price Chart</h2>", unsafe_allow_html=True)
        # Two representations: line and candlestick
        l_chart, b_chart = st.tabs(["Line Chart", "Candle-stick Pattern"])
        with l_chart:
            fig = px.line(data, x=data.index, y='Adj Close', title=ticker)
            st.plotly_chart(fig)
        with b_chart:
            fig_candlestick = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
            fig_candlestick.update_layout(title=ticker, xaxis_title='Date', yaxis_title='Price')
            st.plotly_chart(fig_candlestick)

        # Technical Analysis
        import pandas_ta as ta
        st.markdown("<h3 style='color: #ff6347;'>Technical Analysis</h3>", unsafe_allow_html=True)
        st.write("Explore various technical indicators and metrics to analyze the price action and trends. You can select different technical indicators from the dropdown menu below to visualize how they correlate with the stock's price movements.")
        df = pd.DataFrame()
        ind_list = df.ta.indicators(as_list=True)
        technical_indicator = st.selectbox('Technical Indicator', options=ind_list)
        method = technical_indicator
        indicator = pd.DataFrame(getattr(ta, method)(low=data['Low'], close=data['Close'], high=data['High'], open=data['Open'], volume=data['Volume']))
        indicator['Close'] = data['Close']
        figW_ind_new = px.line(indicator)
        st.plotly_chart(figW_ind_new)

        # Tabulations & Stock Related Data
        pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top News"])
        with pricing_data:
            st.markdown("<h3 style='color: #ff6347;'>Price Movement</h3>", unsafe_allow_html=True)
            data_change = data.copy()
            data_change['% Change'] = data['Adj Close'].pct_change()
            # Since the first column would come as NA value--
            data_change = data_change.fillna(0)
            st.write(data_change) 
            annual_return = data_change['% Change'].mean() * 252 * 100
            st.write('Annual Return:', annual_return, '%')
            sd = np.std(data_change['% Change']) * np.sqrt(252)
            st.write('Standard Deviation:', sd * 100, '%')
            st.write('Risk Adj. Return:', annual_return / (sd * 100))

        # Fundamental Data - API alpha vantage
        from alpha_vantage.fundamentaldata import FundamentalData   
        with fundamental_data:
            key = '350OBOZ7YUVFGMAY'
            fd = FundamentalData(key, output_format='pandas')
            st.markdown("<h3 style='color: #ff6347;'>Balance Sheet</h3>", unsafe_allow_html=True)
            balance_sheet = fd.get_income_statement_annual(ticker)[0]
            bs = balance_sheet.T[2:]
            bs.columns = list(balance_sheet.T.iloc[0])
            st.write(bs)
            st.markdown("<h3 style='color: #ff6347;'>Income Statement</h3>", unsafe_allow_html=True)
            income_statement = fd.get_income_statement_annual(ticker)[0]
            is1 = income_statement.T[2:]
            is1.columns = list(balance_sheet.T.iloc[0])
            st.write(is1)
            st.markdown("<h3 style='color: #ff6347;'>Cash Flow Statements</h3>", unsafe_allow_html=True)
            cash_statement = fd.get_cash_flow_annual(ticker)[0]
            cf = cash_statement.T[2:]
            cf.columns = list(cash_statement.T.iloc[0])
            st.write(cf)

        # News Tab
        from stocknews import StockNews
        with news:
            st.markdown("<h2 style='color: #ff6347;'>Related News Articles</h2>", unsafe_allow_html=True)
            sn = StockNews(ticker, save_news=False)
            df_news = sn.read_rss()
            for i in range(5):
                st.subheader(df_news['title'][i])
                st.write(df_news['published'][i])
                st.write(df_news['summary'][i])
        #forecasting stock movement       
        from datetime import date
        from prophet import Prophet
        from prophet.plot import plot_plotly
        from plotly import graph_objs as go
        st.markdown("<h2 style='color: #ff6347;'>Stock Movement Forecasting</h2>", unsafe_allow_html=True)
        st.markdown("<h4>The stock market is known for being volatile, dynamic, and nonlinear. Accurate stock price prediction is extremely challenging because of multiple (macro and micro) factors</h4>", unsafe_allow_html=True)
        selected_stocks = ticker
        n_years = st.slider("Years of Preditiction: ",1,5)
        period = n_years * 365
        st.markdown("<h3 style='color: #ff6347;'>Stock Forecast</h3>", unsafe_allow_html=True)
        df_train = data.reset_index()[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date":"ds","Close":"y"})
        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)
        fig_forecast = plot_plotly(m,forecast)
        st.write('forecast the future value of an individual stock, a particular sector or the market, or the market as a whole. Yearly and weekly movement of particular stock:')
        fig2 = m.plot_components(forecast)
        st.write(fig2)  
    else:
        st.error("Select Different Start & End Date (or) Please enter a valid ticker symbol")
else:
    st.markdown("<h3 style='text-align: center; font-family: Consolas, monospace;'>.....</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-family: Consolas, monospace; font-size: 18px;'>This intuitive dashboard provides comprehensive tools for market data analysis.Evaluate the strengths, weaknesses, opportunities, and threats of stocks.Stay informed and make smarter investment decisions with Baleyg!</h3>", unsafe_allow_html=True)
    display_typing_text("Choose a valid Ticker Symbol")