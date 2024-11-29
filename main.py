from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Chrome()
driver.get("https://taxireg.infosys.bg/pub/register")
time.sleep(3)

previous_height = driver.execute_script('return document.body.scrollHeight')
element = driver.find_element(By.TAG_NAME, 'body')
while True:
    k = 0
    while previous_height > k:
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)
        k += 1
    elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'ЕИК')]")
    eik_set = set()
    for el in elements:
        eik_set.add(el.text.strip())
    # Print the extracted ЕИК values
    print("\nExtracted ЕИК Elements:")
    for eik in sorted(eik_set):  # Sort for readability
        print(eik)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == previous_height:
        break
    previous_height = new_height

# Extract all ЕИК elements after scrolling
elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'ЕИК')]")
eik_set = set()
for element in elements:
    eik_set.add(element.text.strip())

# Print the extracted ЕИК values
print("\nExtracted ЕИК Elements:")
for eik in sorted(eik_set):  # Sort for readability
    print(eik)

# Close the browser
driver.quit()
