FROM python:3.9.5

WORKDIR /code

COPY . /code

RUN chmod +x /code/docker-entrypoint.sh \
    && apt update \
    && apt upgrade -y \
    && apt install -y --no-install-recommends gcc default-mysql-client vim \
    && apt clean \
    && python3 -m pip install -r requirements.txt \
    && python3 -m pip cache purge

CMD ["/code/docker-entrypoint.sh"]

EXPOSE 5000
