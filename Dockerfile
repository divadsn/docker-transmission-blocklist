FROM alpine:3.13.5
LABEL maintainer="David Sn <divad.nnamtdeis@gmail.com>"

# Remove X Font Server (xfs) user and add www-data user
RUN set -x && \
    deluser xfs && \
    addgroup -g 33 -S www-data && \
    adduser -S -D -u 33 -h /var/www -s /sbin/nologin -G www-data -g www-data www-data && \
    su www-data -s /bin/sh -c "mkdir -p /var/www/shared" && \
    apk add --no-cache curl ca-certificates

ADD crontab /etc/crontabs/www-data
ADD update-lists.sh /usr/local/bin/update-lists.sh
RUN chmod +x /usr/local/bin/update-lists.sh

ENTRYPOINT ["crond", "-f"]
