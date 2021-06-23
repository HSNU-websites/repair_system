FROM python:3.9.5

WORKDIR /code

COPY . /code

RUN apt update \
    && apt upgrade -y \
    && apt install -y --no-install-recommends git default-mysql-client vim \
    && python3 -m pip install -r requirements.txt

CMD ["/usr/local/bin/python3", "-m","gunicorn","-b","0.0.0.0:5000", "manage:app"]

EXPOSE 5000
