import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('./Dataset/convertcsv.csv')  # Replace with your CSV path

# Features (code examples) and labels (vulnerability types)
X = data['Example']
y = data['Vulnerability']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y  # Stratify for balanced classes
)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(
    max_features=1000,
    stop_words=None,  # Solidity code has no "stop words"
    ngram_range=(1, 2)  # Capture 1-2 word sequences (e.g., "uint256" or "external call")
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train the model
model = RandomForestClassifier(
    n_estimators=200,  # More trees for better generalization
    class_weight='balanced',  # Handle class imbalance
    random_state=42
)
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
plt.figure(figsize=(10, 8))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# Save model and vectorizer
joblib.dump(model, 'vulnerability_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

print("✅ Model and vectorizer saved!")