import json
from flask import Flask, render_template
from sassutils.wsgi import SassMiddleware

import models


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True



@app.route('/')
def hello():
    return render_template('base.html')




@app.route('/today')
def today():
    return render_template('today.html', context=models.latest_posts())


@app.route("/posts/<name>")
def posts(name):
    return render_template('posts.html', context=models.posts(name))


app.run()