import pytest
from app import app, expenses # Make sure 'expenses' is imported from your app.py

# Fixture to set up a test client for the Flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True # Enable Flask's testing mode
    with app.test_client() as client:
        # IMPORTANT: Clear the global 'expenses' list before each test.
        # This ensures that each test run starts with a clean slate,
        # preventing previous test data from affecting subsequent tests.
        expenses.clear() 
        yield client # Provide the test client to the test functions

# Test case for adding an expense
def test_add_expense(client):
    # Send a POST request to the /add endpoint with form data.
    # Use 'data' for compatibility with older Werkzeug/Flask versions,
    # but explicitly set 'content_type' to ensure it's treated as form data.
    # 'follow_redirects=True' ensures the test client automatically follows the redirect
    response = client.post(
        '/add', 
        data={'name': 'Groceries', 'amount': '50.00'}, 
        content_type='application/x-www-form-urlencoded', # Crucial change here
        follow_redirects=True
    )

    # After following redirects, the final page should be the main page (index.html),
    # which typically returns a 200 OK status code.
    assert response.status_code == 200

    # Assert that the added expense details are now present in the final HTML response.
    assert b'Groceries' in response.data
    assert b'50.00' in response.data 

    # Optional: You could also check if the expenses list in the app itself was updated
    assert len(expenses) == 1
    assert expenses[0]['name'] == 'Groceries'
    assert expenses[0]['amount'] == 50.00 # Flask's request.form will convert '50.00' to a float

# Test case for clearing all expenses
def test_clear_expenses(client):
    # First, add some expenses to ensure there's something to clear.
    # Use 'data' with 'content_type' here as well, and follow redirects.
    client.post(
        '/add', 
        data={'name': 'Test Item 1', 'amount': '10.00'}, 
        content_type='application/x-www-form-urlencoded', # Crucial change here
        follow_redirects=True
    )
    client.post(
        '/add', 
        data={'name': 'Test Item 2', 'amount': '20.00'}, 
        content_type='application/x-www-form-urlencoded', # Crucial change here
        follow_redirects=True
    )

    # Verify they are present on the initial page load before clearing
    initial_response = client.get('/', follow_redirects=True)
    assert b'Test Item 1' in initial_response.data
    assert b'Test Item 2' in initial_response.data

    # Send a GET request to the /clear endpoint and follow redirects
    response = client.get('/clear', follow_redirects=True)

    # Expect a 200 OK status code after following the redirect to the main page
    assert response.status_code == 200

    # Assert that the cleared items are no longer present on the page
    assert b'Test Item 1' not in response.data
    assert b'Test Item 2' not in response.data

    # Also verify that the global expenses list is empty after clearing.
    assert len(expenses) == 0