# Test successful fund creation
def test_create_fund(client):
    response = client.post("/funds", json={
        "name": "Test Fund",
        "vintage_year": 2024,
        "target_size_usd": 1000000,
        "status": "Fundraising",
    })
    # Check successful creation (201) and that fund name matches what was sent
    assert response.status_code == 201
    assert response.json()["name"] == "Test Fund"

# Test invalid negative target size amount
def test_create_fund_rejects_negative_target_size(client):
    response = client.post("/funds", json={
        "name": "Bad Fund",
        "vintage_year": 2024,
        "target_size_usd": -100,
        "status": "Fundraising",
    })
    assert response.status_code == 422

# Test invalid fund status
def test_create_fund_rejects_invalid_status(client):
    response = client.post("/funds", json={
        "name": "Bad Fund",
        "vintage_year": 2024,
        "target_size_usd": 1000,
        "status": "NotARealStatus",
    })
    assert response.status_code == 422

# Test 404 path on missing fund
def test_get_fund_not_found(client):
    response = client.get("/funds/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

# Test that GET /funds returns an empty list [] when no data in database (vs. crashing on empty result)
def test_list_funds_empty(client):
    response = client.get("/funds")
    assert response.status_code == 200
    assert response.json() == []

# Test updating fund
def test_update_fund(client):
    # Create new fund first so that there is a fund to update
    create_response = client.post("/funds", json={
        "name": "Original Name",
        "vintage_year": 2024,
        "target_size_usd": 1000000,
        "status": "Fundraising",
    })
    fund_id = create_response.json()["id"]

    # Update the previously created fund
    update_response = client.put("/funds", json={
        "id": fund_id,
        "name": "Original Name",
        "vintage_year": 2024,
        "target_size_usd": 1000000,
        "status": "Investing",
    })

    # Check that update succeeded (200 status code) and that status reflects the latest update "Investing"
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "Investing"


# Test that updating a fund which doesn't exist returns 404
def test_update_fund_not_found(client):
    response = client.put("/funds", json={
        "id": "00000000-0000-0000-0000-000000000000",
        "name": "Ghost Fund",
        "vintage_year": 2024,
        "target_size_usd": 1000,
        "status": "Fundraising",
    })
    assert response.status_code == 404