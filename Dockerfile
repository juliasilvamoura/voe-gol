FROM python:3.11-slim

ENV FLASK_APP=main.app
ENV NAME_DB='anac'
ENV USER_DB='root'
ENV PASSWORD_DB='root'
ENV SQLALCHEMY_TRACK_MODIFICATIONS=False
ENV JWT_SECRET_KEY='secreto'
ENV FLASK_ENV='development'

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
