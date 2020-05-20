import psycopg2

con = psycopg2.connect(
        database="Psn_game_base",
        user="postgres",
        password="va041062",
        host="127.0.0.1",
        port="5432"
    )
cur = con.cursor()
cur.execute('''CREATE TABLE psn_games_description
     (id SERIAL PRIMARY KEY NOT NULL,
     game_url TEXT NOT NULL,
     game_title TEXT NOT NULL,
     game_description TEXT NOT NULL,
     platform TEXT NOT NULL);''')
cur.execute('''CREATE TABLE psn_games_prices
     (id SERIAL PRIMARY KEY NOT NULL,
     game_id INT NOT NULL,
     price INT NOT NULL,
     value TEXT NOT NULL,
     req_date DATE NOT NULL);''')
con.commit()
con.close()
print('Tables successfully created')