import pytest

from app import create_app, generate_tracking_no
from models import Staff


# ==========================================================
# UT01 - Tracking Number Generation
# ==========================================================
def test_tracking_number_generation():

    app = create_app()

    with app.app_context():

        tracking_no = generate_tracking_no()

        print("\nGenerated Tracking Number:", tracking_no)

        assert tracking_no is not None
        assert tracking_no.startswith("CPX-")

        print("UT01 Tracking Number Generation: PASSED")


# ==========================================================
# UT02 - Tracking Number Prefix
# ==========================================================
def test_tracking_number_prefix():

    app = create_app()

    with app.app_context():

        tracking_no = generate_tracking_no()

        assert tracking_no[:4] == "CPX-"

        print("\nTracking Number:", tracking_no)
        print("Prefix CPX- verified")

        print("UT02 Tracking Number Prefix: PASSED")


# ==========================================================
# UT03 - Tracking Numbers Should Differ
# ==========================================================
def test_tracking_numbers_are_different():

    app = create_app()

    with app.app_context():

        number1 = generate_tracking_no()
        number2 = generate_tracking_no()

        print("\nTracking Number 1:", number1)
        print("Tracking Number 2:", number2)

        assert number1 != number2

        print("UT03 Tracking Number Uniqueness: PASSED")


# ==========================================================
# UT04 - Password Hashing
# ==========================================================
def test_password_hashing():

    staff = Staff(
        username="testuser",
        full_name="Test User"
    )

    staff.set_password("test123")

    print("\nPassword hash generated")

    assert staff.password_hash is not None
    assert staff.password_hash != "test123"

    print("UT04 Password Hashing: PASSED")


# ==========================================================
# UT05 - Correct Password Verification
# ==========================================================
def test_correct_password():

    staff = Staff(
        username="testuser",
        full_name="Test User"
    )

    staff.set_password("test123")

    result = staff.check_password("test123")

    print("\nCorrect password result:", result)

    assert result is True

    print("UT05 Correct Password Verification: PASSED")


# ==========================================================
# UT06 - Incorrect Password Verification
# ==========================================================
def test_incorrect_password():

    staff = Staff(
        username="testuser",
        full_name="Test User"
    )

    staff.set_password("test123")

    result = staff.check_password("wrongpassword")

    print("\nWrong password result:", result)

    assert result is False

    print("UT06 Incorrect Password Verification: PASSED")