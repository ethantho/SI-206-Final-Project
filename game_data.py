import json
import random
import string
import requests
import sqlite3

def random_search():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(2))

def main(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, name TEXT NOT NULL, release_date DATETIME NOT NULL)")
    client_id = 'cq00hfyu4x1y80l904fwvf3dte661z'
    credentials_info = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret=xgijy8ymuul9w0vc8wgj1eeojznwuj&grant_type=client_credentials")
    access_token = credentials_info.json()['access_token']
    junk = random_search()
    response = requests.post('https://api.igdb.com/v4/games', **{'headers': {'Client-ID': client_id, 'Authorization': ("Bearer " + access_token)},'data': f'fields name,first_release_date; limit 25; search "{junk}";'})
    for game in response.json():
        print(game)
        if 'first_release_date' not in game:
            continue
        #date_id = game['release_dates'][0]
        #date_id = requests.post('https://api.igdb.com/v4/release_dates', **{'headers': {'Client-ID': client_id, 'Authorization': ("Bearer " + access_token)},'data': 'fields date;'})
        cur.execute("INSERT OR IGNORE INTO games VALUES (?,?,?)", (game['id'], game['name'], game['first_release_date']))
    #print(response.json())
    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite3")
    main(conn)

