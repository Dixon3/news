# -*- coding: utf-8 -*-
from datetime import datetime
from elasticsearch import Elasticsearch 
from flask import render_template, flash, redirect, session, url_for, request, g

from grepnews import grepnews
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm

import users 

es = Elasticsearch()


                                          
@grepnews.before_request
def before_request():  
    print current_user
    g.user = current_user


@grepnews.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        print form.username.data,dir(form.password),form.password.data
        user=users.User(form.username.data,form.password.data)
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)

@grepnews.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@grepnews.route("/settings")
@login_required
def settings():
    pass


@grepnews.route('/')
@grepnews.route('/index')
@login_required
def index():
    user=g.user 
    return render_template("index.html", title = 'Home',
        user = user)

@grepnews.route('/feeds',methods=['GET', 'POST'])
def feeds():

    pages = es.search(index="newspapers", doc_type="page",body={
  "query": {
    "bool": {
      "must": [
        {
          "query_string": {
            "default_field": "page.description",
            "query": u"*"
          }
        }
      ],
      "must_not": [],
      "should": []
    }
  },
  "from": 0,
  "size": 250,
  "sort": [{
      "publishedDate": {
        "order": "desc"
      }
    }],
  "facets": {}
})
#    print pages
    return render_template("feeds.html",title='Feeds',feeds=pages)

@grepnews.route('/feed/<id>')
def feed(id):
    feed = es.get(index="newspapers", doc_type="page",id=id)
    print feed
    return render_template("feed.html",title='Feed',feed=feed)

@grepnews.route('/rivers')
def rivers():
    rivers=es.search(index="_river", doc_type="all",body={"query":"*"})
    print rivers

@grepnews.route('/river/<id>')
def river(id):
    feed = es.get(index="newspapers", doc_type="page",id=id)
    print feed
    return render_template("feed.html",title='Feed',feed=feed)


