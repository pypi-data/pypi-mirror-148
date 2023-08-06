import os
import time
import dotenv
import requests
from flask import Blueprint, request, render_template
from .creds import celery_link

song_search = Blueprint("song_search", __name__, static_folder="../static", template_folder="../templates")

dotenv.load_dotenv()


@song_search.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        context = {
            'title': 'Search'
        }
        return render_template('search.html', title=context['title'])

    if request.method == "POST":
        title = 'Search'
        results = []
        genius_results = request_song_info_genius(request.form['search_info']).json()
        for song in genius_results['response']['hits']:
            song = song['result']
            result = {
                'song_id': song['id'],
                'name': song['title'],
                'artist': song['artist_names'],
            }
            result['song_profile'] = f"/song?id={result['song_id']}"
            results.append(result)

        # return context['results']
        return render_template('search.html', title=title, results=results, placeholder=request.form['search_info'])


@song_search.route('/song', methods=['GET', 'POST'])
def song_profile():
    from urllib import parse

    title = "Song Profile Page"
    if request.args is not None:
        result = request_song_id_genius(request.args['id']).json()
        result = result['response']['song']
        result['liked'] = False
        for media in result['media']:
            if media['provider'] == "youtube":
                url = media['url']
                query_def = parse.parse_qs(parse.urlparse(url).query)['v'][0]
                result['youtube_id'] = query_def
        songInfo = {"title": result['title'], "artist": result["primary_artist"]["name"]}
        try:
            audioDBRes = request_song_info_audiodb(songInfo['artist'], songInfo['title']).json()
            result["genre"] = audioDBRes['track'][0]['strGenre']
        except TypeError:
            result["genre"] = "None"

        title = result['full_title']
        song_found = celery_link.send_task("tasks.find_song",
                                           kwargs={"name": songInfo['title'], "artist": songInfo['artist']})
        while str(celery_link.AsyncResult(song_found.id).state) != "SUCCESS":
            time.sleep(0.25)
        song_found_result = celery_link.AsyncResult(song_found.id).result
        if not song_found_result:
            celery_link.send_task("tasks.add_song", kwargs={"name": songInfo['title'], "artist": songInfo['artist'],
                                                            "genre": result['genre'], "genius_id": result['id']})
        else:
            song_liked = celery_link.send_task("tasks.get_liked_song", kwargs={"song_id": result['id'],
                                                                               "user_id": 1})  # TODO: Update user_id with dynamic user id
            while str(celery_link.AsyncResult(song_liked.id).state) != "SUCCESS":
                time.sleep(0.25)
            song_liked = celery_link.AsyncResult(song_liked.id).result
            result['liked'] = song_liked
        update_views = celery_link.send_task("tasks.update_views", kwargs={"genius_id": result['id']})
        while str(celery_link.AsyncResult(update_views.id).state) != "SUCCESS":
            time.sleep(0.25)
        count_views = celery_link.send_task("tasks.get_views", kwargs={"genius_id": result['id']})

        while str(celery_link.AsyncResult(count_views.id).state) != "SUCCESS":
            time.sleep(0.25)
        count_views = celery_link.AsyncResult(count_views.id).result
        result['views'] = count_views
        # to-do call celery link, call celery to increase views
    return render_template('song_profile.html', title=title, result=result)


# API CALLS

def request_song_info_genius(search_info):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + os.getenv('GENIUS_AUTH')}
    search_url = base_url + '/search'
    data = {'q': search_info}
    response = requests.get(search_url, data=data, headers=headers)

    return response


def request_song_id_genius(song_id):
    url = "https://genius-song-lyrics1.p.rapidapi.com/songs/" + song_id

    headers = {
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com",
        "X-RapidAPI-Key": "e66edeed2emshe809355cbf14d21p15ef82jsnf921421de2fe"
    }

    response = requests.request("GET", url, headers=headers)

    return response


def request_song_info_spotify(search_info):
    url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q": search_info, "type": "tracks", "limit": 15}

    headers = {
        'x-rapidapi-host': "spotify23.p.rapidapi.com",
        'x-rapidapi-key': "e66edeed2emshe809355cbf14d21p15ef82jsnf921421de2fe"
    }
    response = requests.get(url, headers=headers, params=querystring)

    return response

def request_loadtopcharts_audiodb():
    url = "https://theaudiodb.p.rapidapi.com/mostloved.php"

    querystring = {"format":"album"}

    headers = {
        'x-rapidapi-host': "theaudiodb.p.rapidapi.com",
        'x-rapidapi-key': "SIGN-UP-FOR-KEY"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response

def request_song_info_audiodb(artist, track_name):
    url = "https://theaudiodb.p.rapidapi.com/searchtrack.php"

    querystring = {"s": artist, "t": track_name}

    headers = {
        'x-rapidapi-host': "theaudiodb.p.rapidapi.com",
        'x-rapidapi-key': "e66edeed2emshe809355cbf14d21p15ef82jsnf921421de2fe"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response


def request_song_by_id_spotify(song_id):
    url = "https://spotify23.p.rapidapi.com/tracks/"
    if type(song_id) == "string":
        querystring = {"ids": song_id}
    else:
        querystring = {"ids": ','.join(song_id)}

    headers = {
        'x-rapidapi-host': "spotify23.p.rapidapi.com",
        'x-rapidapi-key': "e66edeed2emshe809355cbf14d21p15ef82jsnf921421de2fe"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response
