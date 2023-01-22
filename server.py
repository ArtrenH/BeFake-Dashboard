import json
from flask import Flask, render_template
from flask import request

import models, methods


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def hello():
    return render_template('welcome.html')

@app.route('/today')
def today():
    return render_template('posts.html', info={"type": "today"}, context=models.latest_posts())


@app.route('/user')
def users():
    return render_template('users.html', context=models.users())

@app.route("/user/<name>")
def user(name):
    return render_template('posts.html', info={"type": "user", "name": name}, context=models.posts(name))


@app.route("/comments/<post_id>", methods=["GET", "POST"])
def comment(post_id):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        if "content" not in request.form:
            return "No content provided", 400
        methods.add_comment(post_id, request.form["content"])
        return f"Added comment!"


# In Progress:
"""
@app.route("/discovery")
def discovery():
    return render_template('discovery.html', context=models.compile_location_entries())
"""
#app.run(host="0.0.0.0", port="6000")
if __name__ == "__main__":
    app.run()