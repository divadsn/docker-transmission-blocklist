FROM alpine:3.13.5
LABEL maintainer="David Sn <divad.nnamtdeis@gmail.com>"

ARG USER=www-data
ARG UID=82
ARG GID=82

ENV OUTPUT_DIR=/data
ADD update-list.sh /usr/local/bin/update-list.sh

# Add www-data user and install dependencies
RUN set -x && \
    addgroup -g $GID -S $USER && \
    adduser -S -D -u $UID -h $OUTPUT_DIR -s /sbin/nologin -G $USER -g $USER $USER && \
    chmod +x /usr/local/bin/update-list.sh && \
    ln -sf /dev/stdout /var/log/cron.log && \
    apk add --no-cache curl

ADD crontab /etc/crontabs/$USER
ENTRYPOINT ["crond", "-L", "/var/log/cron.log", "-f"]
