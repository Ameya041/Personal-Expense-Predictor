# app/model/predictor.py
import pickle
import numpy as np
import os

class ExpensePredictor:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "expense_model.pkl")
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, data):
        return self.model.predict([list(data.values())])[0]

