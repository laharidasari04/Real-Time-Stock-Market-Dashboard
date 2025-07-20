# 📈 Real-Time Stock Market Dashboard

A comprehensive, real-time stock market dashboard built with Python, Streamlit, and Plotly. This application provides live stock data visualization, technical analysis indicators, and company information for popular stocks.

## 🚀 Features

### 📊 Real-Time Data
- Live stock price updates using Yahoo Finance API
- Current price, volume, and market cap information
- Price change tracking with percentage calculations

### 📈 Technical Analysis
- **Candlestick Charts**: OHLC (Open, High, Low, Close) visualization
- **Moving Averages**: 20-day, 50-day, and 200-day moving averages
- **Bollinger Bands**: Upper and lower bands for volatility analysis
- **RSI (Relative Strength Index)**: Momentum oscillator (0-100 scale)
- **MACD (Moving Average Convergence Divergence)**: Trend-following momentum indicator
- **Volume Analysis**: Trading volume with color-coded bars

### 🏢 Company Information
- Business summary and sector information
- Industry classification and company details
- Website and employee count
- Financial metrics (P/E ratio, market cap)

### ⚙️ Interactive Features
- Stock selection from popular companies
- Multiple time period options (1d to 10y)
- Auto-refresh capability (every 30 seconds)
- Responsive design with modern UI

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **yfinance**: Yahoo Finance API wrapper
- **NumPy**: Numerical computations

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection for real-time data

## 🚀 Installation & Setup

### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd stock-market-dashboard

# Or download and extract the ZIP file
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run stock_dashboard.py
```

### 4. Access the Dashboard
Open your web browser and navigate to:
```
http://localhost:8501
```

## 📖 How to Use

### 1. Stock Selection
- Use the sidebar to select from popular stocks
- Available stocks include: AAPL, GOOGL, MSFT, AMZN, TSLA, META, NVDA, NFLX, JPM, JNJ

### 2. Time Period Selection
- Choose from various time periods:
  - 1d, 5d: Short-term analysis
  - 1mo, 3mo, 6mo: Medium-term analysis
  - 1y, 2y, 5y, 10y: Long-term analysis
  - ytd: Year-to-date
  - max: Maximum available data

### 3. Auto-Refresh
- Enable auto-refresh for real-time updates
- Data refreshes every 30 seconds when enabled

### 4. Interpreting Charts

#### Candlestick Chart
- **Green candles**: Close price > Open price (bullish)
- **Red candles**: Close price < Open price (bearish)
- **Wicks**: Show high and low prices for the period

#### Technical Indicators
- **RSI**: 
  - Above 70: Overbought condition
  - Below 30: Oversold condition
- **MACD**: 
  - Positive values: Bullish momentum
  - Negative values: Bearish momentum
- **Bollinger Bands**: 
  - Price near upper band: Potential overbought
  - Price near lower band: Potential oversold

## 📊 Available Stocks

| Symbol | Company Name |
|--------|--------------|
| AAPL   | Apple Inc. |
| GOOGL  | Alphabet Inc. |
| MSFT   | Microsoft Corporation |
| AMZN   | Amazon.com Inc. |
| TSLA   | Tesla Inc. |
| META   | Meta Platforms Inc. |
| NVDA   | NVIDIA Corporation |
| NFLX   | Netflix Inc. |
| JPM    | JPMorgan Chase & Co. |
| JNJ    | Johnson & Johnson |

## 🔧 Customization

### Adding New Stocks
To add more stocks, modify the `popular_stocks` dictionary in `stock_dashboard.py`:

```python
popular_stocks = {
    "AAPL": "Apple Inc.",
    "GOOGL": "Alphabet Inc.",
    # Add your preferred stocks here
    "YOUR_SYMBOL": "Your Company Name"
}
```

### Modifying Time Periods
Adjust the available time periods in the sidebar:

```python
time_period = st.sidebar.selectbox(
    "Select time period:",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    index=5
)
```

### Customizing Technical Indicators
Modify the `calculate_indicators()` function to add or adjust technical indicators.

## 🐛 Troubleshooting

### Common Issues

1. **"Error fetching data" message**
   - Check your internet connection
   - Verify the stock symbol is valid
   - Yahoo Finance API might be temporarily unavailable

2. **Slow loading times**
   - Reduce the time period selection
   - Disable auto-refresh if not needed
   - Check your internet speed

3. **Missing data**
   - Some stocks may have limited data availability
   - Try a different time period
   - Check if the stock is actively traded

### Performance Tips

- Use shorter time periods for faster loading
- Disable auto-refresh when not actively monitoring
- Close other browser tabs to free up memory

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the error messages in the terminal
3. Ensure all dependencies are properly installed

## 🔮 Future Enhancements

Potential features for future versions:
- Portfolio tracking and management
- Multiple stock comparison
- News sentiment analysis
- Alert notifications
- Export functionality
- Mobile-responsive design improvements
- Additional technical indicators
- Historical data export

---

**Disclaimer**: This dashboard is for educational and informational purposes only. It should not be considered as financial advice. Always do your own research and consult with financial professionals before making investment decisions. 