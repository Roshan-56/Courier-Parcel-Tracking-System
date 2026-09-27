import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    return app


@pytest.fixture
def client(app):
    return app.test_client()


# ==================================================
# IT01 - Home Page Integration
# ==================================================
def test_home_page(client):

    response = client.get("/")

    print("\nHome status code:", response.status_code)

    assert response.status_code == 200
    assert b"ParcelTrack" in response.data

    print("IT01 Home Page Integration: PASSED")


# ==================================================
# IT02 - Login Page Integration
# ==================================================
def test_login_page(client):

    response = client.get("/login")

    print("\nLogin status code:", response.status_code)

    assert response.status_code == 200
    assert b"username" in response.data
    assert b"password" in response.data

    print("IT02 Login Page Integration: PASSED")


# ==================================================
# IT03 - Invalid Login
# ==================================================
def test_invalid_login(client):

    response = client.post(
        "/login",
        data={
            "username": "wronguser",
            "password": "wrongpassword"
        },
        follow_redirects=True
    )

    print("\nInvalid login status:", response.status_code)

    assert response.status_code == 200

    page = response.data.lower()

    assert (
        b"invalid" in page
        or b"incorrect" in page
    )

    print("IT03 Invalid Login Integration: PASSED")


# ==================================================
# IT04 - Valid Login + Authentication + Database
# ==================================================
def test_valid_login(client):

    response = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin123"
        },
        follow_redirects=True
    )

    print("\nValid login status:", response.status_code)

    assert response.status_code == 200
    assert b"Dashboard" in response.data

    print("IT04 Valid Login Integration: PASSED")


# ==================================================
# IT05 - Protected Dashboard
# ==================================================
def test_dashboard_requires_login(client):

    response = client.get(
        "/dashboard",
        follow_redirects=False
    )

    print(
        "\nDashboard without login status:",
        response.status_code
    )

    print(
        "Redirect location:",
        response.headers.get("Location")
    )

    assert response.status_code in (301, 302)

    assert "/login" in response.headers.get(
        "Location", ""
    )

    print("IT05 Dashboard Protection: PASSED")


# ==================================================
# IT06 - Login + Dashboard Integration
# ==================================================
def test_login_and_dashboard(client):

    login = client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin123"
        },
        follow_redirects=True
    )

    assert login.status_code == 200

    dashboard = client.get("/dashboard")

    print(
        "\nDashboard after login:",
        dashboard.status_code
    )

    assert dashboard.status_code == 200
    assert b"Dashboard" in dashboard.data

    print("IT06 Login + Dashboard Integration: PASSED")


# ==================================================
# IT07 - Login + Shipment Page
# ==================================================
def test_shipment_page_after_login(client):

    client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin123"
        },
        follow_redirects=True
    )

    response = client.get("/shipments")

    print(
        "\nShipments page status:",
        response.status_code
    )

    assert response.status_code == 200
    assert b"Shipment" in response.data

    print("IT07 Shipment Page Integration: PASSED")


# ==================================================
# IT08 - New Shipment Form
# ==================================================
def test_new_shipment_form(client):

    client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin123"
        },
        follow_redirects=True
    )

    response = client.get("/shipments/new")

    print(
        "\nNew shipment page:",
        response.status_code
    )

    assert response.status_code == 200

    assert b'name="sender"' in response.data
    assert b'name="receiver"' in response.data
    assert b'name="origin"' in response.data
    assert b'name="destination"' in response.data

    print("IT08 New Shipment Form Integration: PASSED")