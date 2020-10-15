import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from hashlib import sha256

stonks = ['ACN', 'MSFT', 'DIS', 'V', 'NVDA', 'PEP', 'AAPL', 'GOOGL', 'VOT', 'DGRO','SPHD','VWO', 'VEA', 'VCLT', 'SPLB', 'IGLB']
unique_filename = sha256(''.join(stonks).encode('utf-8')).hexdigest() # create a unique filename based on above unique stonks!
print(unique_filename)

try:
    coll = pd.read_pickle(unique_filename) # Read from file if it exists
    print("Previous stonks file found. Using it.")
except FileNotFoundError:
    print('Stonks pickle not found. Creating a new one based on your stonks')
    coll = yf.download(stonks, start="2015-10-01", end="2020-10-01", interval='1d', group_by='tickers') # get data
    coll.to_pickle(unique_filename) # Save this to file

# Clean up columns
to_drop = ['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits', 'Adj Close']
price_close = coll.drop(to_drop, level=1, axis=1)

# Describe it
print(price_close.describe())

# Calculate returns
returns = price_close.pct_change(axis=0,fill_method='bfill')
print(returns.describe())

# Calculate corr for both prices and returns
prices_corr = price_close.corr()
returns_corr = returns.corr()

# Since it makes sense to show corr for returns, here you go
# https://quantdare.com/correlation-prices-returns/
# https://quant.stackexchange.com/questions/489/correlation-between-prices-or-returns
sb.heatmap(returns_corr, annot=True)
plt.show()