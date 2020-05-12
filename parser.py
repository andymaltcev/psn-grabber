import requests
from bs4 import BeautifulSoup
import lxml
import datetime

url = 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-PS4CAT/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
def get_pages_count(url, headers):
    store_page = requests.get(url,  headers = headers)
    soup = BeautifulSoup(store_page.text, 'lxml')
    pages_info = soup.find('div', {'class': 'grid-footer-controls'})\
        .find('a', {'class': 'paginator-control__end paginator-control__arrow-navigation internal-app-link ember-view'})\
        .get('href').split('/')
    pages_qty = int(pages_info[-1])
    return pages_qty
def get_game_data(url, headers, page):
    games_info = []
    current_url = url + str(page+1)
    store_page = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(store_page.text, 'lxml')
    games_titles = soup.find_all('div', {'class': 'grid-cell__body'})
    for game in games_titles:
        try:
            game_title = game.find('div', {'class': 'grid-cell__title'}).find('span').text
            game_price = (game.find('h3', {'class':
                                           game.find('h3').get('class')}).text).split('\xa0')
            actual_date = str(datetime.datetime.now().date())
            games_info.append({'game_title': game_title,
                               'game_price': game_price[1],
                               'price_value': game_price[0],
                               'actual_date': actual_date})
        except: TypeError
    return games_info

pages = int(get_pages_count(url, headers))
for page in range(pages):
    print(get_game_data(url, headers, page))