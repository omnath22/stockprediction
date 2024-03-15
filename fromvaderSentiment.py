from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    # Create a SentimentIntensityAnalyzer object
    analyzer = SentimentIntensityAnalyzer()
    
    # Perform sentiment analysis
    sentiment_scores = analyzer.polarity_scores(text)
    
    # Classify sentiment as positive, negative, or neutral based on compound score
    if sentiment_scores['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Example news article
news_article = """
 Reliance gains $8.5 Billion Deal to Merge India Media Operations."""

# Analyze sentiment of the news article
sentiment = analyze_sentiment(news_article)
print("Sentiment of the news article:", sentiment)
