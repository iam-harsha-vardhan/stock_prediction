import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA

# App Title
st.title("Stock Price Prediction")

# Stock Ticker Dropdown Menu with a wider range of popular tickers
tickers = [
    "AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "NFLX", "META", "NVDA", "SPY", "AMD", 
    "IBM", "ORCL", "INTC", "CSCO", "NVDA", "BABA", "WMT", "DIS", "V", "PYPL", "BA", 
    "GE", "JNJ", "PFE", "MRK", "XOM", "CVX", "T", "VZ", "GOOG", "MCD", "KO", "PEP", 
    "COST", "NKE", "TGT", "HD", "LOW", "INTU", "ADBE", "SQ", "LUV", "AIG", "GM", 
    "F", "USB", "C", "JPM", "WFC", "MS", "GS", "MA", "SPY", "SPCE", "SHOP", "BA",
    "RBLX", "TWTR", "PINS", "UBER", "LYFT", "Z", "ZM", "DDOG", "SNAP", "ETSY", "SE", 
    "SQ", "CRWD", "PLTR", "DOCU", "RNG", "SMH", "SOFI", "BIDU", "BYND", "CZR", "LULU"
]

# Sidebar for navigation
st.sidebar.title("S_T_O_C_K")
page = st.sidebar.radio("Choose a page", ["Stock Data", "Stock Info"])

# Stock Data Page (Existing page with historical and forecast graphs)
if page == "Stock Data":
    ticker = st.selectbox("Select Stock Ticker", tickers, index=0)

    # Time Period Buttons for Historical Data
    st.subheader("Select Time Period for Historical Data")
    col1, col2, col3, col4 = st.columns(4)

    time_period = "max"  # Default to "max"
    with col1:
        if st.button("24h"):
            time_period = "24h"
    with col2:
        if st.button("5d"):
            time_period = "5d"
    with col3:
        if st.button("1mo"):
            time_period = "1mo"
    with col4:
        if st.button("Max"):
            time_period = "max"

    # Fetch Historical Data
    @st.cache_data
    def get_historical_data(ticker, period):
        stock = yf.Ticker(ticker)
        if period == "24h":
            hist = stock.history(period="1d", interval="5m")  # 24 hours with 5-minute intervals
        elif period == "5d":
            hist = stock.history(period="5d")  # Last 5 days
        elif period == "1mo":
            hist = stock.history(period="1mo")  # Last 1 month
        else:
            hist = stock.history(period="max")  # Maximum available data
        return hist

    # Fetch data for the selected period (default to max)
    data = get_historical_data(ticker, time_period)

    # Function to create forecast dates for last 4 months and one month ahead
    def generate_forecast_dates(data, forecast_steps=30):
        # Get the last date from the historical data
        last_date = data.index[-1]
        
        # Create the range for the last 4 months
        start_date = last_date - pd.DateOffset(months=4)
        historical_dates = pd.date_range(start=start_date, end=last_date, freq='MS')  # MS means start of the month
        
        # Forecast Dates (1 month after the last historical data)
        forecast_dates = pd.date_range(last_date, periods=forecast_steps+1, freq='D')[1:]  # forecast the next 30 days
        
        # Concatenate the two ranges as a combined DatetimeIndex
        combined_dates = historical_dates.append(forecast_dates)  # Use append instead of concat
        
        return combined_dates

    # ARIMA Forecast
    @st.cache_data
    def arima_forecast(data, forecast_steps=30):
        model = ARIMA(data['Close'], order=(5, 1, 0))
        fitted_model = model.fit()
        forecast = fitted_model.forecast(steps=forecast_steps)  # Predict the next 30 days
        return forecast

    forecast = arima_forecast(data)

    # Plot Historical Data (Candlestick)
    def plot_candlestick(data, title="Candlestick Chart"):
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            increasing_line_color='green',
            decreasing_line_color='red',
            increasing_fillcolor='rgba(0, 255, 0, 0.3)',
            decreasing_fillcolor='rgba(255, 0, 0, 0.3)',
            name="Candlestick Chart"
        )])
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Stock Price",
            xaxis_rangeslider_visible=False,
            template="plotly_white"
        )
        return fig

    # Plot Prediction Graph (Line Graph)
    def plot_prediction(data, forecast, title="Stock Price Forecast (ARIMA)"):
        # Generate Forecast Dates for Last 4 Months and Next Month
        forecast_dates = generate_forecast_dates(data)

        # Historical Data and Forecast Data (Next 30 days)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Historical Prices',
            line=dict(color='blue', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=forecast_dates[-30:],  # Use the last 30 forecast dates for prediction line
            y=forecast,
            mode='lines',
            name='Forecast Prices',
            line=dict(color='red', dash='dash', width=2)
        ))
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Stock Price",
            template="plotly_white"
        )
        return fig

    # Display the Graphs
    st.subheader(f"Candlestick Chart for {ticker} (Last {time_period})")
    candlestick_fig = plot_candlestick(data)
    st.plotly_chart(candlestick_fig)

    st.subheader("Stock Price Forecast (ARIMA)")
    prediction_fig = plot_prediction(data, forecast)
    st.plotly_chart(prediction_fig)

# Stock Info Page (New page with stock info)
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Stock Info Page (Updated with charts)
if page == "Stock Info":
    ticker = st.selectbox("Select Stock Ticker", tickers, index=0)
    stock = yf.Ticker(ticker)
    
    # Get Stock Info
    stock_info = stock.info
    
    # Display Basic Information
    st.header(f"Basic Information for {ticker}")
    st.write(f"**Company Name:** {stock_info.get('longName', 'N/A')}")
    st.write(f"**Sector:** {stock_info.get('sector', 'N/A')}")
    st.write(f"**Industry:** {stock_info.get('industry', 'N/A')}")
    st.write(f"**Market Cap:** {stock_info.get('marketCap', 'N/A')}")
    st.write(f"**Country:** {stock_info.get('country', 'N/A')}")
    
    # Display Market Data
    st.header("Market Data")
    st.write(f"**Current Price:** ${stock_info.get('currentPrice', 'N/A')}")
    st.write(f"**52 Week High:** ${stock_info.get('fiftyTwoWeekHigh', 'N/A')}")
    st.write(f"**52 Week Low:** ${stock_info.get('fiftyTwoWeekLow', 'N/A')}")
    st.write(f"**PE Ratio:** {stock_info.get('trailingPE', 'N/A')}")
    
    # Display Dividends and Yield
    st.header("Dividends and Yield")
    st.write(f"**Dividend Yield:** {stock_info.get('dividendYield', 'N/A')}")
    st.write(f"**Dividend Rate:** {stock_info.get('dividendRate', 'N/A')}")
    
    # Display Valuation and Ratios
    st.header("Valuation and Ratios")
    st.write(f"**Price to Earnings (P/E):** {stock_info.get('trailingPE', 'N/A')}")
    st.write(f"**Price to Book (P/B):** {stock_info.get('priceToBook', 'N/A')}")
    
    # Display Financial Performance
    st.header("Financial Performance")
    st.write(f"**Revenue:** {stock_info.get('totalRevenue', 'N/A')}")
    st.write(f"**Gross Profit:** {stock_info.get('grossProfits', 'N/A')}")
    
    # Display Cash Flow
    st.header("Cash Flow")
    st.write(f"**Free Cash Flow:** {stock_info.get('freeCashflow', 'N/A')}")
    
    # Display Analyst Ratings
    st.header("Analyst Ratings")
    st.write(f"**Recommendation Mean:** {stock_info.get('recommendationMean', 'N/A')}")
    
    # 1. Stock Price History Chart (Last 6 months)
    st.header("Stock Price History (Last 6 months)")
    stock_history = stock.history(period="6mo")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_history.index, y=stock_history['Close'], mode='lines', name='Stock Price'))
    fig.update_layout(
        title=f"{ticker} Stock Price History (Last 6 months)",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark"
    )
    st.plotly_chart(fig)
    
    # 2. Valuation Metrics as Bar Chart (P/E, P/B)
    st.header("Valuation Metrics (P/E, P/B)")
    pe_ratio = stock_info.get('trailingPE', 'N/A')
    pb_ratio = stock_info.get('priceToBook', 'N/A')
    labels = ['P/E Ratio', 'P/B Ratio']
    values = [pe_ratio, pb_ratio]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['blue', 'green'])
    ax.set_title(f"{ticker} Valuation Metrics")
    ax.set_ylabel('Ratio Value')
    st.pyplot(fig)
    
    # 3. Analyst Ratings Distribution (Pie Chart)
    st.header("Analyst Ratings Distribution")
    recommendation_mean = stock_info.get('recommendationMean', 'N/A')
    
    # Assuming that the recommendationMean is a numerical value from 1 to 5, where:
    # 1 = Strong Buy, 2 = Buy, 3 = Hold, 4 = Sell, 5 = Strong Sell
    if recommendation_mean:
        if recommendation_mean <= 2:
            recommendation = "Strong Buy"
        elif recommendation_mean <= 3:
            recommendation = "Buy"
        elif recommendation_mean <= 4:
            recommendation = "Hold"
        else:
            recommendation = "Sell"
    else:
        recommendation = "N/A"
    
    st.write(f"**Analyst Recommendation Mean:** {recommendation_mean}")
    st.write(f"**Current Recommendation:** {recommendation}")

    # Example of possible distribution - you can replace it with real data
    analyst_ratings = {'Strong Buy': 35, 'Buy': 25, 'Hold': 30, 'Sell': 10}
    fig = go.Figure(data=[go.Pie(labels=list(analyst_ratings.keys()), values=list(analyst_ratings.values()))])
    fig.update_layout(title=f"{ticker} Analyst Ratings Distribution")
    st.plotly_chart(fig)
