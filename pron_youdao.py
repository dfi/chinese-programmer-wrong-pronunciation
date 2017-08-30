from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
# from time import sleep


BASE_URL_YOUDAO = 'http://dict.youdao.com/w/eng/'
WORD            = 'perfect'
XPATH_STRING    = '//a[@data-rel[contains(., "&type=1")]]'


browser = webdriver.Chrome()
input_word = input('Enter your word: ')
url = BASE_URL_YOUDAO + input_word
browser.get(url)

try:
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, XPATH_STRING)))
except NoSuchElementException:
    print('Could not find the element.')
else:
    uk_hover = browser.find_element_by_xpath(XPATH_STRING)
    action = ActionChains(browser)
    action.move_to_element(uk_hover).perform()

    # https://gist.github.com/dariodiaz/3104601
    def apply_style(driver, style):
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            uk_hover,
            style
        )
    original_style = uk_hover.get_attribute('style')
    hightlighted_style = "border: 3px dotted red;"
    apply_style(browser, hightlighted_style)
    # sleep(2)
    # apply_style(browser, original_style)