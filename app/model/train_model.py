# app/model/train_model.py
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression

# Training data (mock)
X = np.array([
    [25000, 7000, 3000, 1500, 1000, 2000],
    [30000, 8000, 3500, 2000, 1200, 2500],
    [20000, 6000, 2500, 1000, 800, 1500],
    [28000, 7500, 3200, 1700, 1100, 2200],
])
y = np.array([14500, 17000, 11800, 15800])

# Train and save model
model = LinearRegression()
model.fit(X, y)

import os

model_path = os.path.join(os.path.dirname(__file__), "expense_model.pkl")

with open(model_path, "wb") as f:
    pickle.dump(model, f)
