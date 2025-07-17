import pytest
from app import app, expenses # Make sure 'app' and 'expenses' are imported
from werkzeug.datastructures import MultiDict # Added for explicit form data handling

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
    # Prepare data using MultiDict for explicit form submission.
    # This ensures compatibility across different Werkzeug/Flask versions.
    data_to_send = MultiDict([('name', 'Groceries'), ('amount', '50.00')])
    
    # Send a POST request to the /add endpoint.
    # 'data' carries the MultiDict, 'content_type' tells the server how to interpret it.
    # 'follow_redirects=True' ensures the test client handles the redirect from /add to /.
    response = client.post(
        '/add', 
        data=data_to_send, 
        content_type='application/x-www-form-urlencoded', 
        follow_redirects=True
    )
    
    # After following redirects, the final page should be the main page (index.html),
    # which typically returns a 200 OK status code.
    assert response.status_code == 200
    
    # Assert that the added expense details are now present in the final HTML response.
    # We check for the byte strings (b'...') because response.data is in bytes.
    assert b'Groceries' in response.data
    assert b'50.00' in response.data 
    
    # Optional but recommended: Verify the internal state of the 'expenses' list
    assert len(expenses) == 1
    assert expenses[0]['name'] == 'Groceries'
    assert expenses[0]['amount'] == 50.00 # Flask's request.form will convert '50.00' to a float

# Test case for clearing all expenses
def test_clear_expenses(client):
    # First, add some expenses to ensure there's something to clear.
    # Using MultiDict and content_type for POST requests here as well.
    client.post(
        '/add', 
        data=MultiDict([('name', 'Test Item 1'), ('amount', '10.00')]), 
        content_type='application/x-www-form-urlencoded', 
        follow_redirects=True
    )
    client.post(
        '/add', 
        data=MultiDict([('name', 'Test Item 2'), ('amount', '20.00')]), 
        content_type='application/x-www-form-urlencoded', 
        follow_redirects=True
    )

    # Verify they are present on the initial page load before clearing.
    # This also helps confirm that the previous 'add' operations were successful and displayed.
    initial_response = client.get('/', follow_redirects=True)
    assert b'Test Item 1' in initial_response.data
    assert b'Test Item 2' in initial_response.data

    # Send a GET request to the /clear endpoint and follow redirects.
    response = client.get('/clear', follow_redirects=True)
    
    # Expect a 200 OK status code after following the redirect to the main page.
    assert response.status_code == 200
    
    # Assert that the cleared items are no longer present on the page.
    assert b'Test Item 1' not in response.data
    assert b'Test Item 2' not in response.data
    
    # Also verify that the global expenses list is empty after clearing.
    assert len(expenses) == 0