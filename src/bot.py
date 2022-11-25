import sqlite3
from mastodon import Mastodon
from dotenv import load_dotenv, dotenv_values
from sqlite3 import Error
from stable_diffusion_tf.stable_diffusion import StableDiffusion
from PIL import Image
import os
import zhtts
import hashlib
import random

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

def select_char(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM hsk1 ORDER BY RANDOM() LIMIT 1")
    rows = cur.fetchall()
    return rows

def select_example_sentences(conn, zh_char):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT Characters, Pinyin, Meaning 
        FROM sentences 
        WHERE Characters LIKE '%{zh_char[0]}%' 
        ORDER BY RANDOM()
        LIMIT 1
    """)
    rows = cur.fetchall()
    return rows

def do_tts(hash, zh_text):
    f = f"./audio/{hash}.wav"
    if  not os.path.exists(os.path.abspath(f)):
        tts = zhtts.TTS(text2mel_name="FASTSPEECH2")
        tts = zhtts.TTS()
        tts.text2wav(zh_text, os.path.abspath(f))
        tts.frontend(zh_text)
        tts.synthesis(zh_text)

    return os.path.abspath(f)

def do_image(hash, en_text, extra):
    print(f"prompt ------> {en_text} {extra}")

    generator = StableDiffusion( 
        img_height=384,
        img_width=384,
        jit_compile=False,
        download_weights=True,
    )
    img = generator.generate(
        f"{en_text} {extra}",
        num_steps=30,
        unconditional_guidance_scale=7.5,
        temperature=1,
        batch_size=1,
    )
    pil_img = Image.fromarray(img[0])
    filename = f"./image/{hash}.png"
    pil_img.save(filename)
    return os.path.abspath(filename)

def do_video(hash, audio, image):
    os.system(f"ffmpeg -y -loop 1 -i {image} -i {audio} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest ./video/{hash}.mp4")

def post_to_mastodon(c_row, s_row, audio, image):
    mastodon = Mastodon(
        access_token = config['ACCESS_TOKEN'],
        api_base_url = config['API_BASE_URL']
    )

    # mastodon.toot(
    mastodon.status_post(
        spoiler_text=c_row[0],
        status=c_row[3] + " -- " + c_row[4] + ' #hsk #mandarin #chinese #study',
        language="zh"
    )

def main():
    database = r"zh.db"
    conn = create_connection(database)

    # Pick a random artist
    # f = open("data/artists.txt", "r")
    # artists = f.readlines()
    # f.close()

    artists = []
    with open("data/artists.txt") as f:
        artists = f.read().splitlines() 
    rand = round(len(artists) * random.random())
    print(artists[rand])
    
    with conn:
        c_rows = select_char(conn)
        s_rows = select_example_sentences(conn, c_rows[0])
        
        hash_object = hashlib.md5( str(c_rows[0][0]).encode('utf-8') )
        h = hash_object.hexdigest()
        print("Study word: " + c_rows[0][0] + " hash: " + h)

        audio = do_tts(h, s_rows[0][0])
        image = do_image(h, s_rows[0][2], c_rows[0][4] + f" {artists[rand]} artstation")
        
        do_video(h, audio, image)
        print(f"./video/{h}.mp4", audio, image)

        # post_to_mastodon(c_rows, s_rows, audio, image)


if __name__=="__main__":
    main()