from flask import *
import time
import random
import json
import logging
import click
import os

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass


def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass


click.echo = echo
click.secho = secho

def CreateAPI(ip,port,db):
    print("[+] Restarting CreateAPI", end = '')
    time.sleep(1)
    print(".", end = '')
    time.sleep(1)
    print(".", end = '')
    time.sleep(1)
    print(".")
    time.sleep(0.5)
    print("[+] CreateAPI Is Ready To Use!")
    print(f"[+] IP: http://{ip}:{port}\n")
    app.run(host=ip, port=port, debug=db)

def RandomName(place):
    @app.route(place, methods=['GET', 'POST'])
    def randomname():
        cwd = os.getcwd()
        with open(rf"{cwd}\makeapi\functions\names.txt", "r") as n:
            allText = n.read()
            words = list(map(str, allText.split()))
        data_set = {'Page': 'RANDOM NAME', "name": f"{random.choice(words)}", "Timestamp": time.time()}
        json123 = json.dumps(data_set)
        return json123

def RandomJoke(place):
    @app.route(place, methods=['GET', 'POST'])
    def randomjoke():
        cwd = os.getcwd()
        print("[+] This Error Will Be Fixed Soon!")
        with open(rf"{cwd}\makeapi\functions\jokes.txt", "r") as n:
            allText = n.read()
            words = list(map(str, allText.split()))
        data_set = {'Page': 'RANDOM JOKES', "joke": f"{random.choice(words)}", "Timestamp": time.time()}
        json123 = json.dumps(data_set)
        return json123

def OwnPage(place,name,what_to_show):
    @app.route(place, methods=['GET', 'POST'])
    def ownpage():
        data_set = {'Page': 'OWN PAGE', name: what_to_show, "Timestamp": time.time()}
        json123 = json.dumps(data_set)
        return json123

@app.route('/', methods=['GET', 'POST'])
def home():
  data_set = {'Page': 'HOME', "Timestamp": time.time()}
  json123 = json.dumps(data_set)
  return json123



