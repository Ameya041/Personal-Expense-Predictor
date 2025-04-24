from flask import Flask, render_template, request
from model.predictor import ExpensePredictor

app = Flask(_name_)
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

if _name_ == '_main_':
    app.run(debug=True)
