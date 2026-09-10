def test_create_account(client, auth_headers):
    response = client.post(
        "/accounts/",
        json={"alias": "Caja de ahorro", "currency": "ARS"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["alias"] == "Caja de ahorro"
    assert data["balance"] == 0.0


def test_create_account_without_auth_fails(client):
    response = client.post("/accounts/", json={"alias": "Caja de ahorro"})
    assert response.status_code == 401


def test_list_accounts_only_shows_own(client, auth_headers):
    client.post("/accounts/", json={"alias": "Cuenta 1"}, headers=auth_headers)
    client.post("/accounts/", json={"alias": "Cuenta 2"}, headers=auth_headers)

    response = client.get("/accounts/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2