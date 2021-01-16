from selenium import webdriver
from time import sleep as sl 
from selenium.webdriver.chrome.options import Options 
import csv
import requests
from lxml import etree

class crawler:
	def __init__(self):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		#取消沙盒模式，解决DevToolsActivePort文件不存在的报错
		chrome_options.add_argument("--no-sandbox")
		#克服有限的资源问题  【但是用于Linux系统】
		chrome_options.add_argument("--disable-dev-shm-usage")
		#避免讓外面訪問，設立私有屬性
		self.__driver = webdriver.Chrome(chrome_options=chrome_options)
		self.__infomation = """
			Benson Linebot v1
			1.dcard
			2.imovie4u
			3.yahoo stock
		"""

	#回傳我們所設置的資訊
	@property
	def infomation(self):
		self.__close()
		return self.__infomation

	def get_forumList(self):
		forumList = []
		with open("forum.csv", "r", encoding="utf-8") as f:
			for line in f.readlines():
				if line == "\n":
					continue
				forumList.append(line)
		return forumList

	def __close(self):
		sl(0.5)
		self.__driver.close()
	
	def crawl_specific_forum(self, name):
		forumList = self.get_forumList()
		for i in forumList:
			if i.split(",")[0] in name:
				link = i.split(",")[1]
				break
		else:
			self.__close()
			return "無此看板"

		self.__driver.get(link)
		sl(0.5)
		r_list = self.__driver.find_elements_by_xpath('//div[@id="__next"]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div')
		xStr = ""
		for article in r_list:
			try:
				title = article.find_element_by_xpath('./article/h2/a/span').text
				href = article.find_element_by_xpath('./article/h2/a').get_attribute('href')
				motion = article.find_element_by_xpath('./article/div[3]/div[1]/div/div[2]').text
				response = article.find_element_by_xpath('./article/div[3]/div[2]/span[2]').text
				xStr += "\n".join([title, href, motion, response])
			except Exception as e:
				pass 
		self.__close()
		return xStr

	def crawl_movie_types(self, name):
		mvStr = ""
		if name == "找電影":
			with open("movie.csv", "r", encoding="utf-8") as f:
				for line in f.readlines():
					line = "\n".join(line.split(","))
					mvStr += line
				self.__close()
				return mvStr
		
		url = "https://www.imovie4u.com"
		res = requests.get(url)
		res.encoding = "utf-8"
		html = res.text
		parseHtml = etree.HTML(html)
		mvList = parseHtml.xpath('//div[@id="featured-titles"]/article')
		for mv in mvList:
			rating = mv.xpath('./div[1]/div[1]/text()')[0][1:]
			title = mv.xpath('./div[2]/h3/a')[0].text
			year = mv.xpath('./div[2]/span')[0].text
			url = mv.xpath('./div[2]/h3/a/@href')[0]
			mvStr += " ".join([rating, title, year]) + "\n" + url + "\n"
		sl(0.5)
		self.__close()
		return mvStr
	
	def crawl_stock(self, name):
		self.__driver.get('https://tw.stock.yahoo.com/')
		sl(0.5)

		stockInput = self.__driver.find_element_by_id("stock_id")
		stockInput.send_keys(name)
		sl(1)
		skStr = ""
		try:
			url = self.__driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/a').get_attribute("data-href")
		except Exception as e:
			self.__close()
			return "無此公司股票"
		
		skStr += name + "\n" + url
		self.__close()
		return skStr
