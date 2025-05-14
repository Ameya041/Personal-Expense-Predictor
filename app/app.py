import os
from flask import Flask, render_template, request
from model.predictor import ExpensePredictor
from datetime import datetime
import json
from pathlib import Path

app = Flask(__name__, static_folder='static')
model = ExpensePredictor()

# File to store historical data
HISTORY_FILE = Path('expense_history.json')

def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    chart_data = {}
    error = None
    trends = load_history()
    
    if request.method == 'POST':
        try:
            # Get form data
            income = float(request.form['income'])
            rent = float(request.form['rent'])
            grocery = float(request.form['grocery'])
            transport = float(request.form['transport'])
            subscriptions = float(request.form['subscriptions'])
            misc = float(request.form['misc'])

            # Prepare features
            features = {
                'income': income,
                'rent': rent,
                'grocery': grocery,
                'transport': transport,
                'subscriptions': subscriptions,
                'misc': misc
            }

            # Get prediction
            prediction = round(model.predict(features), 2)

            # Prepare chart data
            chart_data = {
                'Rent/EMI': rent,
                'Grocery': grocery,
                'Transport': transport,
                'Subscriptions': subscriptions,
                'Miscellaneous': misc
            }

            # Update history
            current_month = datetime.now().strftime("%B %Y")
            total_expense = sum(chart_data.values())
            trends.append({
                'month': current_month,
                'predicted': prediction,
                'actual': total_expense,
                'categories': chart_data
            })
            
            # Keep only last 12 months
            trends = trends[-12:]
            save_history(trends)

        except ValueError as e:
            error = "Please enter valid numbers in all fields"
        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template('form.html', 
                        prediction=prediction, 
                        chart_data=chart_data,
                        trends=trends,
                        error=error)

if __name__ == '__main__':
    HISTORY_FILE.touch(exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
