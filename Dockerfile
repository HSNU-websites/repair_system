FROM python:3.9.5

RUN apt update \
    && apt upgrade -y \
    && apt install -y --no-install-recommends git default-mysql-client \
    && git clone -b main --depth 1 https://github.com/HSNU-websites/repair_system.git /repair_system \
    && cd /repair_system \
    && python3 -m pip install -r requirements.txt

CMD ["/usr/local/bin/python3", "-m","gunicorn","-b","0.0.0.0:5000", "manage:app"]

EXPOSE 5000
