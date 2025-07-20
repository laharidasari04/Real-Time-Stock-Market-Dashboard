# Configuration file for Real-Time Stock Market Dashboard

# Popular stocks configuration
POPULAR_STOCKS = {
    "AAPL": "Apple Inc.",
    "GOOGL": "Alphabet Inc.",
    "MSFT": "Microsoft Corporation",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc.",
    "META": "Meta Platforms Inc.",
    "NVDA": "NVIDIA Corporation",
    "NFLX": "Netflix Inc.",
    "JPM": "JPMorgan Chase & Co.",
    "JNJ": "Johnson & Johnson"
}

# Time periods available
TIME_PERIODS = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]

# Default time period index (1y = index 5)
DEFAULT_TIME_PERIOD_INDEX = 5

# Auto-refresh settings
AUTO_REFRESH_INTERVAL = 30  # seconds
DEFAULT_AUTO_REFRESH = False

# Chart settings
CHART_HEIGHT = 800
MACD_CHART_HEIGHT = 400

# Technical indicator settings
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
MA_PERIODS = [20, 50, 200]
BB_PERIOD = 20
BB_STD = 2

# RSI overbought/oversold levels
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# Data cache settings
CACHE_TTL = 30  # seconds

# Page configuration
PAGE_CONFIG = {
    "page_title": "Real-Time Stock Market Dashboard",
    "page_icon": "📈",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Custom CSS styles
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .positive-change {
        color: #00ff00;
        font-weight: bold;
    }
    .negative-change {
        color: #ff0000;
        font-weight: bold;
    }
</style>
""" 