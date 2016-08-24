# ---------------------------------
# Scrape Scot Parliament data
# from the current (5th) session
# of the Scottish parliament
# May 2016 -
# ---------------------------------

# modules
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import time
from selenium.common.exceptions import NoSuchElementException

# start browser using phantomjs
url = "http://www.scottish.parliament.uk/parliamentarybusiness/28925.aspx"
driver = webdriver.PhantomJS(executable_path='C:/Program Files/phantomjs-2.1.1-windows/bin/phantomjs')
driver.get(url)

# click radio button to say that we want msp votes
select = driver.find_element_by_name('SelectVoteHistoryView$Search').click()
time.sleep(10)

# get all msp ids and hardcode a session
msp_XPATH = '//*[(@id = "SelectVoteHistoryView_ddlMSP")]'
element = driver.find_element_by_xpath(msp_XPATH)
all_options = element.find_elements_by_tag_name("option")
msps = [option.get_attribute("text") for option in all_options]
msp_ids = [option.get_attribute("value") for option in all_options]
msp_ids = msp_ids[1:len(msp_ids)] # remove leading "0"


# select a timeframe
sess = "5" # 5th parliamentary session
select = Select(driver.find_element_by_name('SelectVoteHistoryView$ddlDateRanges'))
select.select_by_value(sess)


# ---------------------------------------
# loop over MSPs
# ---------------------------------------

for i in range(len(msp_ids)):

    msp_id = msp_ids[i]
    msp = msps[i]
    print("Member of Scottish Parliament" + ": " + msp)

    # select an MSP
    select = Select(driver.find_element_by_name('SelectVoteHistoryView$ddlMSP'))
    select.select_by_value(msp_id)
    time.sleep(10)

    # read the first page of results
    html = driver.page_source
    bsObj = BeautifulSoup(html)
    print(bsObj.find("table", {"id": "SelectVoteHistoryView_grdvwResults"}).get_text())

    for page in range(6):
        page = "Page$" + str(page + 2)
        xpath = "//a[contains(@href, " + "\'" + page + "\')]"

        try:
            driver.find_element_by_xpath(xpath).click()
            time.sleep(3)
        except NoSuchElementException as e:
            print("element not found")
            break
        else:
            # read the info on that page too
            html = driver.page_source
            bsObj = BeautifulSoup(html)
            print(bsObj.find("table", {"id": "SelectVoteHistoryView_grdvwResults"}).get_text())    

# quit the driver
driver.quit()



