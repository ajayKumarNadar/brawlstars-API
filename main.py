from flask import Flask, render_template, url_for, redirect, request
from season_reset import reset_graph
import requests
import os

app = Flask(__name__)
URL = "https://api.brawlstars.com/v1/players/%23"
API_KEY = os.environ.get("API_KEY")
Headers = {
    "Authorization": f"Bearer {API_KEY}"
}

TAG = ""
reset_trophy = None
reset_sp = None


def season_reset(response):
    global reset_trophy, reset_sp
    brawlers = response['brawlers']
    reset_trophy = 0
    reset_sp = 0
    for brawler in brawlers:
        trophy = int(brawler['trophies'])
        above_500 = False
        for data in reset_graph:
            if data[0] <= trophy <= data[1]:
                reset_trophy += data[3]
                reset_sp += data[2]
                above_500 = True
        if not above_500:
            reset_trophy += trophy


@app.route("/", methods=["GET"])
def home():
    global TAG
    response = ""
    if TAG:
        TAG = TAG.replace("#", "")
        url = URL + TAG
        response = requests.get(url=url, headers=Headers).json()
        print(response)
        season_reset(response)
    return render_template("index.html", df=response, reset_trophy=reset_trophy, reset_sp=reset_sp)


@app.route("/login", methods=["POST"])
def login():
    global TAG
    TAG = request.form["tag"].upper()
    return redirect(url_for("home"))


@app.route("/logout", methods=["GET"])
def logout():
    global TAG
    TAG = ""
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
