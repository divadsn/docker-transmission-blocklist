# docker-transmission-blocklist
Regularly updated blocklist with lists from iblocklist.com

Use https://mirror.codebucket.de/transmission/blocklist.p2p.gz in Transmission as blocklist url.

## Example usage
```
version: '3.3'
services:
  cron:
    build:
      context: .
      args:
        - USER=www-data
        - UID=82
        - GID=82
    restart: always
    volumes:
      - /usr/local/share/transmission/blocklists:/data
```
