from flask import Flask, render_template, request, redirect, url_for
import logging # Added for logging

app = Flask(__name__)
expenses = [] # Your global list to store expenses

# Configure basic logging to output INFO messages to the console (which GitHub Actions captures)
logging.basicConfig(level=logging.INFO)

# Route for the main page, displays the form and expense list
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', expenses=expenses)

# Route to handle adding new expenses
@app.route('/add', methods=['POST'])
def add_expense():
    logging.info("--- Entering add_expense function ---") # Log entry
    logging.info(f"Request method: {request.method}") # Log request method
    logging.info(f"Full request.form: {request.form}") # Crucial: Log the entire form data received

    name = request.form.get('name')
    amount_str = request.form.get('amount')
    
    logging.info(f"Extracted 'name': {name}") # Log extracted name
    logging.info(f"Extracted 'amount_str': {amount_str}") # Log extracted amount string

    # Basic server-side validation
    if not name or not amount_str:
        logging.error("Validation Error: Missing 'name' or 'amount_str'") # Log error
        return "Missing data", 400 # Return 400 if required data is missing

    try:
        amount = float(amount_str)
        logging.info(f"Amount '{amount_str}' successfully converted to float: {amount}") # Log successful conversion
    except ValueError:
        logging.error(f"Validation Error: Invalid amount format '{amount_str}'") # Log error if conversion fails
        return "Invalid amount format", 400

    expense = {'name': name, 'amount': amount}
    expenses.append(expense) # Add expense to the global list
    logging.info(f"Expense added: {expense}") # Log added expense
    logging.info(f"Current expenses list: {expenses}") # Log current state of expenses

    logging.info("--- Exiting add_expense function (redirecting) ---") # Log exit
    return redirect(url_for('index')) # Redirect back to the main page

# Route to clear all expenses
@app.route('/clear', methods=['GET'])
def clear_expenses():
    logging.info("--- Entering clear_expenses function ---") # Log entry
    expenses.clear() # Clear the global expenses list
    logging.info("All expenses cleared.") # Log action
    logging.info("--- Exiting clear_expenses function (redirecting) ---") # Log exit
    return redirect(url_for('index')) # Redirect back to the main page

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask app in debug mode (useful for local development)