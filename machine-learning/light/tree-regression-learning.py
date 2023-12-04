from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import matplotlib.pyplot as plt
import os
import pickle

path = os.path.dirname(os.path.abspath(__file__))

# load the dataset
file_path = path + "/dataset.csv"
data = pd.read_csv(file_path, delimiter=';')

# Select features and target
features = data.drop('light', axis=1)
target = data['light']

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# create the model with max_depth 
model = DecisionTreeRegressor(max_depth=5)

# Train the model
model.fit(X_train, y_train)

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
new_data = pd.DataFrame({'day':[0,0,0,0,0,0,0,0,0,1], 'ext': [100, 60, 10, 600, 1500, 17, 132, 380, 80, 50]})

new_predictions = model.predict(new_data)

# Display the predictions
print("Prédictions sur les nouvelles données:")
print(new_predictions)

# Curve plot of predictions versus features
plt.scatter(new_data['ext'], new_predictions, color='green', label='Prédictions sur les nouvelles données')
plt.xlabel('Features')
plt.ylabel('Target')
plt.legend()
plt.show()

# Save the model
model_path = path + "/model.pkl"
pickle.dump(model, open(model_path, 'wb'))
