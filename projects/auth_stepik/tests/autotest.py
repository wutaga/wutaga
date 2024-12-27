import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Fixture for browser initialization


@pytest.fixture
def browser(request):

    chrome_options = Options()
    if request.config.getoption("--headless"):
        chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    yield browser
    browser.quit()


def test_login_form_accessibility_SK1(browser):
    """
    check the availability of the login form
    """
    browser.get("https://stepik.org/catalog?auth=login")

    login_form = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "modal-dialog-inner"))
    )
    assert login_form.is_displayed(), "Login_form not found"

    email = browser.find_element(By.CSS_SELECTOR, '[name="login"]')
    assert email.is_displayed(), "email field not found"

    password = browser.find_element(By.CSS_SELECTOR, '[name="password"]')
    assert password.is_displayed(), "password field not found"


def test_successful_login_SK2(browser):
    """
    successful_login
    """
    browser.get("https://stepik.org/catalog?auth=login")
    login_form = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "modal-dialog-inner"))
    )
    assert login_form.is_displayed(), "Login_form not found"

    email = browser.find_element(By.CSS_SELECTOR, '[name="login"]')
    password = browser.find_element(By.CSS_SELECTOR, '[name="password"]')
    email.send_keys("test_off@outlook.com")
    password.send_keys("r3XRXTJB2gn!!cE")
    login_button = browser.find_element(By.CSS_SELECTOR, '[type="submit"]')
    login_button.click()
    main_page_flag_1 = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "learn-last-activity-dropdown")))
    assert main_page_flag_1.is_displayed(), "False main_page_flag_1"
    main_page_flag_2 = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "navbar__profile")))
    assert main_page_flag_2.is_displayed(), "False main_page_flag_2"
