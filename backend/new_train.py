import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from imblearn.over_sampling import SMOTE  # For handling class imbalance
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

# Load the dataset
data = pd.read_csv('./Dataset/newdata.csv')  # Use the improved CSV file

# Features (code examples) and labels (vulnerability types)
X = data['Example']
y = data['Vulnerability']

# Split the data (stratify to maintain class balance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# TF-IDF Vectorizer with Solidity-specific adjustments
vectorizer = TfidfVectorizer(
    max_features=1500,  # Increased to capture more code patterns
    stop_words=None,
    ngram_range=(1, 3),  # Now includes 3-grams (e.g., "msg.sender.call")
    analyzer='word',     # Focus on Solidity keywords
    token_pattern=r'\b\w+\b|\S+',  # Capture Solidity-specific tokens like `uint256`
    lowercase=False      # Preserve case sensitivity (important for Solidity)
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Handle class imbalance with SMOTE (only on training data)
# Handle class imbalance with SMOTE (only on training data)
smote = SMOTE(random_state=42, k_neighbors=2)  # Reduce neighbors for SMOTE
X_train_res, y_train_res = smote.fit_resample(X_train_vec, y_train)


# Train the model with hyperparameters tuned for code analysis
model = RandomForestClassifier(
    n_estimators=300,           # More trees for better stability
    class_weight='balanced',    # Double protection against imbalance
    max_depth=15,               # Prevent overfitting
    min_samples_split=5,        # More granular splits
    random_state=42,
    n_jobs=-1                   # Use all CPU cores
)
model.fit(X_train_res, y_train_res)

# Evaluate the model
y_pred = model.predict(X_test_vec)

# Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix with improved readability
plt.figure(figsize=(12, 10))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=np.unique(y), 
            yticklabels=np.unique(y),
            cbar=False)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Vulnerability Classification Confusion Matrix')
plt.tight_layout()
plt.show()

# Feature Importance (Top 20 tokens)
feature_importances = pd.DataFrame({
    'token': vectorizer.get_feature_names_out(),
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False).head(20)

plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='token', data=feature_importances, palette='viridis')
plt.title('Top 20 Important Code Tokens for Vulnerability Detection')
plt.tight_layout()
plt.show()

# Save model and vectorizer with versioning
timestamp = time.strftime("%Y%m%d-%H%M%S")
joblib.dump(model, f'models/vulnerability_model_{timestamp}.pkl')
joblib.dump(vectorizer, f'models/tfidf_vectorizer_{timestamp}.pkl')

# Print final evaluation metrics
print(f"✅ Model saved with accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"✅ F1-score (weighted): {f1_score(y_test, y_pred, average='weighted'):.2f}")
