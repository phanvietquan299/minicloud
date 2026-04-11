FROM nginx:stable-alpine

ARG SERVER_LABEL=core

RUN apk add --no-cache gettext
RUN rm -f /etc/nginx/conf.d/default.conf

COPY conf.default /tmp/conf.default
COPY html/ /usr/share/nginx/html/

RUN envsubst '$SERVER_LABEL' < /tmp/conf.default > /etc/nginx/conf.d/default.conf && \
	envsubst '$SERVER_LABEL' < /usr/share/nginx/html/index.html > /tmp/index.html && \
	mv /tmp/index.html /usr/share/nginx/html/index.html && \
	rm -f /tmp/conf.default

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
