# Test creating a new investor
def test_create_investor(client):
    response = client.post("/investors", json={
        "name": "CalPERS",
        "investor_type": "Institution",
        "email": "test@example.com",
    })
    # Status code should return 201 and check investor name matches
    assert response.status_code == 201
    assert response.json()["name"] == "CalPERS"

# Check duplicate email isn't accepted
def test_create_investor_rejects_duplicate_email(client):
    # Create investor in database
    payload = {"name": "Investor A", "investor_type": "Institution", "email": "dup@example.com"}
    client.post("/investors", json=payload)

    # Try creating another investor with the same email
    response = client.post("/investors", json={**payload, "name": "Investor B"})

    # Check returned status code is 409, consistent with duplicate/conflicting email
    assert response.status_code == 409

# Check invalid investor type
def test_create_investor_rejects_invalid_type(client):
    response = client.post("/investors", json={
        "name": "Bad Investor",
        "investor_type": "NotARealType",
        "email": "bad@example.com",
    })
    assert response.status_code == 422