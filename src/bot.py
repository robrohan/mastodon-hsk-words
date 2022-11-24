import sqlite3
from mastodon import Mastodon
from dotenv import load_dotenv, dotenv_values
from sqlite3 import Error
import os
import zhtts
import hashlib

# take environment variables from .env.
load_dotenv()
config = dotenv_values(".env")

# print(config['API_BASE_URL'])

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

def do_tts(text):
    hash_object = hashlib.md5( str(text).encode('utf-8') )
    h = hash_object.hexdigest()
    f = "./audio/"+h+".wav"

    if  not os.path.exists(os.path.abspath(f)):
        tts = zhtts.TTS(text2mel_name="FASTSPEECH2")
        tts = zhtts.TTS()
        tts.text2wav(text, os.path.abspath(f))
        tts.frontend(text)
        tts.synthesis(text)

    return os.path.abspath(f)

def post_to_mastodon(row):
    mastodon = Mastodon(
        access_token = config['ACCESS_TOKEN'],
        api_base_url = config['API_BASE_URL']
    )

    file = do_tts(row[0])
    print(file, flush=True)

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