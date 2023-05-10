FROM nginx:1.23.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY ./manager.sh /manager.sh

USER root

RUN apk add --no-cache openssl bash
RUN chmod +x /manager.sh

CMD ["/manager.sh"]