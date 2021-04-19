# docker-transmission-blocklist
Regularly updated blocklist with lists from iblocklist.com

## Usage
Use the following content for the docker-compose.yml file, then run docker-compose up.

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
