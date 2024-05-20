import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests on")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def driver(browser):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(options=options)
    elif browser == "opera":
        options = webdriver.OperaOptions()
        driver = webdriver.Opera(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.set_window_size(360, 640)  # Set window size to emulate mobile device
    yield driver
    driver.quit()
