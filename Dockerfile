FROM python:3.8.5

RUN pip install --upgrade pip \
    && mkdir /app

ADD . /APP

WORKDIR /APP

RUN pip install -r requirements.txt

CMD python /app/main.py