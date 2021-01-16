from selenium import webdriver 
from time import sleep as sl 
import csv

driver = webdriver.Chrome()
driver.get('https://www.imovie4u.com/')
sl(0.5)

mvtList = driver.find_elements_by_xpath('//div[@id="mCSB_1_container"]/div/div[2]/nav/ul/li/a')

for tp in mvtList:
	title = tp.text
	if title == "情色" or title == "寫真":
		continue
	url = tp.get_attribute('href')
	with open("movie.csv", "a+", newline="", encoding="utf-8") as f:
		writer = csv.writer(f)
		writer.writerow([title, url])
driver.quit()