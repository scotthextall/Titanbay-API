# Function to create test fund before running investments unit tests
def create_fund(client):
    return client.post("/funds", json={
        "name": "Fund A",
        "vintage_year": 2024,
        "target_size_usd": 1000000,
        "status": "Fundraising",
    }).json()

# Function to create test investor before running investments unit tests
def create_investor(client):
    return client.post("/investors", json={
        "name": "Investor A",
        "investor_type": "Institution",
        "email": "investor@example.com",
    }).json()

# Create new investment test
def test_create_investment(client):
    # Create fund and investor in database due to pre-requisite for creating a new investment
    fund = create_fund(client)
    investor = create_investor(client)

    response = client.post(f"/funds/{fund['id']}/investments", json={
        "investor_id": investor["id"],
        "amount_usd": 50000,
        "investment_date": "2024-06-01",
    })

    # Check status code returned is 201 and that fund_id of the investment matches id of fund that investment sits under
    assert response.status_code == 201
    assert response.json()["fund_id"] == fund["id"]

# Check creating an investment for a missing fund returns 404
def test_create_investment_fails_for_missing_fund(client):
    investor = create_investor(client)
    response = client.post(
        "/funds/00000000-0000-0000-0000-000000000000/investments",
        json={
            "investor_id": investor["id"],
            "amount_usd": 50000,
            "investment_date": "2024-06-01",
        },
    )
    assert response.status_code == 404

# Check creating an investment for a missing investor returns 404
def test_create_investment_fails_for_missing_investor(client):
    fund = create_fund(client)
    response = client.post(f"/funds/{fund['id']}/investments", json={
        "investor_id": "00000000-0000-0000-0000-000000000000",
        "amount_usd": 50000,
        "investment_date": "2024-06-01",
    })
    assert response.status_code == 404

# Check listing investments for a fund returns 200 and exactly 1 investment (newly created as part of the function)
def test_list_investments_for_fund(client):
    fund = create_fund(client)
    investor = create_investor(client)
    client.post(f"/funds/{fund['id']}/investments", json={
        "investor_id": investor["id"],
        "amount_usd": 1000,
        "investment_date": "2024-01-01",
    })

    response = client.get(f"/funds/{fund['id']}/investments")
    assert response.status_code == 200
    assert len(response.json()) == 1