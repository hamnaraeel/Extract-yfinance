
import yfinance as yf
import json

def print_json(title, data):
	print(f"\n--- {title} ---")
	try:
		# Try to convert DataFrame/Series to dict
		if hasattr(data, 'to_dict'):
			print(json.dumps(data.to_dict(), indent=2, default=str))
		else:
			print(json.dumps(data, indent=2, default=str))
	except Exception as e:
		print(f"Error converting to JSON: {e}")
		print(data)

# Step 2: Single Ticker
ticker = yf.Ticker("AAPL")
print_json("Apple (AAPL) Info", ticker.info)
history = ticker.history(period="1mo")
print_json("Historical Data (1mo)", history.head())
print_json("Dividends", ticker.dividends)
print_json("Splits", ticker.splits)

# Step 3: Multiple Tickers
tickers = yf.Tickers("AAPL MSFT TSLA")
print_json("AAPL Info (Multiple)", tickers.tickers["AAPL"].info)
print_json("MSFT History (5d)", tickers.tickers["MSFT"].history(period="5d"))

# Step 4: Market Summary (commented out due to error)
# market = yf.Market("US")
# summary = market.summary()
# print_json("Market Summary", summary)

# Step 5: Download Function
data = yf.download(["AAPL", "MSFT"], start="2024-01-01", end="2024-02-01")
print_json("Download OHLCV", data.head())

# Step 6: Search and Lookup (commented out, may require API access)
# search = yf.Search("Tesla")
# print_json("Search Tesla", search.tickers)
# lookup = yf.Lookup("US0378331005")
# print_json("Lookup Apple by ISIN", lookup.tickers)

# Step 7: Sector and Industry Data (commented out, may require API access)
# sectors = yf.Sector()
# print_json("Sectors", sectors.all())
# industries = yf.Industry()
# print_json("Industries", industries.all())

# Step 8: Live Market Data (WebSocket, commented out)
# from yfinance import WebSocket
# ws = WebSocket(["AAPL", "MSFT"])
# for message in ws:
#     print_json("Live Trade Update", message)
