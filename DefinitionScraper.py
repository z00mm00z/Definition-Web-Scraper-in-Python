from bs4 import BeautifulSoup
import requests
import csv

exceptions = []
exceptionNo = 0

dataFile = open('WORD_DATA_LEN_5.csv', 'r')
outputWordFile = open('OUTPUT_DATA.csv', 'w')
type(dataFile)

csvreader = csv.reader(dataFile, delimiter=',')
csvwriterWords = csv.writer(outputWordFile, delimiter=',')

print("If Google's HTML code is changed, this script may need to be updated.")
print("Definitions are scraped from Google, Dictionary.com and Merriam Webster.")

for row in csvreader:
    query = row[0]
    
    print('---------')
    print(query)
    try:
        url = f'https://google.com/search?q={query}+definition&oq=help+defin&aqs=chrome.0.69i59j69i57l3j0i271j69i60l3.1869j0j7&sourceid=chrome&ie=UTF-8'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        definition = soup.find('div', attrs={'class':'BNeawe s3v9rd AP7Wnd'}).find('div', attrs={'class':'v9i61e'}).get_text()
        print('Source: https://google.com')
        print(definition)
    except AttributeError as e:
        try:
            url = f'https://dictionary.com/browse/{query}'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")

            definition = soup.find('span', attrs={'class':'one-click-content css-nnyc96 e1q3nk1v1'}).get_text()
            print('Source: https://dictionary.com')
            print(definition)
        except (AttributeError, requests.exceptions.TooManyRedirects) as e:
            try:
                url = f'https://merriam-webster.com/dictionary/{query}'
                r = requests.get(url)
                soup = BeautifulSoup(r.content, "html.parser")

                definition = soup.find('span', attrs={'class':'dtText'}).get_text()
                definition = definition.replace(": ", "")
                print('Source: https://merriam-webster.com')
                print(definition)
            except AttributeError:
                print('FAILED: definition for "' + str(query) + '" could not be found.')
                exceptionNo += 1
                exceptions.append(query)
    except requests.exceptions.TooManyRedirects: 
        print('Too many redirects') 
        



for i in exceptions:
    print(exceptions[i])

dataFile.close()
outputWordFile.close()
    
    

