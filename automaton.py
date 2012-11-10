#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, flash
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)

import re
from handler.zwave import zwave
from handler.cameras import cameras
from handler.tv import tv

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active


class Anonymous(AnonymousUser):
    name = u"anonymous"

USERS = {
    1: User(u"wylie", 1),
    2: User(u"camille", 2),
    2: User(u"stan", 3),
    3: User(u"gage", 4, False),
}

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())


app = Flask(__name__)
app.register_blueprint(zwave, url_prefix='/zwave')
app.register_blueprint(cameras, url_prefix='/cameras')
app.register_blueprint(tv, url_prefix='/tv')


SECRET_KEY = "PingZero.Networks"
DEBUG = True

app.config.from_object(__name__)

login_manager = LoginManager()

login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))


login_manager.setup_app(app)

@app.route("/")
@login_required
def index():
	browser = request.user_agent.browser
	# version = request.user_agent.version and int(request.user_agent.version.split('.')[0])
	# platform = request.user_agent.platform
	uas = request.user_agent.string

	if (browser=='safari'):
		if (re.search('iPad', uas)) or (re.search('iPhone', uas)):
			return render_template("index.html", iOS=True)
	return render_template("index.html")

@app.route("/secret")
@fresh_login_required
def secret():
    return render_template("secret.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        if password == "datamaersk" and username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember=remember):
                flash("%s has logged in" % (username))
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid user or password.")
    return render_template("login.html")


@app.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("reauth.html")


@app.route("/logout")
@login_required
def logout():
    flash("%s logged out" % (current_user.name))
    logout_user()
    return render_template('logout.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5678)

