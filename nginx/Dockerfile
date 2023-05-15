FROM nginx:1.23.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY nginx.dev.conf /etc/nginx/conf.d

ARG DEBUG=True

RUN if [ "$DEBUG" = "True" ]; then \
        cp /etc/nginx/conf.d/nginx.dev.conf /etc/nginx/conf.d/nginx.conf; \
    fi