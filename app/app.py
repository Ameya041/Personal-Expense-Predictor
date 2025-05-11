import os
from flask import Flask, render_template, request
from model.predictor import ExpensePredictor

app = Flask(__name__)
model = ExpensePredictor()

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    chart_data = {}

    if request.method == 'POST':
        # read all six input fields
        income = float(request.form['income'])
        rent = float(request.form['rent'])
        grocery = float(request.form['grocery'])
        transport = float(request.form['transport'])
        subscriptions = float(request.form['subscriptions'])
        misc = float(request.form['misc'])

        # build a dict so predictor.predict can call .values()
        features = {
            'income': income,
            'rent': rent,
            'grocery': grocery,
            'transport': transport,
            'subscriptions': subscriptions,
            'misc': misc
        }
        # get prediction
        prediction = model.predict(features)

        # prepare chart data
        chart_data = {
            'Rent/EMI': rent,
            'Grocery': grocery,
            'Transport': transport,
            'Subscriptions': subscriptions,
            'Miscellaneous': misc
        }

    return render_template('form.html', prediction=prediction, chart_data=chart_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
