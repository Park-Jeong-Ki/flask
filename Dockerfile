# Python 이미지를 기반으로 함
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 파일 복사
COPY ./requirements.txt /app/

# gunicorn 설치
RUN pip install gunicorn

# Node.js 및 npm 설치 (필요한 경우)
RUN apt-get update && apt-get install -y nodejs npm

# requirements.txt에 명시된 Python 의존성 설치
RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi

# 애플리케이션 파일 복사
COPY . /app

# 소유권 설정 및 .git 디렉토리 제거 (필요한 경우)
RUN chown -R python:python /app && rm -rf .git*

# 애플리케이션 실행
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
