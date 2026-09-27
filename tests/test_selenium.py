from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:5000"


def test_logout():

    driver = webdriver.Chrome()

    try:
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)

        # =====================================
        # STEP 1 - LOGIN
        # =====================================

        driver.get(BASE_URL + "/login")

        username = wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "username")
            )
        )

        username.send_keys("admin")

        driver.find_element(
            By.NAME, "password"
        ).send_keys("admin123")

        login_button = driver.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']"
        )

        driver.execute_script(
            "arguments[0].click();",
            login_button
        )

        wait.until(
            EC.url_contains("/dashboard")
        )

        print("\nLogin successful")
        print("Dashboard URL:", driver.current_url)

        assert "/dashboard" in driver.current_url

        # =====================================
        # STEP 2 - LOGOUT
        # =====================================

        driver.get(BASE_URL + "/logout")

        print("Logout request completed")
        print("After logout URL:", driver.current_url)

        # =====================================
        # STEP 3 - TRY DASHBOARD AGAIN
        # =====================================

        driver.get(BASE_URL + "/dashboard")

        wait.until(
            lambda d: "/login" in d.current_url
        )

        print(
            "Dashboard request after logout:",
            driver.current_url
        )

        # =====================================
        # STEP 4 - VERIFY SESSION TERMINATED
        # =====================================

        assert "/login" in driver.current_url
        assert "/dashboard" not in driver.current_url

        print("Session terminated successfully")
        print("Protected dashboard blocked")

        print("\n==============================")
        print("LOGOUT TEST SUCCESSFUL")
        print("==============================")

        print("\nTC12 LOGOUT: PASSED")

    finally:
        driver.quit()