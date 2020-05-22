import psycopg2
import ps_store_parser as psp
import datetime

url = 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-PS4CAT/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
current_date = (datetime.datetime.now().date())

con = psycopg2.connect(
        database="Psn_game_base",
        user="postgres",
        password="va041062",
        host="127.0.0.1",
        port="5432"
    )
cur = con.cursor()
pages = psp.get_pages_count(url, headers)
for page in range(pages):
    page_info = psp.get_game_data(url, headers, page)
    for item in page_info:
        game_name = item['game_title']
        cur.execute("SELECT id FROM public.psn_games_description WHERE game_title = %s;", (game_name,))
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO psn_games_description (game_url, game_title, game_description, platform) VALUES (%s, %s, %s, %s)",
                (item['game_url'], item['game_title'], item['game_description'], item['game_platform']))
            cur.execute("SELECT id FROM public.psn_games_description WHERE game_title = %s;", (game_name,))
            game_id = cur.fetchone()
            cur.execute("SELECT req_date FROM public.psn_games_prices WHERE game_id = %s;", (game_id))
            date_found = cur.fetchone()
            while date_found is None:
                cur.execute(
                    "INSERT INTO psn_games_prices (game_id, price, value, req_date) VALUES (%s, %s, %s, %s)",
                    (game_id, item['game_price'], item['price_value'], item['req_date']))
                con.commit()
                cur.execute("SELECT req_date FROM public.psn_games_prices WHERE game_id = %s;", (game_id))
                date_found = cur.fetchone()
            if current_date != date_found[0]:
                cur.execute(
                    "INSERT INTO psn_games_prices (game_id, price, value, req_date) VALUES (%s, %s, %s, %s)",
                    (game_id, item['game_price'], item['price_value'], item['req_date']))
                con.commit()
            else:
                continue
        else:
            cur.execute("SELECT id FROM public.psn_games_description WHERE game_title = %s;", (game_name,))
            game_id = cur.fetchone()
            cur.execute("SELECT req_date FROM public.psn_games_prices WHERE game_id = %s;", (game_id))
            date_found = cur.fetchone()
            if current_date != date_found[0]:
                cur.execute(
                    "INSERT INTO psn_games_prices (game_id, price, value, req_date) VALUES (%s, %s, %s, %s)",
                    (game_id, item['game_price'], item['price_value'], item['req_date']))
                con.commit()
            else:
                continue
con.close()
print('Data successfully updated')

