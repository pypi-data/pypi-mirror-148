from flask import Flask, redirect, render_template, request
from dotenv import load_dotenv
from blueprints.crud import crud, create_db
from blueprints.celery_test import celery_test
from blueprints.song_search import song_search
from blueprints.users import users
from blueprints.users_interactions import users_interactions
from blueprints.song_interaction import song_interaction
from blueprints.playlist_interaction import playlist_interaction
from blueprints.topchart import topten_charts
from blueprints.topsong import top_songs
from blueprints.creds import celery_link
from blueprints.latest_dump import user_dump
import time

load_dotenv()

app = Flask(__name__)
app.register_blueprint(crud, url_prefix='/api')
app.register_blueprint(celery_test, url_prefix='/celery')
app.register_blueprint(song_search, url_prefix='')
app.register_blueprint(users, url_prefix='')
app.register_blueprint(users_interactions)
app.register_blueprint(song_interaction, url_prefix='')
app.register_blueprint(playlist_interaction, url_prefix='/playlist')
app.register_blueprint(topten_charts, url_prefix='')
app.register_blueprint(top_songs, url_prefix='')
app.register_blueprint(user_dump, url_prefix='')


@app.before_first_request
def make_db():
    create_db()
    celery_link.AsyncResult("tasks.schedule_tasks")

@app.route('/')
def hello_world():

    title = 'Home Page'

    news_elements = celery_link.send_task("tasks.get_news")

    while str(celery_link.AsyncResult(news_elements.id).state) != "SUCCESS":
        time.sleep(0.05)
    news_elements = celery_link.AsyncResult(news_elements.id).result
    # celery_link.send_task("tasks.run_dump")
    return render_template('home.html', title=title, news=news_elements)

@app.route('/search')
def hello_search():
    context = {
        'title': 'Search Page'
    }
    return render_template('search.html', data=context)

@app.route('/register')
def hello_register():
    context = {
        'title': 'Register Page'
    }
    return render_template('register.html.html', data=context)

@app.route('/login')
def hello_login():
    context = {
        'title': 'Login Page'
    }
    return render_template('login.html', data=context)


if __name__ == '__main__':
    app.run()
