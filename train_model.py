import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load the dataset
data = pd.read_csv('./train_data.csv')

# Clean the labels (e.g., './Dataset/reentrancy (RE)/' ➝ 'reentrancy')
def clean_label(label):
    return re.sub(r'[^a-zA-Z ]', '', label).strip().lower()

data['label'] = data['label'].apply(clean_label)

# Features and labels
X = data['code']
y = data['label']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train the model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(model, 'vulnerability_model_clean.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer_clean.pkl')

print("✅ Cleaned model and vectorizer saved.")
