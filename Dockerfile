FROM nikolaik/python-nodejs:python3.6-nodejs12-alpine

COPY . /ComicCrawler
RUN  pip install /ComicCrawler




