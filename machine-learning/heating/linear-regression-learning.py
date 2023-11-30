from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

import matplotlib.pyplot as plt

# Load the dataset
file_path = "dataset.csv"
data = pd.read_csv(file_path, delimiter=';')

# Select features and target
features = data.drop('temperature', axis=1)
target = data['temperature']

# Divised the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Create the model
model = LinearRegression()

# Train the model
model.fit(X_train.values, y_train.values)

print(model.score(X_train, y_train))

# Make predictions
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"Mean Squared Error: {mse}")
print(f"R-squared Score: {r2}")

# Plot the results
plt.scatter(y_test, predictions)
plt.xlabel("Valeurs réelles")
plt.ylabel("Prédictions")
plt.show()

# Make a prediction
result = round(model.predict([[0, 0, 0, 2, 4]])[0])

print(f"Prédiction : {result}")

# Save the model
pickle.dump(model, open('model.pkl', 'wb'))


