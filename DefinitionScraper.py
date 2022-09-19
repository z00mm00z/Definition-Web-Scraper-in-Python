from bs4 import BeautifulSoup
import requests
import csv

exceptions = []

file = open('WORD_DATA_LEN_5.csv')
type(file)

csvreader = csv.reader(file, delimiter=',')

print("If Google's HTML code is changed, this script may need to be updated.")

for row in csvreader:
    query = row[0]
    
    print('---------')
    try:
        url = f'https://www.google.com/search?q={query}+definition&oq=help+defin&aqs=chrome.0.69i59j69i57l3j0i271j69i60l3.1869j0j7&sourceid=chrome&ie=UTF-8'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        definition = soup.find('div', attrs={'class':'BNeawe s3v9rd AP7Wnd'}).find('div', attrs={'class':'v9i61e'}).get_text()

        print(query)
        print('Source: https://google.com')
        print(definition)
    except AttributeError: 
        try:
            url = f'https://dictionary.com/browse/{query}'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")

            definition = soup.find('span', attrs={'class':'one-click-content css-nnyc96 e1q3nk1v1'}).get_text()
            print(query)
            print('Source: https//dictionary.com')
            print(definition)
        except AttributeError:
            print('EXCEPTION: definition for "' + str(query) + '" could not be found.')
            exceptions.append(query)
    
for i in exceptions:
    print(exceptions[i])
    
    

