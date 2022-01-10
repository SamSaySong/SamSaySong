# import the libs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
# create the initial window
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--headless")
chrome_options.add_experimental_option('w3c', False)
chrome_options.add_experimental_option(
    "excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(
    executable_path=r"D:\Win\Train Python\wwin-01\selenium01\chromedriver.exe", chrome_options=chrome_options)

# go to the home page
driver.get('https://www.zomato.com/vi/ncr')

# storing the current window handle to get back to dashbord
main_page = driver.current_window_handle

# wait for page to load completely
sleep(5)

# click on the sign in tab
driver.find_element_by_xpath("//a[contains(text(),'Log in')]").click()

sleep(5)

# click to log in using gg
driver.find_element_by_xpath("//span[contains(text(),'Continue with Google')]").click()
sleep(5)
# changing the handles to access login page 
for handle in driver.window_handles:
    if handle != main_page:
        login_page = handle

# change the control to signin page
driver.switch_to.window(login_page)


# # enter the email
# driver.find_element_by_xpath('//*[@id ="email"]').send_keys('132123')

# # enter the password
# driver.find_element_by_xpath('//*[@id ="pass"]').send_keys('65465456')

# # click the login button
# driver.find_element_by_xpath('//*[@id ="u_0_0"]').click()


# change control to main page
driver.switch_to.window(main_page)

sleep(10)
# print user name


# closing the window
driver.quit()
