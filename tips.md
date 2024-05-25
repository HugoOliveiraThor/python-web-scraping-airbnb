# Used when try to find the element and click them

```python
local = WebDriverWait(browser, TIME_TO_WAIT).until(
     EC.presence_of_element_located((By.ID, 'bigsearch-query-location-input'))
 )
 local.send_keys("João Pessoa - PB")


 checkin = WebDriverWait(browser, TIME_TO_WAIT).until(
     EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='structured-search-input-search-button']"))
 )
 checkin.click()
 ```