import pandas as pd

# Replace with your data collection method (including sentiment labels)
data = pd.DataFrame({
    "text": [
        "Apple stock price is rising!",
        "The new iPhone release was disappointing.",
        "The company is facing financial challenges, but they are optimistic about the future."
    ],
    "sentiment": ["positive", "negative", "neutral"]  # Add sentiment labels based on your data collection
})

# Preprocess text (remove punctuation, lowercase, etc.)
data["text"] = data["text"].str.lower().str.replace("[^\w\s]", "", regex=True)
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(max_features=1000)
features = vectorizer.fit_transform(data["text"])
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, data["sentiment"], test_size=0.2)

# Train a Naive Bayes model
model = MultinomialNB()
model.fit(X_train, y_train, pos_label="positive")
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1:.2f}")
