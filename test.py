from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://taxireg.infosys.bg/pub/register")

#THIS CODE IS JUST CHECKING IF THE SCROLL AUTOMATION WORKS OR NOT. THE PRINT STATEMENT WOULD RETURN TRUE IF IT DOES BUT IT CURRENTLY RETURNS FALSE BECAUSE THE PAGE HEIGHT STAYS THE SAME!!!

# Get initial scroll height
initial_height = driver.execute_script("return document.documentElement.scrollHeight")

# Scroll to the bottom
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Wait for new content to load
try:
    WebDriverWait(driver, 10).until(
        lambda d: driver.execute_script("return document.documentElement.scrollHeight") > initial_height
    )
except:
    print("New content did not load.")

# Get updated scroll height
updated_height = driver.execute_script("return document.documentElement.scrollHeight")

# Compare heights
print(f"Initial Height: {initial_height}")
print(f"Updated Height: {updated_height}")
print("Did scrolling load more content?", updated_height > initial_height)

# Quit driver
driver.quit()
