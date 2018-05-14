from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import sys
from Tour import TourInfo
from bs4 import BeautifulSoup as bs

main_url = 'http://tour.interpark.com/'
keyword='로마'
tour_list = []
#chromedriver path
driver = wd.Chrome(executable_path='../chromedriver')

#load driver and open chrome browser
driver.get(main_url)

#find search window and input keyword
driver.find_element_by_id('SearchGNBText').send_keys(keyword)

#find search button css(id) and click event
driver.find_element_by_css_selector('.search-btn').click()

#waiting for loading display result in chrome browser
try:
    #waiting
    element = WebDriverWait(driver,10).until(
        #1 element -> exit
        EC.presence_of_element_located(By.CLASS_NAME, 'oTravelBox')
    )
except Exception as e:
    print('error', e)

#implicityly wait
driver.implicitly_wait(10)

#more button css click
driver.find_element_by_css_selector('.oTravelBox>.boxList>.moreBtnWrap>.moreBtn').click()

#move page
#TODO: use while and click next to end page
for page in range(1, 2 ):#16
    try:
        # execute javascript (move next page)
        driver.execute_script("searchModule.SetCategoryList(%s, '')" % page)
        time.sleep(2)
        #product info
        boxItems = driver.find_elements_by_css_selector('.oTravelBox>.boxList>li')
        #get item
        for li in boxItems:
            #set TourInfo
            obj = TourInfo(
                li.find_element_by_css_selector('h5.proTit').text,
                li.find_element_by_css_selector('.proPrice').text,
                li.find_elements_by_css_selector('.info-row .proInfo')[1].text,
                li.find_element_by_css_selector('a').get_attribute('onclick'),
                li.find_element_by_css_selector('img').get_attribute('src')
            )
            #add item
            tour_list.append(obj)
    except Exception as e1:
        print('error', e1)

#item parsing and extract final item
for tour in tour_list:
    arr = tour.link.split(',')
    if arr:
        link = arr[0].replace('searchModule.OnClickDetail(', '')
        detail_url = link[1:-1]
        driver.get(detail_url)
        time.sleep(2)
        soup = bs(driver.page_source, 'html.parser')
        data = soup.select('.tip-cover')
        content_final = ''
        for c in data[0].contents:
            content_final += str(c)
        content_final = re.sub("'", '"', content_final)
        content_final = re.sub(re.compile(r'\r\n|\r|\n|\n\r+'), '', content_final)
        # print(content_final)

driver.close()
driver.quit()
sys.exit()