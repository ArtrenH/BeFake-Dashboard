import json
from flask import Flask, render_template
from flask import request
from sassutils.wsgi import SassMiddleware

import models, methods


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True



@app.route('/')
def hello():
    return render_template('base.html')




@app.route('/today')
def today():
    return render_template('posts.html', info={"type": "today"}, context=models.latest_posts())


@app.route('/user')
def users():
    return render_template('users.html', context=models.users())

@app.route("/user/<name>")
def user(name):
    return render_template('posts.html', info={"type": "user", "name": name}, context=models.posts(name))


@app.route("/comment", methods=["GET", "POST"])
def comment():
    post_id = request.args.get('post_id')
    if post_id is None:
        return "No post id provided", 400
    if request.method == "GET":
        print("get request")
    elif request.method == "POST":
        print("post request")
        print(request.form)
        if "content" not in request.form:
            return "No content provided", 400
        methods.add_comment(post_id, request.form["content"])
    return f"comments for {post_id}"

app.run()