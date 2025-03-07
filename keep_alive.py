from flask import Flask,render_template
from threading import Thread
app = Flask(__name__)

@app.route('/')
def index():
    return "I'm Alive Beacuse Of RefOo"

def run():
    app.run(debug=True)  # Disable Flask auto-reloader
    
def keep_alive():
    Thread(target=run).start()
