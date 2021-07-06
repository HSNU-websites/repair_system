FROM jonasal/nginx-certbot

COPY templates /etc/nginx/templates

RUN rm /var/log/nginx/access.log \
    && ln -s /dev/null /var/log/nginx/access.log \
