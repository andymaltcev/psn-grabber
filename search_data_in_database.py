import psycopg2
import matplotlib as mpl
import matplotlib.pyplot as plt

con = psycopg2.connect(
        database="Psn_game_base",
        user="postgres",
        password="va041062",
        host="127.0.0.1",
        port="5432"
    )
cur = con.cursor()

title = input('Enter the title: ')

cur.execute("SELECT id FROM public.psn_games_description WHERE game_title = %s;", (title,))

game_id = cur.fetchone()

cur.execute("SELECT price, req_date FROM public.psn_games_prices WHERE game_id = %s ORDER BY req_date;", (game_id))

data = cur.fetchall()
x = []
y = []

for item in data:
    x.append(item[1])
    y.append(item[0])

mpl.rcParams.update({'font.size': 7})
plt.title(title, fontsize = 16)
plt.ylabel('price, RUB', fontsize = 12)
plt.xlabel('date', fontsize = 12)
plt.plot(x,y)
plt.show()