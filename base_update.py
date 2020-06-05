import psycopg2

con = psycopg2.connect(
        database="Psn_game_base",
        user="postgres",
        password="va041062",
        host="127.0.0.1",
        port="5432"
    )
cur = con.cursor()

cur.execute("SELECT game_title FROM public.psn_games_description ")

title_list = cur.fetchall()
for title in title_list:
    title_lowreg = (title[0].lower(),)
    game_name = (title[0],)
    print(game_name, title_lowreg)
    cur.execute("UPDATE public.psn_games_description SET title_lowreg = (%s) WHERE game_title = (%s);", (title_lowreg, game_name))
    print('Done')
con.commit()