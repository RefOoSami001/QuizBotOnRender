from flask import Flask,render_template
from threading import Thread
app = Flask(__name__)

@app.route('/')
def index():
    return "I'm Alive Beacuse Of RefOo"

def run():
    app.run(host='0.0.0.0', port=8000)
    
def keep_alive():
    Thread(target=run).start()
