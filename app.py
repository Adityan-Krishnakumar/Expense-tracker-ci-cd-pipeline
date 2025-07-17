from flask import Flask, render_template, request, redirect, url_for
import logging # Add this line

app = Flask(__name__)
expenses = []

logging.basicConfig(level=logging.INFO) # Add this line to configure logging

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    logging.info("--- Entering add_expense function ---") # New log

    # Print the raw request method
    logging.info(f"Request method: {request.method}") # New log

    # Log the entire request.form object
    logging.info(f"Full request.form: {request.form}") # New log

    name = request.form.get('name')
    amount_str = request.form.get('amount')

    # Log the extracted values
    logging.info(f"Extracted 'name': {name}") # New log
    logging.info(f"Extracted 'amount_str': {amount_str}") # New log

    if not name or not amount_str:
        logging.error("Validation Error: Missing 'name' or 'amount_str'") # New log
        return "Missing data", 400 # This is where your 400 BAD REQUEST is likely coming from

    try:
        amount = float(amount_str)
        logging.info(f"Amount '{amount_str}' successfully converted to float: {amount}") # New log
    except ValueError:
        logging.error(f"Validation Error: Invalid amount format '{amount_str}'") # New log
        return "Invalid amount format", 400

    expense = {'name': name, 'amount': amount}
    expenses.append(expense)
    logging.info(f"Expense added: {expense}") # New log
    logging.info(f"Current expenses list: {expenses}") # New log

    logging.info("--- Exiting add_expense function (redirecting) ---") # New log
    return redirect(url_for('index'))

@app.route('/clear', methods=['GET'])
def clear_expenses():
    logging.info("--- Entering clear_expenses function ---") # New log
    expenses.clear()
    logging.info("All expenses cleared.") # New log
    logging.info("--- Exiting clear_expenses function (redirecting) ---") # New log
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)