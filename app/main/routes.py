from flask import render_template,  url_for, request, Blueprint

main = Blueprint('main',__name__)

@main.route("/")
def index():
    return render_template('main/index.html')

@main.route("/home")
def home():
    return render_template('main/home.html')

@main.route("/about")
def about():
    return render_template('main/about.html')
