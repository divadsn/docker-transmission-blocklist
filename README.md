# docker-transmission-blocklist
Regularly updated blocklist with lists from iblocklist.com

## Usage
Use the following content for the docker-compose.yml file, then run docker-compose up.
```
version: '3.3'
services:
  cron:
    image: divadsn/transmission-blocklist
    restart: always
    volumes:
      - /usr/local/share/transmission/blocklists:/var/www/transmission
```
