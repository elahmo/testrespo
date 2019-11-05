from flask import render_template, url_for, abort, redirect, Blueprint, request, jsonify
from webapp.models import BlogPost, Leader
from flask import current_app
import requests
import json
from webapp.users.forms import LoginForm
from webapp.models import Leader, Daily, News
from webapp.core.forms import SelectForm
from flask_login import current_user, login_required
from selenium import webdriver
from webapp import db
from datetime import datetime, date, timedelta
import time






core = Blueprint('core',__name__)

@core.route('/')
def index():
    since = datetime.now() - timedelta(hours=23)
    since.strftime('%y%d%m')


    day = db.session.query(Daily).filter(Daily.date > since).all()

    return render_template('index.html', day=day)



@core.route('/indexpredictions')
def index_predictions():

    page= request.args.get('page',1,type=int)

    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=10)


    return render_template('indexpost.html', blog_posts=blog_posts)

@core.route('/player')
@login_required
def player_info():

    myPlayer = Leader.query.all()

    return render_template('player_info.html', myPlayer=myPlayer)

@core.route('/news')
def news():

    since = datetime.now() - timedelta(days=2)
    since.strftime('%y%d%m')

    newsDay = db.session.query(News).filter(News.date > since).all()

    return render_template('playernews.html', newsDay=newsDay)



@core.route('/highlights', methods=["GET", "POST"])


def highlights():

    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []

    search_params = {
        'key' : current_app.config['YOUTUBE_API_KEY'],
        'q' : 'nba highlights',
        'part' : 'snippet',
        'maxResults' : 12,
        'type' : 'video'
        }

    r = requests.get(search_url, params=search_params)

    video_ids = []

    rezultat = r.json()['items']


    for rez in rezultat:
        video_ids.append(rez['id']['videoId'])

    video_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'id' : ','.join(video_ids),
            'part' : 'snippet,contentDetails',
            'maxResults' : 12
        }

    r = requests.get(video_url, params=video_params)
    results = r.json()['items']

    for result in results:
            video_data = {
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],

                'title' : result['snippet']['title'],
            }

            videos.append(video_data)



    return render_template('highlights.html', videos=videos)

@core.route('/charts', methods=['GET', 'POST'])
def charts():

    myPlayer = Leader.query.all()



    return render_template('charts.html', myPlayer=myPlayer)


@core.route('/process' , methods=['GET','POST'])
def process():

    data = request.form['selectField']

    print(data)

    if data:
        data = int(data)
        player = Leader.query.filter_by(field1=data).first()
        print(player.PPG)

        return jsonify({"data": [player.Gamesplayed, player.AverageMin,  player.FGM,
         player.FGA, player.FG_, player._3PM, player._3ATT, player._3PT_, player.FTM,
         player.FTA, player.FT_, player.REB, player.AST, player.STL, player.BLK,
         player.TOV, player.PPG ], 'average' : [13, 30]})

@core.route('/update')
def update():

    browser = webdriver.Chrome('C:\\Users\\User\\Desktop\\chromedriver')

    browser.get('https://www.nba.com/scores#/')

    full_score = []
    full_name = []
    links = []

    full_scores = browser.find_elements_by_xpath('//span[@class="current_score"]')
    team_names =  browser.find_elements_by_xpath('//div[@class="score-tile__team-name"]')

    score_img = browser.find_elements_by_tag_name('img')


    for img in score_img:
        links.append(img.get_attribute('src'))

    for score in full_scores:
        full_score.append(score.text)

    for name in team_names:
        full_name.append(name.text)


    print (full_name)
    print (full_score)

    for a, b, c in zip(full_name, full_score, links):
        update = Daily(name=a, score=b, link=c)
        db.session.add(update)
        db.session.commit()

    browser.close()

    return redirect(url_for('core.index'))





@core.route('/newsupdate')
def news_update():

    browser = webdriver.Chrome('C:\\Users\\User\\Desktop\\chromedriver')

    browser.get('https://www.rotoworld.com/sports/nba/basketball')

    article_prof = []
    titles_full= []
    body_text = []
    links = []

    player_name = browser.find_elements_by_xpath('//div[@class="player-news-article__profile"]')
    titles_text = browser.find_elements_by_xpath('//div[@class="player-news-article__title"]')
    text = browser.find_elements_by_xpath('//div[@class="player-news-article__summary"]')
    images = browser.find_elements_by_tag_name('img')


    for name in player_name:
        article_prof.append(name.text)

    for title in titles_text:
        titles_full.append(title.text)

    for whole in text:
        body_text.append(whole.text)

    for img in images:
        links.append(img.get_attribute('src'))

    links2= links[1:]

    db_dic = [{
    'title' : titles_full,
    'heading' : article_prof,
    'article' : body_text,
    'pic' : links2[1::2]
    }]


    db.session.bulk_insert_mappings(News, db_dic, return_defaults=True)


    browser.close()

    return redirect(url_for('core.news'))

@core.route('/playersupdate', methods=["GET"])
def players_update():

    request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2019-20&SeasonType=Regular+Season&StatCategory=PTS'
    response = requests.get(url, headers = request_headers)
    stat = response.json()
    results = stat['resultSet']
    need = results['rowSet']

    player_name = []
    player_team = []
    player_gp = []
    player_min = []
    player_fgm = []
    player_fga = []
    player_fgpc = []
    player_3pm = []
    player_3a = []
    player_3pc = []
    player_ftm = []
    player_fta = []
    player_ftpc= []
    player_oreb = []
    player_dreb = []
    player_reb = []
    player_ast = []
    player_stl = []
    player_blk = []
    player_tov = []
    player_pts = []

    for item in need:
     player_name.append(item[2])
    for item in need:
        player_team.append(item[3])
    for item in need:
        player_gp.append(item[4])
    for item in need:
        player_min.append(item[5])
    for item in need:
        player_fgm.append(item[6])
    for item in need:
        player_fga.append(item[7])
    for item in need:
        player_fgpc.append(item[8])
    for item in need:
        player_3pc.append(item[9])
    for item in need:
        player_3a.append(item[10])
    for item in need:
        player_3pc.append(item[11])
    for item in need:
        player_ftm.append(item[12])
    for item in need:
        player_fta.append(item[13])
    for item in need:
        player_ftpc.append(item[14])
    for item in need:
        player_oreb.append(item[15])
    for item in need:
        player_dreb.append(item[16])
    for item in need:
        player_reb.append(item[17])
    for item in need:
        player_ast.append(item[18])
    for item in need:
        player_stl.append(item[19])
    for item in need:
        player_blk.append(item[20])
    for item in need:
        player_tov.append(item[21])
    for item in need:
        player_pts.append(item[22])


    return jsonify({'name' : player_name})



@core.route('/currentyear')
def current_year():

    return render_template('playertoday.html')
