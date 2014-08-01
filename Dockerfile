FROM debian:wheezy

RUN apt-get -qq update && apt-get -qq install python python-pip python-virtualenv sudo python-dev libpq-dev

RUN useradd -d /app -r app
WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN virtualenv python_env && . ./python_env/bin/activate && pip install -r requirements.txt
ADD . /app

ENTRYPOINT ["./invoke.sh"]
EXPOSE 8000
