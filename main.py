from flask import Flask, render_template, request
import os
from bs4 import BeautifulSoup
import requests
import scholarly

app = Flask(__name__)

def search(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    jstor_raw = requests.get(f"https://www.jstor.org/action/doBasicSearch?Query={query}", headers=headers).text
    print(jstor_raw)
    soup = BeautifulSoup(jstor_raw, 'html.parser')
    li_tags = soup.find_all("li")
    for tag in li_tags:
        print(tag)

def scholar(query):
    results = scholarly.search_pubs('machine learning')
    for result in results:
        print(result)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/search')
def search_():
    engine = request.args["engine"]
    return "test"

@app.route("/pubchem")
def pubchem():
    return render_template("pubchem.html", data={"query": request.args["query"]})

@app.route("/pubmed")
def pubchem():
    return render_template("pubmed.html", data={"query": request.args["query"]})

@app.route("/pubsci")
def pubchem():
    return render_template("pubsci.html", data={"query": request.args["query"]})

app.run(host="0.0.0.0", port="3000")
