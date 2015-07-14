from algo_coin.dashboard import dashboard
from flask import Flask, render_template


@dashboard.app.route('/index')
@dashboard.app.route('/')
@dashboard.app.route('/home')
def home():
    return render_template("index.html")
