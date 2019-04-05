# movie_ratings
# VERSION   0.0.1

FROM python:3.7.3-alpine3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod 755 movie_rating.py

ENTRYPOINT [ "python", "./movie_rating.py" ]
