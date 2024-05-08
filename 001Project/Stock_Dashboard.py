#Harsha's Stock DashBoard Project:
#----import the necessary libraries----#
import streamlit as st
import pandas as pd, numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
# @Streamlit for Webapplication development
#Title---
st.markdown("""
    <h1 style='text-align: center;'>
        <span style='color: #ff6347; font-size: 1.65em;'>Baleyg</span> - 
        <span style='color: white;'>Market Analyzer</span>
    </h1>""", unsafe_allow_html=True)
st.write("Welcome to Baleyg! Your one-stop destination for market data, Analyze and Visualize Stock Information like never before. Browse thorugh our wide range of technical indicators, read through the Fundamental Statements and Keep Up to Date with our personalised stock news!")
#Sidebar
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date:')
end_date = st.sidebar.date_input('End Date:')
if ticker:
    # I have created a personal section for giving my information here-- feel free to change it as per your requirement:
    st.sidebar.markdown("<h4 style='color: #ff6347;'>My Information</h4>", unsafe_allow_html=True)
    st.sidebar.markdown("<span style='color: #ff6347;'>**Name:**</span> Jonnalagadda Sri Harsha", unsafe_allow_html=True)
    st.sidebar.markdown("<span style='color: #ff6347;'>**Education:**</span> IInd year CSE Data Science", unsafe_allow_html=True)
    st.sidebar.markdown("<span style='color: #ff6347;'>**Location:**</span> Chennai, India", unsafe_allow_html=True)
    st.sidebar.write("This dashboard aims to provide users with a comprehensive tool for analyzing stock market data. I've taken up this project as a challenge to develop a user-friendly web application for effective market analysis.")


    #----- Getting Our Data & Price Charts-----#
    data = yf.download(ticker,start = start_date,end = end_date)
    st.markdown("<h2 style='color: #ff6347;'>Price Chart</h2>", unsafe_allow_html=True)
    #two representations lin and candle stick
    l_chart, b_chart = st.tabs(["Line Chart","Candle-stick Pattern"])
    with l_chart:
        fig = px.line(data, x = data.index, y = data['Adj Close'],title= ticker)
        st.plotly_chart(fig)
    with b_chart:
        fig_candlestick = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'],low=data['Low'], close=data['Close'])])
        fig_candlestick.update_layout(title=ticker, xaxis_title='Date', yaxis_title='Price')
        st.plotly_chart(fig_candlestick)
    
    #-------Technical Analysis-------#
    import pandas_ta as ta
    st.markdown("<h3 style='color: #ff6347;'>Technical Analysis</h3>", unsafe_allow_html=True)
    st.write("Explore various technical indicators and metrics to analyze the price action and trends.You can select different technical indicators from the dropdown menu below to visualize how they correlate with the stock's price movements.")
    df = pd.DataFrame()
    ind_list = df.ta.indicators(as_list= True)
    #st.write(ind_list)
    technical_indicator = st.selectbox('Technical Indicator',options=ind_list)
    method = technical_indicator
    indicator = pd.DataFrame(getattr(ta,method)(low=data['Low'],close=data['Close'],high=data['High'],open=data['Open'],volume=data['Volume']))
    indicator['Close'] = data['Close']
    figW_ind_new = px.line(indicator)
    st.plotly_chart(figW_ind_new)

    #-------Tabulations & Stock Related Data-------#
    pricing_data, fundamental_data, news = st.tabs(["Pricing Data","Fundamental Data","Top News"])
    with pricing_data:
        st.markdown("<h3 style='color: #ff6347;'>Price Movement</h3>", unsafe_allow_html=True)
        data_change = data
        data_change['% Change'] = data['Adj Close']/data['Adj Close'].shift(1) - 1
        #since the first column would come as NA value--
        data_change.fillna('-')
        st.write(data_change) 
        annual_return = data_change['% Change'].mean()*252*100
        st.write('Annual Return:',annual_return,'%')
        sd = np.std(data_change['% Change'])*np.sqrt(252)
        st.write('Standard Deviation:',sd*100,'%')
        st.write('Risk Adj. Return:',annual_return/(sd*100))

    #Fundamental Data - API alpha vantage
    from alpha_vantage.fundamentaldata import FundamentalData   
    with fundamental_data:
        key = '350OBOZ7YUVFGMAY'
        fd = FundamentalData(key,output_format = 'pandas')
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
    
    #News Tab
    from stocknews import StockNews
    with news:
        st.markdown("<h2 style='color: #ff6347;'>Related News Articles</h2>", unsafe_allow_html=True)
        sn = StockNews(ticker,save_news=False)
        df_news = sn.read_rss()
        for i in range(5):
            st.subheader(df_news['title'][i])
            st.write(df_news['published'][i])
            st.write(df_news['summary'][i])
else:
    st.error('Enter A Valid Ticker Symbol')
