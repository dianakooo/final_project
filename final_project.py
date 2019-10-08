from flask import Flask, render_template, request
import urllib.request
import json
import markovify

def vkmarkov():
    communities = ['krutiecitati', 'pachkasigg', 'pacan_status_200']
    token="8423c2448423c2448423c244d08441f2a1884238423c244dee1644d9e90529494134bf8"
    texts = []
    for c in communities:
        of = 0
        posts = []
        while of != 300:
            http = 'https://api.vk.com/method/wall.get?domain=%s&offset=%s8&count=100&v=5.92&access_token=%s' % (
            c, of, token)
            req = urllib.request.Request(http)
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            data = json.loads(result)
            posts += data['response']['items']
            of += 100
        for post in posts:
            texts.append(post['text'])
    joined = ' '.join(texts)
    m = markovify.Text(joined)
    sentence = m.make_sentence()
    while sentence == None:
        sentence = m.make_sentence()
    return sentence

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quote', methods = ['POST', 'GET'])
def graph():
    if request.method == 'POST':
        sentence = vkmarkov()
    return render_template('quote.html', sentence=sentence)

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)