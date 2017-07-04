# Rajat Agrawal 
# 16200159

# Part 1. Text Data Scraping 
# This part of the assignment should be implemented as a Python script, which includes
# comments to explain your work. Tasks to be completed in your script:
# 1. Identify the URLs for all news articles listed on the website:   http://mlg.ucd.ie/modules/COMP41680/news/index.html
# 2. Retrieve all web pages corresponding to these article URLs.
# 3. From the web pages, extract the main body text containing the content of each news article. Save the body of each article as plain text.

# Import necessary libraries
import requests
from bs4 import BeautifulSoup

def dump_article_data(article):
	text_file_path = "data_dump/text_data.txt"
	# Open a text file
	text_file = open(text_file_path, "a")
	# write content into the text file
	text_file.write(article + "\n")
	# Close the text file
	text_file.close()
	# Success message
	print(len(article), "characters successfully written to text_data.txt")

def read_article_page(article_url):
	# read current article
	article_page_source = requests.get(article_url)
	# parse article page using Beautiful Soup
	article_parsed_page = BeautifulSoup(article_page_source.text, "lxml")
	# fetch all the div content of main class.
	main_div_content = article_parsed_page.find("div", { "class" : "main" })
	# strip and write the main content of the page
	dump_article_data(" ".join(main_div_content.text.split()))
	
def read_month_page(month_url):
	# Open month page
	month_page_source = requests.get(month_url)
	# Parse month page using Beautiful Soup
	month_parsed_page = BeautifulSoup(month_page_source.text, "lxml")
	# title file path
	title_file_path = "data_dump/title_data.txt"
	# Open a title text file
	title_text_file = open(title_file_path, "a")
	# Parse thru each <li>
	for li in month_parsed_page.find_all("li"):
		# Check if <li> has <a>, then fetch data.
		if li.find('a'):
			# Get article href info from each <li> and <a>
			article_info = li.find("a")["href"]
			# Fetch titles
			title = li.text
			# write content into the text file
			title_text_file.write(str(title) + "\n")
			print("Title:", title, ",written successfully.")
			# Before we append article_url to the month_url, we need to trim "month-xxx.html"
			# "month-xxx.html" has 14 characters, so we can trim this and append with article_info
			trimmed_month_url = month_url[:-14]
			# create full article url
			article_url = trimmed_month_url + article_info
			# You can check the response code for each page by following commented code
			# response = requests.get(article_url)
			# print(response)
			read_article_page(article_url)
	# Close the text file
	title_text_file.close()

def read_index_page(page_url):
	# Read the website
	page_source = requests.get(page_url)
	# Parse source code using Beautiful Soup
	parsed_page = BeautifulSoup(page_source.text, "lxml")
	# Parse thru each <li>
	for li in parsed_page.find_all("li"):
		# Get month href info from each <li> and <a>
		month_info = li.find("a")["href"]
		# Before we append month_url to the page_url, we need to trim "index.html" from page url
		# "index.html" has 10 characters, so we can trim this and append with month_info
		trimmed_page_url = page_url[:-10]
		# create full url for the given month
		month_url = trimmed_page_url + month_info
		# call read_month_page(month_url) function to read each month data individually.
		read_month_page(month_url)

# web url we want to scrape
page_url = "http://mlg.ucd.ie/modules/COMP41680/news/index.html"
# calling read_index_page function to scrape the index page.
read_index_page(page_url)