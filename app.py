from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbproject  # 'dbsparta'라는 이름의 db를 만듭니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/guide')
def get_guidepage():
    return render_template('guide.html')


@app.route('/silence')
def get_silencepage():
    return render_template('silence.html')


@app.route('/affirmation')
def get_affirmationpage():
    return render_template('affirmation.html')


@app.route('/visualization')
def get_visualizationpage():
    return render_template('visualization.html')


@app.route('/exercise')
def get_exercisepage():
    return render_template('exercise.html')


@app.route('/read')
def get_readpage():
    return render_template('reading.html')


@app.route('/scribing')
def get_scribingpage():
    return render_template('scribing.html')


## API 역할을 하는 부분
@app.route('/api/read', methods=['POST'])
def write_review():
    # title_receive로 클라이언트가 준 title 가져오기
    title_receive = request.form['title_give']
    # author_receive로 클라이언트가 준 author 가져오기
    author_receive = request.form['author_give']
    # review_receive로 클라이언트가 준 review 가져오기
    review_receive = request.form['review_give']

    # DB에 삽입할 review 만들기
    review = {
        'title': title_receive,
        'author': author_receive,
        'review': review_receive
    }
    # reviews에 review 저장하기
    db.reviews.insert_one(review)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})


@app.route('/api/read', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    reviews = list(db.reviews.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'reviews': reviews})


@app.route('/api/silence', methods=['POST'])
def post_silence():
    # 1. 클라이언트로부터 데이터를 받기
    url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_title = og_title['content']
    url_description = og_description['content']
    url_image = og_image['content']

    silence = {'url': url_receive, 'title': url_title, 'desc': url_description, 'image': url_image,
               'comment': comment_receive}

    # 3. mongoDB에 데이터를 넣기
    db.silences.insert_one(silence)

    return jsonify({'result': 'success'})


@app.route('/api/silence', methods=['GET'])
def read_silence():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.silences.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'silences': result})


@app.route('/api/silence', methods=['POST'])
def delete_silence():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    url_receive = request.form['url_give']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.silences.insert_one({'url': url_receive})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


# exercise api
@app.route('/api/exercise', methods=['POST'])
def post_exercise():
    # 1. 클라이언트로부터 데이터를 받기
    url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_title = og_title['content']
    url_description = og_description['content']
    url_image = og_image['content']

    exercise = {'url': url_receive, 'title': url_title, 'desc': url_description, 'image': url_image,
                'comment': comment_receive}

    # 3. mongoDB에 데이터를 넣기
    db.exercises.insert_one(exercise)

    return jsonify({'result': 'success'})


@app.route('/api/exercise', methods=['GET'])
def read_exercise():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.exercises.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'exercises': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5007, debug=True)
