import requests
import yfinance as yf


tk = ("reliance")
tkres = tk  + ".BO"
# url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=ioc&apikey=SF2KJLRRW7BRU3YD'
# r = requests.get(url)
# data = r.json()

# print(data)

ticker = yf.Ticker(tkres)
url = 'https://newsapi.org/v2/everything?'
params = {
    'q': ticker.info['industryKey'],
    'from': '2024-02-09',
    'sortBy': 'popularity',
    'apiKey': '7919e2baf4204e35ad417533b496a930',  # Replace with your actual API key
    'pageSize': 5  # Specify the number of articles to retrieve
}
response = requests.get(url, params=params)
#     articles = [
#     "Apple stock price is expected to rise in the next quarter.",
#     "The new iPhone release was met with disappointment by critics.",
#     "The company is facing financial difficulties."
# ]
data = response.json()
articles_with_sentiment = []
print(data)
print(response)
for article in data['articles']:
    print(article)