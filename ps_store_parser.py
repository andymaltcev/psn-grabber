import requests
from bs4 import BeautifulSoup
import lxml
import datetime

def get_pages_count(url, headers):
    store_page = requests.get(url,  headers = headers)
    soup = BeautifulSoup(store_page.text, 'lxml')
    pages_info = soup.find('div', {'class': 'grid-footer-controls'})\
        .find('a', {'class': 'paginator-control__end paginator-control__arrow-navigation internal-app-link ember-view'})\
        .get('href').split('/')
    pages_qty = int(pages_info[-1])
    print('Number of pages', pages_qty)
    return pages_qty
def get_game_data(url, headers, page):
    games_info = []
    current_url = url + str(page+1)
    print('Receiving...', current_url)
    store_page = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(store_page.text, 'lxml')
    games_titles = soup.find_all('div', {'class': 'grid-cell__body'})
    for game in games_titles:
        try:
            game_url = game.find('a', {'class': 'internal-app-link ember-view'}).get('href').split('/')[3]
            game_title = game.find('div', {'class': 'grid-cell__title'}).find('span').text
            game_description = game.find('div', {'class': 'grid-cell__left-detail grid-cell__left-detail--detail-2'}).text
            game_platform = game.find('div', {'class': 'grid-cell__left-detail grid-cell__left-detail--detail-1'}).text
            game_price = (game.find('h3', {'class':game.find('h3').get('class')}).text).split('\xa0')
            req_date = str(datetime.datetime.now().date())
            title_lowreg = game_title.lower()

            games_info.append({'game_url': game_url,
                               'game_title': game_title,
                               'game_price': int(game_price[1].replace('.','')),
                               'game_description': game_description,
                               'game_platform': game_platform,
                               'price_value': game_price[0],
                               'req_date': req_date,
                               'title_lowreg': title_lowreg})
        except: TypeError
    return games_info


