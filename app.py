from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In a real app, you'd use a database. For simplicity, we'll use a list.
expenses = [] # List to store our expenses

@app.route('/')
def index():
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    if request.method == 'POST':
        item = request.form['item']
        amount = float(request.form['amount']) # Convert amount to float
        expenses.append({'item': item, 'amount': amount})
    return redirect(url_for('index'))

@app.route('/clear')
def clear_expenses():
    global expenses
    expenses = [] # Clear all expenses
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)