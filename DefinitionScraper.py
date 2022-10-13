from bs4 import BeautifulSoup
import requests
import csv

#DECLERATIONS
exceptions = []
words = []
definitions = []
exceptionsCount = 0

#GET FILE TO READ
userInput = input('File to use, e.g. WORD_DATA_LEN_5.csv: ', )

#OPEN FILES
dataFile = open(userInput, 'r')
outputWordFile = open('OUTPUT_DATA.csv', 'w')
type(dataFile)

#INITIALIZE CSV R/W
csvreader = csv.reader(dataFile, delimiter=',')
csvwriter = csv.writer(outputWordFile, delimiter=',')

#STORES LENGTH OF SOURCE FILE
fileLength = 0
for i in csvreader:
    fileLength += 1

#RE-INITIALIZE SOURCE FILE
dataFile = open(userInput, 'r')
csvreader = csv.reader(dataFile, delimiter=',')

#START INFORMATION
print(f"Finding definitions for {fileLength} lines. \n")
print("If Google's HTML code is changed, this script may need to be updated.")
print("Definitions are scraped from Google, Dictionary.com and Merriam Webster.\n")

#DISPLAYS SCRAPE INFO
def ScrapeInfo(query, defIn, source):
    print(str(csvreader.line_num) + ' - ' + query)
    words.append(query)
    definitions.append(defIn)
    print('Source: ' + source)
    print(defIn)

#CORE SCRAPING ALGORITHM
for row in csvreader:
    query = row[0]
    
    print('---------')
    try:
        url = f'https://google.com/search?q={query}+definition&oq=help+defin&aqs=chrome.0.69i59j69i57l3j0i271j69i60l3.1869j0j7&sourceid=chrome&ie=UTF-8'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        definition = soup.find('div', attrs={'class':'BNeawe s3v9rd AP7Wnd'}).find('div', attrs={'class':'v9i61e'}).get_text()

        ScrapeInfo(query, definition, 'https://google.com')
    except (AttributeError, requests.exceptions.TooManyRedirects) as e:
        try:
            url = f'https://dictionary.com/browse/{query}'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")

            definition = soup.find('span', attrs={'class':'one-click-content css-nnyc96 e1q3nk1v1'}).get_text()

            ScrapeInfo(query, definition, 'https://dictionary.com')
        except (AttributeError, requests.exceptions.TooManyRedirects) as e:
            try:
                url = f'https://merriam-webster.com/dictionary/{query}'
                r = requests.get(url)
                soup = BeautifulSoup(r.content, "html.parser")

                #REMOVES UNWANTED SCRAPED CHARACTERS 
                definition = soup.find('span', attrs={'class':'dtText'}).get_text()
                definition = definition.replace(": ", "")

                ScrapeInfo(query, definition, 'https://merriam-webster.com')
            except (AttributeError, requests.exceptions.TooManyRedirects):
                print('FAILED: definition for "' + str(query) + '" could not be found.')
                exceptionsCount += 1
                exceptions.append(query)

#WRITING WORDS AND DEFINITIONS TO OUTPUT FILE      
for i in range(len(words)):
    csvwriter.writerow([words[i], definitions[i]])

#EXCEPTION HANDLER
if exceptionsCount != 0:
    print('---------')
    print(str(exceptionsCount) + ' definition(s) could not be found.')
    for exception in exceptions:
        print(exception)
        answer = input('Add now? (y/n): ', )
        if answer == 'y':
            defIn = input('Definition: ', )
            csvwriter.writerow([exception, defIn])
            
#CLOSES FILES
dataFile.close()
outputWordFile.close()

#PRINT FINAL INFO
print(f'\nDone. {len(definitions)} definition(s) found. {exceptionsCount} execption(s) handled.')
    
    

