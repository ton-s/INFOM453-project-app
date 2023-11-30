from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pickle
import os
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.abspath(__file__))

# Load the dataset
file_path = path + "/dataset.csv"
data = pd.read_csv(file_path, delimiter=';')

# Select features and target
features = data.drop('temperature', axis=1)
target = data['temperature']

# Divised the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Create polynomial features
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train.values)
X_test_poly = poly.transform(X_test.values)

# Create the model
model = LinearRegression()

# Train the model
model.fit(X_train_poly, y_train)

print(model.score(X_train_poly, y_train))

# Make predictions
predictions = model.predict(X_test_poly)

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
sample_data_poly = poly.transform([[0, 0, 0, 2, 4]]) 
result = round(model.predict(sample_data_poly)[0])

print(f"Prédiction : {result}")

# Save the model
model_path = path + "/model.pkl"
pickle.dump(model, open(model_path, 'wb'))



