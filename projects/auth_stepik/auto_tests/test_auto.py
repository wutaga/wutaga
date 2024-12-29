import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Fixture for browser initialization
@pytest.fixture
def browser(request):
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    if request.config.getoption("--headless"):
        chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(service=service,options=chrome_options)
    browser.maximize_window()
    yield browser
    browser.quit()


def test_login_form_accessibility_SK1(browser):
    """
    check the availability of the login form
    """
    browser.get("https://stepik.org/catalog?auth=login")
    login_form = WebDriverWait(browser, 15).until(
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
    login_form = WebDriverWait(browser, 15).until(
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


@pytest.mark.parametrize(
    "case_id, email, password, error_message",
    [
        ("EXT1", "test@outlook.com", "r3XMRTJB2gn", "E-mail адрес и/или пароль не верны."),
        ("EXT2", "test@outlook.com", "r3XRXTJB2gn!!cE", "E-mail адрес и/или пароль не верны."),
        ("EXT3", "test_off@outlook.com", "r3XMRTJB2gn", "E-mail адрес и/или пароль не верны."),
        ("EXT4", "", "", "Both fields are required"),
        ("EXT5", "", "r3XRXTJB2gn!!cE", "Заполните это поле."),
        ("EXT6", "test_off@outlook.com", "", "Заполните это поле.")
    ],
    ids=[
        "EXT1: test@outlook.com, r3XMRTJB2gn, Invalid mail and password",
        "EXT2: test@outlook.com, r3XRXTJB2gn!!cE, Invalid mail",
        "EXT3: test_off@outlook.com, r3XMRTJB2gn, Invalid password",
        "EXT4: "" , "", Empty email and password",
        "EXT5: "", r3XRXTJB2gn!!cE, Empty email",
        "EXT6: test_off@outlook.com, "", Empty password"
    ]
)

def test_login_with_invalid_data(browser,case_id, email, password, error_message):
    """
    login_with_invalid_data
    """
    browser.get("https://stepik.org/catalog?auth=login")
    WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog-inner")))
    email_field = browser.find_element(By.CSS_SELECTOR, '[name="login"]')
    password_field = browser.find_element(By.CSS_SELECTOR, '[name="password"]')
    login_button = browser.find_element(By.CSS_SELECTOR, '[type="submit"]')
    if email and password:
        email_field.send_keys(email)
        password_field.send_keys(password)
        login_button.click()
        error_message_element = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[role="alert"]')))
        assert error_message_element.text == error_message, f"Test {case_id} failed: Expected {error_message}, but got {error_message_element.text}"
    elif not email and not password:
        login_button.click()
        scripts_after_click = browser.find_elements(By.CSS_SELECTOR, 'script')
        assert any("clicklogin" in script.get_attribute("innerHTML") for script in scripts_after_click), \
            f"Test {case_id} failed: Expected DOM change with 'clicklogin' script, but it was not found."
    else:
        if not email:
            password_field.send_keys(password)
            login_button.click()
            email_error = email_field.get_attribute("validationMessage")
            assert email_error == error_message, f"Test {case_id} failed: Expected {error_message}, but got {email_error}"
        if not password:
            email_field.send_keys(email)
            login_button.click()
            password_error = password_field.get_attribute("validationMessage")
            assert password_error == error_message, f"Test {case_id} failed: Expected {error_message}, but got {password_error}"