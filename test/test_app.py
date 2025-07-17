import pytest
from app import app, expenses # Make sure 'expenses' is imported from your app.py

# Fixture to set up a test client for the Flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True # Enable Flask's testing mode
    with app.test_client() as client:
        # Clear the expenses list before each test to ensure tests are isolated
        # This is crucial for consistent test results as 'expenses' is a global list
        expenses.clear() 
        yield client # Provide the test client to the test functions

# Test case for adding an expense
def test_add_expense(client):
    # Send a POST request to the /add endpoint with form data
    # follow_redirects=True tells the test client to automatically follow any HTTP redirects
    # that the Flask app might issue after processing the form (e.g., redirecting to '/')
    response = client.post('/add', data={'name': 'Groceries', 'amount': '50.00'}, follow_redirects=True)
    
    # After following redirects, the final page should be the main page (index.html),
    # which typically returns a 200 OK status code.
    assert response.status_code == 200
    
    # Assert that the added expense details are now present in the final HTML response.
    # We check for the byte strings as response.data is bytes.
    assert b'Groceries' in response.data
    assert b'50.00' in response.data 
    
    # Optional: You could also check if the expenses list in the app itself was updated
    # assert len(expenses) == 1
    # assert expenses[0]['name'] == 'Groceries'
    # assert expenses[0]['amount'] == 50.00

# Test case for clearing all expenses
def test_clear_expenses(client):
    # First, add some expenses to ensure there's something to clear
    client.post('/add', data={'name': 'Test Item 1', 'amount': '10.00'}, follow_redirects=True)
    client.post('/add', data={'name': 'Test Item 2', 'amount': '20.00'}, follow_redirects=True)

    # Verify they are present before clearing (optional, but good for robust testing)
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
    
    # Optional: If your app displays a success message after clearing, you can assert that too
    # assert b'Expenses cleared successfully!' in response.data 

    # Optional: Also verify the global expenses list is empty
    # assert len(expenses) == 0
    # End of test file - dummy change