from flask import Flask, jsonify, make_response, request, redirect, url_for, render_template
from markupsafe import escape
import requests

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['name']
      return redirect(url_for('success',name = user + ' post'))
   else:
      user = request.args.get('name')
      return redirect(url_for('success',name = user + ' get'))

# allow both GET and POST requests
@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="language"></label></div>
               <div><label>Framework: <input type="text" name="framework"></label></div>
               <input type="submit" value="Submit">
           </form>'''   

@app.route('/calling_api', methods=['POST'])
def calling_api():
    request_data = call_nyt_api()

    response = make_response(request_data)
    response.headers["Content-Type"] = "application/json"
    return response

def call_nyt_api():
    # https://api.nytimes.com/svc/topstories/v2/{ASSUNTO}.json?api-key=yourkey

    all_subjects = ['arts', 'automobiles', 'books', 'business', 'fashion', 'food', 'health', 'home', 
        'insider', 'magazine', 'movies', 'nyregion', 'obituaries', 'opinion', 'politics', 
        'realestate', 'science', 'sports', 'sundayreview', 'technology', 'theater', 
        't-magazine', 'travel', 'upshot', 'us', 'world']
    assuntos = ['arts', 'books']

    if not assuntos:
        assuntos.append('books')

    response_json = []
    for assunto in assuntos:
        url = f'https://api.nytimes.com/svc/topstories/v2/{assunto}.json?api-key=PSQZz4GUxDx5ZkUlIoJPxebouJ19YdZg'

        request = requests.get(url)
        response_json.append(trim_api_results(request.json()['results'], assunto))
        
    return jsonify({'results': response_json})

def trim_api_results(json, assunto):
    j = []
    for i in range(3):
        j.append(
            {
                'title' : json[i]['title'],
                'abstract' : json[i]['abstract'],
                'url' : json[i]['url'],
                'author' : json[i]['byline'],
                'image' : json[i]['multimedia'][0]['url']
            }
        )
    
    return {assunto : j}