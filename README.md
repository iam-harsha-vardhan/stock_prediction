
# Stock Price Prediction and Information App
A Streamlit-based application that provides users with stock price data, prediction models, and relevant stock information. This app allows users to view historical stock prices, generate predictions using ARIMA, and explore detailed stock metrics such as market data, dividends, valuation ratios, and more.

#Features
Stock Price Data: Fetches historical stock data for selected tickers.
ARIMA Forecasting: Provides a 30-day forecast for stock prices using ARIMA.
Stock Information: Displays detailed stock information, including company data, market data, valuation metrics, and financial performance.
Interactive Charts: Uses Plotly for interactive candlestick charts and stock price history graphs.
Analyst Ratings: Displays analyst ratings and recommendations for the selected stock.

## Getting started

#Clone the repository:

git clone https://github.com/iam-harsha-vardhan/stock_prediction.git

#Install the required packages:

pip install -r requirements.txt

#Run the app:

streamlit run app.py

##How to Use

Select Stock Ticker: Choose from a list of popular stock tickers.
Choose Time Period: Select a time period (24 hours, 5 days, 1 month, or max data) for the historical stock data.
View Stock Data: Visualize historical data in the form of candlestick charts.
Forecast Stock Prices: View the predicted stock prices for the next 30 days based on ARIMA modeling.
Stock Information: View detailed stock info including market cap, P/E ratio, dividend yield, and financial performance.



#Acknowledgements
Streamlit: For building the interactive user interface.
yFinance: For fetching the stock data.
Plotly: For creating the interactive charts.
statsmodels: For implementing the ARIMA model.
