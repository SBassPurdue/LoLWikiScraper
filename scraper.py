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
content = driver.page_source

print("Parsing list of champions...")
soup = BeautifulSoup(content, features="html.parser")

table = soup.find('table', attrs={'class':'wikitable sortable jquery-tablesorter'})
table = table.tbody

quotes_dict = {}
row = table.tr
while row is not None:
    link = row.a['href']
    champ_name = link[6:]
    link = "https://leagueoflegends.fandom.com" + link + "/LoL/Audio"
    failed_parses = 0
    successful_parse = False
    while not successful_parse and failed_parses < 5:
        try:
            print("Fetching " + champ_name, end="... ")
            driver.get(link)
            content = driver.page_source
            print("Parsing " + champ_name)
            quotesoup = BeautifulSoup(content, features="html.parser") #new soup to parse each champ's page
            successful_parse = True
        except Exception:
            print("Timed out, trying again...")
            failed_parses = failed_parses + 1
    quotes_raw = quotesoup.findAll('i')
    quotes = []

    for quote in quotes_raw:
        quotes.append(quote.string)

    quotes_dict[champ_name] = quotes

    row.extract() #remove the row from the table to parse the next one
    row = table.tr

driver.quit()
print("Exporting to csv")
frame = pd.DataFrame.from_dict(quotes_dict, orient='index')
frame.to_csv('quotes.csv', encoding='utf-8')
