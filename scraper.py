from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd


options = Options()
options.headless = True
print("Initializing webdriver...")
driver = webdriver.Firefox(options=options)

print("Fetching list of champions...")
driver.get("https://leagueoflegends.fandom.com/wiki/List_of_champions")
#driver.get("file:///home/surrept/Desktop/league.html")
content = driver.page_source

print("Parsing list of champions...")
soup = BeautifulSoup(content, features="html.parser")

table = soup.find('table', attrs={'class':'wikitable sortable jquery-tablesorter'})
#table = soup.find('table', attrs={'class':'wikitable sortable'})
table = table.tbody

quotes_dict = {}
row = table.tr
while row is not None:
    link = row.a['href']
    champ_name = link[6:]
    print("Parsing " + champ_name)

    link = "https://leagueoflegends.fandom.com" + link + "/LoL/Audio"
    driver.get(link)
    content = driver.page_source
    quotesoup = BeautifulSoup(content, features="html.parser") #new soup to parse each champ's page
    quotes_raw = quotesoup.findAll('i')
    quotes = []

    for quote in quotes_raw:
        quotes.append(quote.string)

    quotes_dict[champ_name] = quotes

    row.extract() #remove the row from the table to parse the next one
    row = table.tr

print("Exporting to csv")
frame = pd.DataFrame.from_dict(quotes_dict, orient='index')
frame.to_csv('quotes.csv', index=False, encoding='utf-8')
