FROM python:3.10.1

WORKDIR /code

RUN apt update \
    && apt upgrade -y \
    && apt install -y --no-install-recommends gcc default-mysql-client vim tzdata \
    && apt clean \
    && python3 -m pip install -r requirements.txt \
    && python3 -m pip cache purge

ENV FLASK_APP=manage \
    FLASK_ENV=production

COPY . /code

CMD ["/bin/sh", "/code/docker-entrypoint.sh"]

EXPOSE 5000
