import scrapy
from bs4 import BeautifulSoup
import re
import pymongo
from pymongo import MongoClient
import io

class IndeedSpider(scrapy.Spider):
    name = "indeed-intern"
    client = MongoClient('localhost', 27017)
    count = 0
    chunk = ""
    def clean_html(self,html):
	"""
	Copied from NLTK package.
	Remove HTML markup from the given string.

	:param html: the HTML string to be cleaned
	:type html: str
	:rtype: str
	"""

	# First we remove inline JavaScript/CSS:
	cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
	# Then we remove html comments. This has to be done before removing regular
	# tags since comments can contain '>' characters.
	cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
	# Next we can remove the remaining tags:
	cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
	# Finally, we deal with whitespace
	cleaned = re.sub(r"&nbsp;", " ", cleaned)
	cleaned = re.sub(r"  ", " ", cleaned)
	cleaned = re.sub(r"  ", " ", cleaned)
	return cleaned.strip()

    def start_requests(self):
        urls = [
            'https://www.indeed.com/jobs?q=software+intern&l=Sunnyvale%2C+CA',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parseMore(self, response):
	html = response.css('body').extract_first()
	html = self.clean_html(html)
	soup = BeautifulSoup(html)
	db = self.client.indeed
	self.chunk = self.chunk + soup.get_text()
	jobItem = {"title" : response.meta['title'], 
		   "company" : response.meta['company'],
		   "detailUrl" : response.meta['detailUrl'],
		   "desp" : soup.get_text()}
	jobId = db.intern.insert_one(jobItem).inserted_id
	self.count = self.count + 1
	print self.count



    def parse(self, response):
        jobResults = response.css('div.row.result')
	for jobResult in  jobResults:
		title = jobResult.css('a.turnstileLink::attr(title)').extract_first()
		company = jobResult.css('span.company').css('a::text').extract_first()
		if not company or not company.strip():
			company = jobResult.css('span.company').css('span::text').extract_first()
		if not company or not company.strip():
			company = jobResult.css('span.company').css('span.span::text').extract_first()
		detailUrl = jobResult.css('a.turnstileLink').css('a::attr(href)').extract_first()
		
		if title:
			title = title.strip()
		if company:
			company = company.strip()
		if detailUrl:
			detailUrl = detailUrl.strip()
		if detailUrl.startswith('/'):
			detailUrl = "https://www.indeed.com" + detailUrl
		if detailUrl:
			request =  scrapy.Request(url=detailUrl, callback=self.parseMore)
			request.meta['title'] = title
			request.meta['company'] = company
			request.meta['detailUrl'] = detailUrl
			yield request
		next_page = response.css('div.pagination').css('a')[-1].css('a::attr(href)').extract_first()
		
		
		if self.count > 1000:
			filename = 'train_data.txt'
			#print(self.chunk)
			with io.open(filename, 'w', encoding='utf-8') as file:
				file.write(self.chunk) 
				self.log('Saved file %s' % filename)
			return 
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
		else:
			print "next none, bye bye"

