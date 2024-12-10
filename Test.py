import json
import os
import time  # Import time module for delays
from helperfunctions import BrowserHelpers
from selenium.webdriver.common.by import By

# Load test data
# Reads test input data and element selectors from an external JSON file
with open("test_data.json", "r") as file:
    data = json.load(file)

# Extract selectors for elements used in tests
selectors = data["selectors"]

# Converts the relative path of the base file which is the QE-index.html to a URL format the browser can navigate to since browser.get expects a url
base_url = f"file://{os.path.abspath(data['base_url'])}"

# Logger function to log test results
# Prints whether a test passed or failed, and provides an error message if it failed
def log_test_result(test_name, status, error_message=None):
    if status:
        print(f"{test_name}: PASSED")
    else:
        print(f"{test_name}: FAILED")
        if error_message:
            print(f"Error: {error_message}")

# Test Functions
# Each function represents a specific test case

# Test 1: Verify Login Elements
# Simulates a login action by entering email and password into the input fields and verifying their presence
def test_1(email, password):
    browser = BrowserHelpers()  # Initialize the browser
    try:
        browser.open_browser(base_url)  # Open the browser to the base URL
        time.sleep(2)
        browser.wait_for_page_load(By.ID, selectors["test_1"]["email_input"])  # Wait for the email input to load
        time.sleep(1)
        browser.find_element(By.ID, selectors["test_1"]["email_input"])  # Verify email input is present
        time.sleep(1)
        browser.find_element(By.ID, selectors["test_1"]["password_input"])  # Verify password input is present
        browser.find_element(By.XPATH, selectors["test_1"]["login_button"])  # Verify login button is present
        time.sleep(1)
        browser.send_keys(By.ID, selectors["test_1"]["email_input"], email)  # Enter email
        browser.send_keys(By.ID, selectors["test_1"]["password_input"], password)  # Enter password
        time.sleep(2)
        log_test_result("Test 1", True)  # Log the result as passed
    except Exception as e:
        log_test_result("Test 1", False, str(e))  # Log the result as failed with an error
    finally:
        browser.quit_browser()  # Close the browser

# Test 2: Verify List Items
# Checks that the correct number of list items are displayed and their content matches the expected values
def test_2(expected_count, second_text, second_badge):
    browser = BrowserHelpers()
    try:
        browser.open_browser(base_url)  # Open the browser to the base URL
        time.sleep(2) 
        browser.wait_for_page_load(By.ID, "test-2-div")  # Wait for the list section to load
        time.sleep(1)
        list_items = browser.find_elements(By.XPATH, selectors["test_2"]["list_items"])  # Find all list items
        assert len(list_items) == expected_count  # Verify the number of list items matches expectation
        time.sleep(1) 
        assert second_text in list_items[1].text  # Verify the text of the second list item
        badge_value = list_items[1].find_element(By.CLASS_NAME, selectors["test_2"]["badge_class"]).text
        assert badge_value == second_badge  # Verify the badge value of the second list item
        time.sleep(2) 
        log_test_result("Test 2", True)  # Log the result as passed
    except Exception as e:
        log_test_result("Test 2", False, str(e))  # Log the result as failed with an error
    finally:
        browser.quit_browser()  # Close the browser

# Test 3: Verify Dropdown Functionality
# Verifies that the default dropdown option is selected and allows selecting a new option
def test_3(default_option, new_option):
    browser = BrowserHelpers()
    try:
        browser.open_browser(base_url)  # Open the browser to the base URL
        time.sleep(2)
        browser.wait_for_page_load(By.ID, "test-3-div")  # Wait for the dropdown section to load
        time.sleep(1) 
        dropdown_button = browser.find_element(By.ID, selectors["test_3"]["dropdown_button"])  # Find the dropdown
        assert dropdown_button.text == default_option  # Verify the default option
        time.sleep(1)
        browser.click(By.ID, selectors["test_3"]["dropdown_button"])  # Open the dropdown
        browser.click(By.XPATH, selectors["test_3"]["dropdown_option"].format(new_option))  # Select the new option
        assert dropdown_button.text == new_option  # Verify the new option is selected
        time.sleep(2)
        log_test_result("Test 3", True)  # Log the result as passed
    except Exception as e:
        log_test_result("Test 3", False, str(e))  # Log the result as failed with an error
    finally:
        browser.quit_browser()  # Close the browser

# Test 4: Verify Button States
# Confirms that the first button is enabled and the second button is disabled
def test_4(first_enabled, second_enabled):
    browser = BrowserHelpers()
    try:
        browser.open_browser(base_url)  # Open the browser to the base URL
        time.sleep(2)
        browser.wait_for_page_load(By.ID, "test-4-div")  # Wait for the button section to load
        time.sleep(1)
        first_button = browser.find_element(By.XPATH, selectors["test_4"]["first_button"])  # Locate the first button
        second_button = browser.find_element(By.XPATH, selectors["test_4"]["second_button"])  # Locate the second button
        assert first_button.is_enabled() == first_enabled  # Verify the state of the first button
        time.sleep(1) 
        assert second_button.is_enabled() == second_enabled  # Verify the state of the second button
        time.sleep(2)
        log_test_result("Test 4", True)  # Log the result as passed
    except Exception as e:
        log_test_result("Test 4", False, str(e))  # Log the result as failed with an error
    finally:
        browser.quit_browser()  # Close the browser

# Test 5: Verify Success Button and Alert
# Waits for a button to appear, clicks it, and checks for a success message
def test_5():
    browser = BrowserHelpers()
    try:
        browser.open_browser(base_url)  # Open the browser to the base URL
        time.sleep(2)
        browser.wait_for_page_load(By.ID, selectors["test_5"]["test_5_div"])  # Wait for the section to load
        time.sleep(1)
        button = browser.wait_for_element(By.ID, selectors["test_5"]["button"])  # Wait for the button to appear
        time.sleep(1) 
        button.click()  # Click the button
        success_alert = browser.find_element(By.ID, selectors["test_5"]["success_alert"])  # Check for success alert
        assert success_alert.is_displayed()  # Verify the success alert is displayed
        assert not button.is_enabled()  # Verify the button is now disabled
        time.sleep(2) 
        log_test_result("Test 5", True)  # Log the result as passed
    except Exception as e:
        log_test_result("Test 5", False, str(e))  # Log the result as failed with an error
    finally:
        browser.quit_browser()  # Close the browser

# Test 6: Verify Table Cell Value
# Fetches and verifies the value of a specific cell in a grid
def test_6(row, col, expected_value):
    browser = BrowserHelpers()
    try:
        browser.open_browser(base_url)  # Open the browser to the base URL
        time.sleep(2)
        browser.wait_for_page_load(By.ID, "test-6-div")  # Wait for the table section to load
        time.sleep(1)

        def get_cell_value(row, col):
            table = browser.find_element(By.XPATH, selectors["test_6"]["grid_table"])  # Find the table
            time.sleep(1)
            return table.find_element(By.XPATH, f".//tr[{row + 1}]/td[{col + 1}]").text  # Get the cell value

        cell_value = get_cell_value(row, col)
        assert cell_value == expected_value  # Verify the cell value matches the expected value
        time.sleep(2)
        log_test_result("Test 6", True)  # Log the result as passed
    except Exception as e:
        log_test_result("Test 6", False, str(e))  # Log the result as failed with an error
    finally:
        browser.quit_browser()  # Close the browser

# Execute Tests
# Runs all test cases using the data loaded from the JSON file
test_1(data["test_1"]["email"], data["test_1"]["password"])
test_2(
    data["test_2"]["expected_list_count"],
    data["test_2"]["second_item_text"],
    data["test_2"]["second_item_badge"]
)
test_3(
    data["test_3"]["default_option"],
    data["test_3"]["new_option"]
)
test_4(
    data["test_4"]["first_button_enabled"],
    data["test_4"]["second_button_enabled"]
)
test_5()
test_6(
    data["test_6"]["cell_coordinates"][0],
    data["test_6"]["cell_coordinates"][1],
    data["test_6"]["expected_cell_value"]
)
