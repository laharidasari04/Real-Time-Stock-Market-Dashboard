import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
import time
from config import *

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Custom CSS for better styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📈 Real-Time Stock Market Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for stock selection
st.sidebar.header("📊 Stock Selection")

# Popular stocks list
popular_stocks = POPULAR_STOCKS

# Stock selection
selected_stock = st.sidebar.selectbox(
    "Select a stock:",
    list(popular_stocks.keys()),
    format_func=lambda x: f"{x} - {popular_stocks[x]}"
)

# Time period selection
time_period = st.sidebar.selectbox(
    "Select time period:",
    TIME_PERIODS,
    index=DEFAULT_TIME_PERIOD_INDEX
)

# Auto-refresh option
auto_refresh = st.sidebar.checkbox(f"🔄 Auto-refresh (every {AUTO_REFRESH_INTERVAL} seconds)", value=DEFAULT_AUTO_REFRESH)

# Function to get stock data
@st.cache_data(ttl=CACHE_TTL)
def get_stock_data(symbol, period):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info
    except Exception as e:
        # Check for 429 error
        if '429' in str(e) or 'Too Many Requests' in str(e):
            st.error(f"Yahoo Finance is rate-limiting requests (Error 429: Too Many Requests).\n\nPlease wait a few minutes before trying again. Avoid rapid refreshes or switching stocks too quickly.\n\nFor heavy use, consider a paid data API.")
        else:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None, None

# Function to calculate technical indicators
def calculate_indicators(df):
    if df is None or df.empty:
        return df
    
    # Moving averages
    for period in MA_PERIODS:
        df[f'MA{period}'] = df['Close'].rolling(window=period).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=RSI_PERIOD).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=RSI_PERIOD).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['Close'].ewm(span=MACD_FAST, adjust=False).mean()
    exp2 = df['Close'].ewm(span=MACD_SLOW, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=MACD_SIGNAL, adjust=False).mean()
    
    # Bollinger Bands
    df['BB_middle'] = df['Close'].rolling(window=BB_PERIOD).mean()
    bb_std = df['Close'].rolling(window=BB_PERIOD).std()
    df['BB_upper'] = df['BB_middle'] + (bb_std * BB_STD)
    df['BB_lower'] = df['BB_middle'] - (bb_std * BB_STD)
    
    return df

# Function to create price chart
def create_price_chart(df, symbol):
    if df is None or df.empty:
        return None
    
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=(f'{symbol} Stock Price', 'Volume', 'RSI'),
        row_width=[0.6, 0.2, 0.2]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        ),
        row=1, col=1
    )
    
    # Moving averages
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MA20'], name='MA20', line=dict(color='orange')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MA50'], name='MA50', line=dict(color='blue')),
        row=1, col=1
    )
    
    # Bollinger Bands
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_upper'], name='BB Upper', 
                  line=dict(color='gray', dash='dash'), opacity=0.7),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_lower'], name='BB Lower', 
                  line=dict(color='gray', dash='dash'), opacity=0.7),
        row=1, col=1
    )
    
    # Volume
    colors = ['red' if close < open else 'green' for close, open in zip(df['Close'], df['Open'])]
    fig.add_trace(
        go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color=colors),
        row=2, col=1
    )
    
    # RSI
    fig.add_trace(
        go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple')),
        row=3, col=1
    )
    fig.add_hline(y=RSI_OVERBOUGHT, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=RSI_OVERSOLD, line_dash="dash", line_color="green", row=3, col=1)
    
    fig.update_layout(
        title=f'{symbol} Stock Analysis',
        xaxis_rangeslider_visible=False,
        height=CHART_HEIGHT,
        showlegend=True
    )
    
    return fig

# Function to create MACD chart
def create_macd_chart(df, symbol):
    if df is None or df.empty:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue'))
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['Signal'], name='Signal', line=dict(color='red'))
    )
    fig.add_trace(
        go.Bar(x=df.index, y=df['MACD'] - df['Signal'], name='MACD Histogram')
    )
    
    fig.update_layout(
        title=f'{symbol} MACD Indicator',
        xaxis_title='Date',
        yaxis_title='MACD',
        height=MACD_CHART_HEIGHT
    )
    
    return fig

# Main dashboard logic
def main():
    # Get stock data
    hist_data, stock_info = get_stock_data(selected_stock, time_period)
    
    if hist_data is not None and not hist_data.empty:
        # Calculate indicators
        hist_data = calculate_indicators(hist_data)
        
        # Get current price and change
        current_price = hist_data['Close'].iloc[-1]
        previous_price = hist_data['Close'].iloc[-2] if len(hist_data) > 1 else current_price
        price_change = current_price - previous_price
        price_change_pct = (price_change / previous_price) * 100
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Current Price",
                value=f"${current_price:.2f}",
                delta=f"{price_change:.2f} ({price_change_pct:.2f}%)"
            )
        
        with col2:
            if stock_info and 'marketCap' in stock_info:
                market_cap = stock_info['marketCap'] / 1e9  # Convert to billions
                st.metric("Market Cap", f"${market_cap:.2f}B")
            else:
                st.metric("Market Cap", "N/A")
        
        with col3:
            if stock_info and 'volume' in stock_info:
                volume = stock_info['volume']
                st.metric("Volume", f"{volume:,}")
            else:
                st.metric("Volume", "N/A")
        
        with col4:
            if stock_info and 'trailingPE' in stock_info:
                pe_ratio = stock_info['trailingPE']
                st.metric("P/E Ratio", f"{pe_ratio:.2f}")
            else:
                st.metric("P/E Ratio", "N/A")
        
        # Stock information
        if stock_info:
            st.subheader("📋 Company Information")
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                if 'longBusinessSummary' in stock_info:
                    st.write("**Business Summary:**")
                    st.write(stock_info['longBusinessSummary'])
                
                if 'sector' in stock_info:
                    st.write(f"**Sector:** {stock_info['sector']}")
                
                if 'industry' in stock_info:
                    st.write(f"**Industry:** {stock_info['industry']}")
            
            with info_col2:
                if 'website' in stock_info:
                    st.write(f"**Website:** {stock_info['website']}")
                
                if 'country' in stock_info:
                    st.write(f"**Country:** {stock_info['country']}")
                
                if 'employees' in stock_info:
                    st.write(f"**Employees:** {stock_info['employees']:,}")
        
        # Charts
        st.subheader("📊 Technical Analysis")
        
        # Price chart
        price_chart = create_price_chart(hist_data, selected_stock)
        if price_chart:
            st.plotly_chart(price_chart, use_container_width=True)
        
        # MACD chart
        macd_chart = create_macd_chart(hist_data, selected_stock)
        if macd_chart:
            st.plotly_chart(macd_chart, use_container_width=True)
        
        # Recent data table
        st.subheader("📋 Recent Price Data")
        recent_data = hist_data.tail(10)[['Open', 'High', 'Low', 'Close', 'Volume']]
        st.dataframe(recent_data, use_container_width=True)
        
        # Statistics
        st.subheader("📈 Statistics")
        stats_col1, stats_col2 = st.columns(2)
        
        with stats_col1:
            st.write("**Price Statistics:**")
            st.write(f"52-Week High: ${hist_data['High'].max():.2f}")
            st.write(f"52-Week Low: ${hist_data['Low'].min():.2f}")
            st.write(f"Average Volume: {hist_data['Volume'].mean():,.0f}")
        
        with stats_col2:
            st.write("**Technical Indicators:**")
            if 'RSI' in hist_data.columns:
                current_rsi = hist_data['RSI'].iloc[-1]
                st.write(f"Current RSI: {current_rsi:.2f}")
            if 'MACD' in hist_data.columns:
                current_macd = hist_data['MACD'].iloc[-1]
                st.write(f"Current MACD: {current_macd:.4f}")
    
    else:
        st.error("Unable to fetch stock data. Please check the stock symbol and try again.")
    
    # Auto-refresh functionality
    if auto_refresh:
        time.sleep(AUTO_REFRESH_INTERVAL)
        st.rerun()

# Run the main function
if __name__ == "__main__":
    main() 