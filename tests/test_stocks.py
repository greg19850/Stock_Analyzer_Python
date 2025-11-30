def test_get_stocks_empty(client):
    """Test GET /stocks/ returns empty list when database is empty."""

    # Arrange - db is empty

    #  Act - make request
    response = client.get("/api/v1/stocks/")

    # Assert - check response
    assert response.status_code == 200
    assert response.json() == []

def test_create_stock(client):
    """Test POST /stocks/ creates new stock."""

    # Arrange
    stock_data = {
        "symbol": "AAPL",
        "name": "Apple Inc",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }

    # Act
    response = client.post("/api/v1/stocks/", json=stock_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["name"] == "Apple Inc"
    assert data["exchange"] == "NASDAQ"
    assert data["sector"] == "Technology"
    assert data["industry"] == "Consumer Electronics"

def test_create_duplicate_symbol(client):
    """Test POST /stocks/ returns 400 when creating duplicate symbol."""

    stock_data_1 = {
        "symbol": "AAPL",
        "name": "Apple Inc",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }

    stock_data_2 = {
        "symbol": "AAPL",
        "name": "Other Stock",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }

    response_1 = client.post("/api/v1/stocks/", json=stock_data_1)
    response_2 = client.post("/api/v1/stocks/", json=stock_data_2)

    assert response_1.status_code == 201
    assert response_2.status_code == 400
    assert "already exist" in response_2.json()["detail"].lower()

def test_create_with_missing_fields(client):

    """Test POST /stocks/ returns error when missing required fields."""
    stock_data = {
        "symbol": "AAPL",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }

    response = client.post("/api/v1/stocks", json=stock_data)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"][-1] == "name" for error in errors)

def test_valid_stock_returned(client):
    """Test Get /stocks/{id} returns valid stock"""
    # Arrange
    stock_data = {
        "symbol": "AAPL",
        "name": "Apple Inc",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }

    # Act
    client.post("/api/v1/stocks/", json=stock_data)
    response = client.get("/api/v1/stocks/1")

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert data["symbol"] == stock_data["symbol"]
    assert data["name"] == stock_data["name"]
    assert data["exchange"] == stock_data["exchange"]
    assert data["sector"] == stock_data["sector"]
    assert data["industry"] == stock_data["industry"]

def test_stock_not_found(client):
    """Test Get /stocks/{id} returns 404 when id of stock not found"""

    # Arrange - no stocks needed

    # Act
    response = client.get("/api/v1/stocks/2")

    # Assert
    assert response.status_code == 404