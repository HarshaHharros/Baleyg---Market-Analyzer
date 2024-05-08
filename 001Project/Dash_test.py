#Harsha's Stock DashBoard Project

#This is my personal Initial code
# I've added this to the repository to provide a general understanding of the code
# as this is comparatively simple because it lacks text styling and tab charts


import streamlit as st
import pandas as pd, numpy as np
import yfinance as yf
import plotly.express as px
# @Streamlit for Webapplication development

st.title('Baleyg - One Stop for Market Data')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date:')
end_date = st.sidebar.date_input('End Date:')

#----- Getting Our Data -----#
data = yf.download(ticker,start = start_date,end = end_date)
st.header('Price Chart')
fig = px.line(data, x = data.index, y = data['Adj Close'],title= ticker)
st.plotly_chart(fig)
#-------Technical Analysis-------#
import pandas_ta as ta
st.subheader('Technical Analysis')
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
    st.header('Price Movements')
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

#Fundamental Data   
from alpha_vantage.fundamentaldata import FundamentalData   
with fundamental_data:
    key = '350OBOZ7YUVFGMAY'
    fd = FundamentalData(key,output_format = 'pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_income_statement_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns = list(balance_sheet.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cash_statement = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_statement.T[2:]
    cf.columns = list(cash_statement.T.iloc[0])
    st.write(cf)
#News Tab
from stocknews import StockNews
with news:
    st.header('Related News Articles')
    sn = StockNews(ticker,save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(df_news['title'][i])
        st.write(df_news['published'][i])
        st.write(df_news['summary'][i])
    
    