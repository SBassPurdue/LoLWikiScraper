from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd


options = Options()
options.headless = True
print("Initializing webdriver", end="... ", flush=True)
driver = webdriver.Firefox(options=options)
print("Done.") #Finished initializing webdriver

print("Fetching list of champions", end="... ", flush=True)
driver.get("https://leagueoflegends.fandom.com/wiki/List_of_champions")
content = driver.page_source
print("Done.") #Finished fetching list of champions

print("Parsing list of champions", end="... ", flush=True)
soup = BeautifulSoup(content, features="html.parser")
table = soup.find('table', attrs={'class':'wikitable sortable jquery-tablesorter'})
table = table.tbody
print("Done.") #Finished parsing list of champions

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
            print("Fetching " + champ_name, end="... ", flush=True)
            driver.get(link)
            content = driver.page_source
            print("Parsing " + champ_name, end="... ", flush=True)
            quotesoup = BeautifulSoup(content, features="html.parser") #new soup to parse each champ's page
            successful_parse = True
            print("Done") #Finished fetching and parsing champion's quotes
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
print("Exporting to csv...")
frame = pd.DataFrame.from_dict(quotes_dict, orient='index')
frame.to_csv('quotes.csv', encoding='utf-8')
print("Results stored in quotes.csv")
