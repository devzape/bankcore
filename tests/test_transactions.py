def create_two_accounts(client, headers):
    acc1 = client.post("/accounts/", json={"alias": "Cuenta 1"}, headers=headers).json()
    acc2 = client.post("/accounts/", json={"alias": "Cuenta 2"}, headers=headers).json()
    return acc1["id"], acc2["id"]


def test_deposit_increases_balance(client, auth_headers):
    acc_id, _ = create_two_accounts(client, auth_headers)

    response = client.post(
        "/transactions/deposit",
        json={"account_id": acc_id, "amount": 500, "description": "Test"},
        headers=auth_headers,
    )
    assert response.status_code == 200

    account = client.get(f"/accounts/{acc_id}", headers=auth_headers).json()
    assert account["balance"] == 500.0


def test_transfer_moves_money_correctly(client, auth_headers):
    acc1_id, acc2_id = create_two_accounts(client, auth_headers)

    client.post(
        "/transactions/deposit",
        json={"account_id": acc1_id, "amount": 1000},
        headers=auth_headers,
    )

    response = client.post(
        "/transactions/transfer",
        json={"from_account_id": acc1_id, "to_account_id": acc2_id, "amount": 300},
        headers=auth_headers,
    )
    assert response.status_code == 200

    acc1 = client.get(f"/accounts/{acc1_id}", headers=auth_headers).json()
    acc2 = client.get(f"/accounts/{acc2_id}", headers=auth_headers).json()
    assert acc1["balance"] == 700.0
    assert acc2["balance"] == 300.0


def test_transfer_with_insufficient_balance_fails(client, auth_headers):
    acc1_id, acc2_id = create_two_accounts(client, auth_headers)

    response = client.post(
        "/transactions/transfer",
        json={"from_account_id": acc1_id, "to_account_id": acc2_id, "amount": 100},
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_transfer_to_same_account_fails(client, auth_headers):
    acc_id, _ = create_two_accounts(client, auth_headers)

    response = client.post(
        "/transactions/transfer",
        json={"from_account_id": acc_id, "to_account_id": acc_id, "amount": 50},
        headers=auth_headers,
    )
    assert response.status_code == 400