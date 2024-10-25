from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
    data = []
    with open('static/py/form_4_filings.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            data.append(row)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)