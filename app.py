# import Flask library
from flask import Flask
from flask import request

# Create Flask app
app = Flask(__name__)

# import Keras library
from keras.preprocessing import sequence
from keras.models import load_model
from keras.preprocessing.text import text_to_word_sequence
from keras.datasets import imdb


# 각 시퀀스의 최대 단어 수 설정
maxlen = 10

# imdb 데이터셋에서 단어 인덱스 가져오기
word_index = imdb.get_word_index()

# 파일에서 모델 로드
nlp_model = load_model('imdb_nlp.h5')


# run prediction
def predict_sentiment(my_test):
    # 문장을 토큰화하기
    word_sequence = text_to_word_sequence(my_test)

    # 빈 정수 시퀀스 생성
    int_sequence = []

    # 문장의 각 단어에 대해서
    for w in word_sequence:
        # 어휘로부터 정수를 가져와 리스트에 추가
        int_sequence.append(word_index[w])

    # 정수 시퀀스를 모델이 예측한 입력 크기로 패딩
    sent_test = sequence.pad_sequences([int_sequence], maxlen=maxlen)

    # 모델을 사용해 예측 수행
    y_pred = nlp_model.predict(sent_test)

    # 예측된 0과 1 사이의 실수인 감정 값을 반환
    return y_pred[0][0]


# route 또는 HTTP endpoint 구축
@app.route('/hello')
def hello():
    return 'Hello, World!'


# 입력이 없을 때 처음 보여주는 기본 HTML
htmlDefault = '<h4>Simple Python NLP demo</h4><form><textarea rows=10 cols=100 name=\'text_input\'></textarea><br><input type=submit></form>'


# route 또는 HTTP endpoint 구축
# 이 route는 텍스트 매개변수를 읽어서 분석한다.
@app.route('/process')
def process():
    # 반환하는 HTML의 정의
    retHTML = ''

    # 'text_input'라는 이름으로 HTTP 매개변수 가져오기
    in_text = request.args.get('text_input')

    # 입력이 있으면 처리하고 아니면 기본 페이지를 표시한다.
    if in_text is not None:
        # 우선, 입력된 것을 표시
        retHTML += 'TEXT: <b>%s</b>' % (in_text)

        # 딥러닝 모델 실행
        result = predict_sentiment(in_text)

        # 긍정적인 감정이면
        if result > 0.5:
            retHTML += '<h4>Positive Sentiment! :-)</h4><br>'
        # 부정적인 감정이면
        else:
            retHTML += '<h4>Negative Sentiment! :-(</h4><br>'

    # 단순히 표시하기
    else:
        return htmlDefault


# run main application
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=1234)