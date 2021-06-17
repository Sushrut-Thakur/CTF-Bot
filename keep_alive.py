import warnings
warnings.filterwarnings("ignore") # Ignores warnings due to deprecated functions

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive! I get pinged every 50 minutes!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
