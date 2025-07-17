import pytest
from app import app, expenses

@pytest.fixture
def client():
    app.config['TESTING'] = True 
    with app.test_client() as client:
        
        expenses.clear()
        yield client 

def test_index_page(client):
    
    response = client.get('/')
    assert response.status_code == 200 
    assert b"No expenses added yet." in response.data 

def test_add_expense(client):
    """Test adding a new expense."""
    response = client.post('/add', data={'item': 'Lunch', 'amount': '15.50'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Lunch" in response.data
    assert b"15.50" in response.data 
    assert len(expenses) == 1 

def test_add_multiple_expenses(client):
    """Test adding multiple expenses."""
    client.post('/add', data={'item': 'Books', 'amount': '30.00'}, follow_redirects=True)
    client.post('/add', data={'item': 'Coffee', 'amount': '5.25'}, follow_redirects=True)
    assert len(expenses) == 2 
    assert b"Books" in client.get('/').data
    assert b"Coffee" in client.get('/').data

def test_clear_expenses(client):
    """Test clearing all expenses."""
    client.post('/add', data={'item': 'Dinner', 'amount': '25.00'}, follow_redirects=True)
    assert len(expenses) == 1 
    response = client.get('/clear', follow_redirects=True)
    assert response.status_code == 200
    assert b"No expenses added yet." in response.data 
    assert len(expenses) == 0 