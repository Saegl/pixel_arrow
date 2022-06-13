from flask import Flask
from external_host import *

app = Flask(__name__)


@app.route("/")
def index():
    return "Alisher's server"


PORT = 12345

app.run("0.0.0.0", PORT)
