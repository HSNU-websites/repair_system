FROM jonasal/nginx-certbot

COPY templates /etc/nginx/templates

RUN rm /var/log/nginx/access.log \
    && ln -s /dev/null /var/log/nginx/access.log \
    && sed -i "s/\/etc\/nginx\/conf.d/\/etc\/nginx\/user_conf.d/" /docker-entrypoint.d/20-envsubst-on-templates.sh
