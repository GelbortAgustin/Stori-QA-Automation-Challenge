from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def navigate_to_practice_page(context):
    context.driver.get("https://rahulshettyacademy.com/AutomationPractice/")

def select_suggestion(context, input_text, suggestion_text):
    suggestion_input = context.driver.find_element(By.ID, 'autocomplete')
    suggestion_input.clear()
    suggestion_input.send_keys(input_text)
    
    # Wait for suggestions to load
    suggestions = WebDriverWait(context.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//li[@class='ui-menu-item']/div"))
    )
    
    for suggestion in suggestions:
        if suggestion_text in suggestion.text:
            suggestion.click()
            break
    else:
        raise ValueError(f"Suggestion '{suggestion_text}' not found")

@given('I navigate to the practice page')
def step_impl(context):
    navigate_to_practice_page(context)

@when('I enter "{input_text}" in the suggestion box')
def step_impl(context, input_text):
    context.input_text = input_text

@when('I select "{suggestion_text}" from the suggestions')
def step_impl(context, suggestion_text):
    select_suggestion(context, context.input_text, suggestion_text)

@then('the suggestion box should contain "{suggestion_text}"')
def step_impl(context, suggestion_text):
    suggestion_input = context.driver.find_element(By.ID, 'autocomplete')
    assert suggestion_text in suggestion_input.get_attribute('value')

@when('I select option {index:d} from the dropdown')
def step_impl(context, index):
    dropdown = context.driver.find_element(By.ID, 'dropdown-class-example')
    select = Select(dropdown)
    select.select_by_index(index)
    context.selected_option = select.first_selected_option.text

@then('the dropdown should display "{expected_text}"')
def step_impl(context, expected_text):
    assert context.selected_option == expected_text

@when('I click on "open window" button')
def step_impl(context):
    context.driver.find_element(By.ID, 'openwindow').click()

@when('I switch to the new window')
def step_impl(context):
    context.driver.switch_to.window(context.driver.window_handles[1])

@then('the new window should contain "{expected_text}"')
def step_impl(context, expected_text):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{expected_text}')]"))
    )
    assert expected_text in context.driver.page_source

@when('I close the new window')
def step_impl(context):
    context.driver.close()

@when('I switch back to the original window')
def step_impl(context):
    context.driver.switch_to.window(context.driver.window_handles[0])

@when('I click on "open tab" button')
def step_impl(context):
    context.driver.find_element(By.ID, 'opentab').click()

@then('the new tab should display the home button')
def step_impl(context):
    context.driver.switch_to.window(context.driver.window_handles[1])
    button = context.driver.find_element(By.XPATH, "//button[contains(text(),'Home')]")
    assert button.is_displayed()

@then('I take a screenshot named "{filename}"')
def step_impl(context, filename):
    context.driver.save_screenshot(filename)

@when('I switch back to the original tab')
def step_impl(context):
    context.driver.switch_to.window(context.driver.window_handles[0])

@when('I enter "{text}" in the alert input box')
def step_impl(context, text):
    alert_input = context.driver.find_element(By.ID, 'name')
    alert_input.clear()
    alert_input.send_keys(text)

@when('I click on "alert" button')
def step_impl(context):
    context.driver.find_element(By.ID, 'alertbtn').click()

@then('an alert should display "{expected_text}"')
def step_impl(context, expected_text):
    alert = context.driver.switch_to.alert
    assert expected_text in alert.text

@when('I accept the alert')
def step_impl(context):
    alert = context.driver.switch_to.alert
    alert.accept()

@when('I click on "confirm" button')
def step_impl(context):
    context.driver.find_element(By.ID, 'confirmbtn').click()

@then('a confirmation alert should display "{expected_text}"')
def step_impl(context, expected_text):
    alert = context.driver.switch_to.alert
    assert expected_text in alert.text

@when('I check the web table for course costs')
def step_impl(context):
    context.rows = context.driver.find_elements(By.XPATH, "//table[@name='courses']//tr")

@then('I should find a course costing ${cost}')
def step_impl(context, cost):
    for row in context.rows[1:]:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns[2].text == cost:
            print(f"Course costing ${cost}: {columns[1].text}")
            break
    else:
        raise AssertionError(f"Course costing ${cost} not found")

@when('I check the fixed header web table')
def step_impl(context):
    context.rows = context.driver.find_elements(By.XPATH, "//table[@id='product']//tr")

@then('I should find an {title}')
def step_impl(context, title):
    for row in context.rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) > 0 and title in columns[2].text:
            print(f"{title}: {columns[0].text}")
            break
    else:
        raise AssertionError(f"{title} not found")

@when('I switch to the iframe')
def step_impl(context):
    iframe = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "courses-iframe"))
    )
    context.driver.switch_to.frame(iframe)

@then('I should see the text "{expected_text}"')
def step_impl(context, expected_text):
    text_element = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{expected_text}')]"))
    )
    assert expected_text in text_element.text

@when('I switch back to the default content')
def step_impl(context):
    context.driver.switch_to.default_content()
