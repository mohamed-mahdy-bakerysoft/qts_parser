import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://quotes.toscrape.com/'
page = requests.get(base_url)
soup = BeautifulSoup(page.text, 'html.parser')
quotes = []

next_li_element = soup.find('li', class_='next')

while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']
    page = requests.get(base_url + next_page_relative_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    quote_elements = soup.find_all('div', class_='quote')

    for quote_element in quote_elements:
        text = quote_element.find('span', class_='text').text
        author = quote_element.find('small', class_='author').text
        tags = [tag_element.text for tag_element in
                quote_element.find('div', class_='tags').find_all('a', class_='tag')]

        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags)
            }
        )
    next_li_element = soup.find('li', class_='next')

with open('qts_parser.json', 'w', encoding='utf-8') as file:
    json.dump(quotes, file, ensure_ascii=False, indent=4)
