import pytest
from app import app, expenses
from werkzeug.datastructures import MultiDict # Add this import

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        expenses.clear() 
        yield client

def test_add_expense(client):
    # Use MultiDict for explicit form data
    data_to_send = MultiDict([('name', 'Groceries'), ('amount', '50.00')])

    response = client.post(
        '/add', 
        data=data_to_send, # Use the MultiDict here
        content_type='application/x-www-form-urlencoded',
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b'Groceries' in response.data
    assert b'50.00' in response.data 

    assert len(expenses) == 1
    assert expenses[0]['name'] == 'Groceries'
    assert expenses[0]['amount'] == 50.00

def test_clear_expenses(client):
    # Use MultiDict for explicit form data when adding items
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

    initial_response = client.get('/', follow_redirects=True)
    assert b'Test Item 1' in initial_response.data
    assert b'Test Item 2' in initial_response.data

    response = client.get('/clear', follow_redirects=True)

    assert response.status_code == 200
    assert b'Test Item 1' not in response.data
    assert b'Test Item 2' not in response.data

    assert len(expenses) == 0