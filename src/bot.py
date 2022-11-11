import sqlite3
from mastodon import Mastodon
from dotenv import load_dotenv, dotenv_values
from sqlite3 import Error

# take environment variables from .env.
load_dotenv()
config = dotenv_values(".env")

print(config['API_BASE_URL'])

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def select_all_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM hsk1 ORDER BY RANDOM() LIMIT 1")
    rows = cur.fetchall()
    for row in rows:
        post_to_mastodon(row)

def post_to_mastodon(row):
    # print(row)
    # print(row[0])
    # print(row[3] + " -- " + row[4])
    mastodon = Mastodon(
        access_token = config['ACCESS_TOKEN'],
        api_base_url = config['API_BASE_URL']
    )
    # mastodon.toot(
    mastodon.status_post(
        spoiler_text=row[0], 
        status=row[3] + " -- " + row[4] + ' #hsk #mandarin #chinese #study',
        language="zh"
    )

def main():
    database = r"zh.db"
    conn = create_connection(database)
    with conn:
        select_all_tasks(conn)


if __name__=="__main__":
    main()