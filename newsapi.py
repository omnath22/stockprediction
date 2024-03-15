import requests

def fetch_news(company_name, api_key):
    # Base URL for the News API
    base_url = 'https://newsapi.org/v2/everything'

    # Parameters for the API request
    params = {
        'q': company_name,  # Company name to search for
        'apiKey': api_key   # Your News API key
    }

    try:
        # Make the GET request to the API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        news_data = response.json()

        # Extract and print relevant information from the response
        for article in news_data['articles']:
            print('Title:', article['title'])
            print('Description:', article['description'])
            print('Source:', article['source']['name'])
            print('URL:', article['url'])
            print('Published At:', article['publishedAt'])
            print('---')

    except requests.exceptions.RequestException as e:
        # Print an error message if there's a problem with the request
        print('Error:', e)

# Example usage: Search for news articles related to Apple Inc.
company_name = 'reliance.'
api_key = 'YOUR_API_KEY_HERE'  # Replace with your News API key
fetch_news(company_name, "7919e2baf4204e35ad417533b496a930")
