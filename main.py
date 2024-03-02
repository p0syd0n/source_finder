from flask import Flask, render_template, request, redirect
import os
from bs4 import BeautifulSoup
import requests
import json
from scholarly import scholarly
import re
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)
SCI_HUB = '/scihub' # 'https://sci-hub.yncjkj.com/'
SCHOLAR_MAX = 10
PORT = os.environ.get("PORT")

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
    query = request.args["query"]
    return redirect(f"/{engine}?query={query}")

@app.route('/blend')
def blend():
    query = request.args['query']
    if not query:
        return 'Query not found. Go back and try again'

    # Google Scholar Data

    # raw data

    try:

        raw_scholar = scholarly.search_pubs(query)
    except:
        return render_template("not_available.html", data=json.loads(json.dumps({'feature_name': 'Blend Search', 'details': 'Google Scholar error'})))
    scholar_objects = []

    # iterating over objects in the response

    articles = 0
    for item in raw_scholar:
        if articles == SCHOLAR_MAX:
            break
        try:

            # finding a DOI
            doi = None
            doi_pattern = r'10.\d{4,9}/[-._;()/:A-Z0-9]+'
            doi_match = re.search(doi_pattern, item['pub_url'])

            if doi_match:
                doi = doi_match.group()
                print(f"DOI: {doi}")
            else:
                print("DOI not found in the URL.")\
            
            sci_hub_url = ""
            try:
                sci_hub_url = SCI_HUB + "?doi="+doi
            except TypeError:
                sci_hub_url = ""
            # adding the article to the list
            scholar_objects.append({'name': item['bib']['title'], 'source': 'Google Scholar', 'url': item['pub_url'], 'sci_hub': sci_hub_url, 'abstract': item['abstract']})
            articles += 1
        except:
            continue

    data = {'query': query, 'objects': (scholar_objects)}
    print(data)
    json_data = json.loads(json.dumps(data))

    return render_template('search.html', data=json_data)

@app.route("/pubchem")
def pubchem():
    return render_template("pubchem.html", data={"query": request.args["query"]})

@app.route("/pubmed")
def pubmed():
    #return render_template("pubmed.html", data={"query": request.args["query"]})
    return redirect(f"https://pubmed.ncbi.nlm.nih.gov/?term={request.args['query']}")

@app.route("/scipub")
def pubsci():
    return render_template("scipub.html", data={"query": request.args["query"]})

@app.route("/scihub")
def scihub():
    return render_template("scihub.html", data={"doi": request.args["doi"]})

#results = scholarly.search_pubs("machine learning")
# for i in results:
#     print(i['bib']['title'])
    
app.run(host="0.0.0.0", port=PORT)

