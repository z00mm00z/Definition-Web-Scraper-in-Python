from bs4 import BeautifulSoup
import requests
import csv

exceptions = []
words = []
definitions = []
exceptionsCount = 0

dataFile = open('WORD_DATA_LEN_5.csv', 'r')
outputWordFile = open('OUTPUT_DATA.csv', 'w')
type(dataFile)

csvreader = csv.reader(dataFile, delimiter=',')
csvwriter = csv.writer(outputWordFile, delimiter=',')

print("If Google's HTML code is changed, this script may need to be updated.")
print("Definitions are scraped from Google, Dictionary.com and Merriam Webster.")

def Scrape(query, defIn, source):
    print(query)
    words.append(query)
    definitions.append(defIn)
    print('Source: ' + source)
    print(defIn)


for row in csvreader:
    query = row[0]
    
    print('---------')
    try:
        url = f'https://google.com/search?q={query}+definition&oq=help+defin&aqs=chrome.0.69i59j69i57l3j0i271j69i60l3.1869j0j7&sourceid=chrome&ie=UTF-8'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        definition = soup.find('div', attrs={'class':'BNeawe s3v9rd AP7Wnd'}).find('div', attrs={'class':'v9i61e'}).get_text()

        Scrape(query, definition, 'https://google.com')
    except (AttributeError, requests.exceptions.TooManyRedirects) as e:
        try:
            url = f'https://dictionary.com/browse/{query}'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")

            definition = soup.find('span', attrs={'class':'one-click-content css-nnyc96 e1q3nk1v1'}).get_text()
            Scrape(query, definition, 'https://dictionary.com')
        except (AttributeError, requests.exceptions.TooManyRedirects) as e:
            try:
                url = f'https://merriam-webster.com/dictionary/{query}'
                r = requests.get(url)
                soup = BeautifulSoup(r.content, "html.parser")

                definition = soup.find('span', attrs={'class':'dtText'}).get_text()
                definition = definition.replace(": ", "")

                Scrape(query, definition, 'https://merriam-webster.com')
            except (AttributeError, requests.exceptions.TooManyRedirects):
                print('FAILED: definition for "' + str(query) + '" could not be found.')
                exceptionsCount += 1
                exceptions.append(query)
        
for i in range(len(words)):
    csvwriter.writerow([words[i], definitions[i]])
    
if exceptionsCount != 0:
    print('---------')
    print(str(exceptionsCount) + ' definition(s) could not be found.')
    for exception in exceptions:
        print(exception)
        answer = input('Add now? (y/n): ', )
        if answer == 'y':
            defIn = input('Definition: ', )
            csvwriter.writerow([exception, defIn])
            

dataFile.close()
outputWordFile.close()

print(f'Done. {len(definitions)} definition(s) found. {exceptionsCount} execption(s) handled.')
    
    

