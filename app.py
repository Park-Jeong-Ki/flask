from flask import Flask, request, jsonify
import pandas as pd
from cryptography.fernet import Fernet
import os
from io import StringIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return "Flask 서버가 정상적으로 실행되고 있습니다. 검색을 위해 /search 라우트를 사용하세요."

@app.route('/hello_world', methods=['GET'])
def hello_world():
    return "Hello World"

def load_key():
    key = b'TU0vRuj7uW0T2Gh81dwtC5qTs7djhmqUkzpWRlR06c0='
    return Fernet(key)

def load_data():
    fernet = load_key()
    directory = './main_data/'
    file_name = 'main_data.csv'
    encrypted_file_path = os.path.join(directory, file_name)

    if os.path.isfile(encrypted_file_path):
        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted = encrypted_file.read()
        decrypted = fernet.decrypt(encrypted)
        df = pd.read_csv(StringIO(decrypted.decode('utf-8')))
        return df
    else:
        return None

def search_keyword_in_columns(df, keyword):
    search_columns = ['감정평가요약', '특수권리분석', '참고사항']
    rows = []

    for index, row in df.iterrows():
        for col in search_columns:
            text = row[col]
            if pd.isna(text):
                continue
            sentences = text.split('.')
            for sentence in sentences:
                if keyword in sentence:
                    rows.append({'사건번호': row['사건번호'], '주요키워드': sentence.strip()})

    result_df = pd.DataFrame(rows)
    return result_df, len(rows)  # 결과 DataFrame과 검색된 결과의 개수를 반환

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'No keyword provided'}), 400

    df = load_data()
    if df is not None:
        result_df, count = search_keyword_in_columns(df, keyword)  # 검색 결과와 개수를 받음
        return jsonify({'results': result_df.to_dict(orient='records'), 'count': count})  # 결과와 개수를 함께 JSON 형태로 리턴
    else:
        return jsonify({'error': 'Data not found'}), 404

if __name__ == '__main__':
    app.run
