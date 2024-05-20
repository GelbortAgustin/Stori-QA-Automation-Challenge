import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Navegar por la pagina
def navigate_to_practice_page(driver):
    driver.get("https://rahulshettyacademy.com/AutomationPractice/")

# Funcion para que encuentre los paises en base a un bucle
def select_suggestion(driver, input_text, suggestion_text):
    suggestion_input = driver.find_element(By.ID, 'autocomplete')
    suggestion_input.clear()
    suggestion_input.send_keys(input_text)
    
    # Espera la carga de pagina
    suggestions = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[@class='ui-menu-item']/div"))
    )
    
    for suggestion in suggestions:
        if suggestion_text in suggestion.text:
            suggestion.click()
            break
    else:
        raise ValueError(f"Suggestion '{suggestion_text}' not found")

# 1.0 Select MEXICO
def test_select_mexico(driver):
    navigate_to_practice_page(driver)
    select_suggestion(driver, "Me", "Mexico")
    time.sleep(3)

# 1.1 Select United States (USA)
def test_select_usa(driver):
    navigate_to_practice_page(driver)
    select_suggestion(driver, "Uni", "United States (USA)")
    time.sleep(3)

# 1.2 Select United Arab Emirates
def test_select_uae(driver):
    navigate_to_practice_page(driver)
    select_suggestion(driver, "Uni", "United Arab Emirates")
    time.sleep(3)

#la idea de los test cases 1.0/1.1/1.2 es hacerlos en uno mismo, pero me daba error al querer borrar el campo y reescribir encima, por eso decidi separarlos en casos separados y que aparezcan como indiduales en el reporte

# 2. Dropdown Example
def test_dropdown_example(driver):
    navigate_to_practice_page(driver)
    dropdown = driver.find_element(By.ID, 'dropdown-class-example')
    select = Select(dropdown)
    select.select_by_index(2)  # Select option 2
    assert select.first_selected_option.text == 'Option2'

    select.select_by_index(3)  # Select option 3
    assert select.first_selected_option.text == 'Option3'

# 3. Switch Window Example TEST CASE FAILED OK
def test_switch_window_example(driver):
    navigate_to_practice_page(driver)
    driver.find_element(By.ID, 'openwindow').click()
    time.sleep(2)

    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    
    # Wait for the element containing the text to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '30 day money back guarantee')]"))
    )
    
    assert '30 day money back guarantee' in driver.page_source

    # Close the new window and switch back to the original window
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# 4. Switch Tab Example
def test_switch_tab_example(driver):
    navigate_to_practice_page(driver)
    driver.find_element(By.ID, 'opentab').click()
    time.sleep(2)

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[1])
    button = driver.find_element(By.XPATH, "//button[contains(text(),'Home')]")
    driver.save_screenshot('switch_tab_example.png')

    # Switch back to the original tab
    driver.switch_to.window(driver.window_handles[0])

# 5. Switch to Alert Example
def test_switch_to_alert_example(driver):
    navigate_to_practice_page(driver)
    alert_input = driver.find_element(By.ID, 'name')
    alert_input.send_keys("Stori Card")
    driver.find_element(By.ID, 'alertbtn').click()

    alert = driver.switch_to.alert
    print(alert.text)
    alert.accept()

    alert_input.send_keys("Stori Card")
    driver.find_element(By.ID, 'confirmbtn').click()

    alert = driver.switch_to.alert
    assert alert.text == "Hello Stori Card, Are you sure you want to confirm?"
    print(alert.text)
    alert.accept()

# 6. Web Table Example
def test_web_table_example(driver):
    navigate_to_practice_page(driver)
    rows = driver.find_elements(By.XPATH, "//table[@name='courses']//tr")
    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns[2].text == "25":
            print(f"Course costing $25: {columns[1].text}")
        if columns[2].text == "15":
            print(f"Course costing $15: {columns[1].text}")

# 7. Web Table Fixed Header Example
def test_web_table_fixed_header_example(driver):
    navigate_to_practice_page(driver)
    rows = driver.find_elements(By.XPATH, "//table[@id='product']//tr")
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) > 0 and "Engineer" in columns[2].text:
            print(f"Engineer: {columns[0].text}")
        if len(columns) > 0 and "Businessman" in columns[2].text:
            print(f"Businessman: {columns[0].text}")

# 8. iFrame Example
def test_iframe_example(driver):
    navigate_to_practice_page(driver)
    
    # Switch to iframe
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "courses-iframe"))
    )
    driver.switch_to.frame(iframe)
    
    # Esperar a que el elemento este cargado para ser mostrado
    text_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'We are essentially a Full Stack QA consulting and Training company and we got you covered for your test implementation and training needs.')]"))
    )
    text = text_element.text
    print(text)
    
    driver.switch_to.default_content()
