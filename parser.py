import requests
from bs4 import BeautifulSoup
import lxml
import time

url = 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-PS4CAT/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
def count_pages(url, headers):
    store_page = requests.get(url,  headers = headers)
    soup = BeautifulSoup(store_page.text, 'lxml')
    pages_info = soup.find('div', {'class': 'grid-footer-controls'})\
        .find('a', {'class': 'paginator-control__end paginator-control__arrow-navigation internal-app-link ember-view'})\
        .get('href').split('/')
    pages_qty = int(pages_info[-1])
    return pages_qty
def gathering_games_info(url, headers, page):
    games_info = []
    current_url = url + str(page+1)
    store_page = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(store_page.text, 'lxml')
    #print(soup)
    #print(store_page)
    games_titles = soup.find_all('div', {'class': 'grid-cell__body'})
    #print(games_titles)
    for game in games_titles:
        print('NEW GAME')
        print(game)
        game_name = game.find('div', {'class': 'grid-cell__title'}).find('span').text
        game_price = (game.find('h3', {'class':
                                           game.find('h3').get('class')}).text).split('\xa0')
        games_info.append({game_name: game_price})
    return games_info

pages = int(count_pages(url, headers))
for page in range(pages):
    print(gathering_games_info(url, headers, page))
