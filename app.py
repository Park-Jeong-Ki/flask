from flask import Flask, request, jsonify
import pandas as pd
from cryptography.fernet import Fernet
import os
from io import StringIO
from flask_cors import CORS  # CORS를 위한 라이브러리 임포트

app = Flask(__name__)
CORS(app)  # CORS 설정 적용
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return "Flask 서버가 정상적으로 실행되고 있습니다. 검색을 위해 /search 라우트를 사용하세요."

# secret.key 파일로부터 키를 불러오는 함수
def load_key():
    key = b'TU0vRuj7uW0T2Gh81dwtC5qTs7djhmqUkzpWRlR06c0='
    return Fernet(key)

# 암호화된 파일을 복호화하여 메모리에 로드하는 함수
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

# 키워드 검색을 수행하는 함수
def search_keyword_in_columns(df, keyword):
    search_columns = ['감정평가요약', '특수권리분석', '참고사항']
    keyword_filter = df[search_columns].apply(lambda x: x.str.contains(keyword, na=False, regex=True)).any(axis=1)
    result_df = df[keyword_filter]
    result_columns = ['사건번호']
    result_df = result_df[result_columns]
    # TODO result_df에 새로운 컬럼을 추가하여 검색 결과를 표시할 수 있도록 구현
    # 주요 키워드 탐색 결과를 표시하는 컬럼을 추가하고, 해당 컬럼에 키워드가 포함된 문장을 입력
    result_df['주요키워드'] = '키워드가 포함된 문장'
    return 

# API 루트
@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'No keyword provided'}), 400

    df = load_data()
    if df is not None:
        result_df = search_keyword_in_columns(df, keyword)
        return jsonify(result_df.to_dict(orient='records'))
    else:
        return jsonify({'error': 'Data not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
