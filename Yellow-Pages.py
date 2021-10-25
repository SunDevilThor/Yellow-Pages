# Yellow Pages - UK 
# Tutorial from John Watson Rooney YouTube channel

import requests 
from bs4 import BeautifulSoup
import pandas as pd

main_list = []

def extract(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('div', class_= 'row businessCapsule--mainRow')

def transform(articles):
    for item in articles: 
        title = item.find('h2', class_= 'businessCapsule--name text-h2').text
        address = item.find('span', {'itemprop': 'address'}).text.strip().replace('\n', '')
        try:
            website = item.find('a', class_= 'btn btn-yellow businessCapsule--ctaItem')['href']
            if '/customerneeds/sendenquiry/sendtoone/' in website:
                website = ''
        except:
            website = ''
        try: 
            phone_number = item.find('span', class_= 'business--telephoneNumber').text.strip()
        except:
            phone_number = ''

        business = {
            'title': title, 
            'address': address, 
            'website': website, 
            'phone_number': phone_number,
        }

        main_list.append(business)
    
    return

def load():
    df = pd.DataFrame(main_list)
    df.to_csv('Yellow-Pages.csv')
    print('Items saved to CSV file.')

x = 1
for x in range(1, 10):
    print(f'Getting page: {x}')
    articles = extract(f'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=1315848789&keywords=cafes+%26+coffee+shops&location=london&pageNum={x}')
    transform(articles)
    x += 1

load()
print('Completed. Items found:', len(main_list))

