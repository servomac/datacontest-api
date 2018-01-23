FROM python:3.6

WORKDIR /usr/src/app

ADD requirements/ requirements/
RUN pip install -r requirements/test.txt

ADD . /usr/src/app

CMD [ "python", "manage.py", "run" ]
