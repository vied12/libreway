#!/usr/bin/env python
# Encoding: utf-8
from pymongo import MongoClient
from flask import Flask
from pprint import pprint as pp
import sys
import json
import feedparser
import requests
from pyquery import PyQuery as pq
from lxml import etree

app = Flask(__name__)
app.config.from_envvar('TIMEREADER_SETTINGS')

client     = MongoClient(app.config['MONGO_HOST'])
db         = client[app.config['MONGO_DB']]
collection =  db["articles"]


for art in collection.find():
	if not 'count_words' in art or not art['count_words'] or art['count_words'] == 0:
		d     = pq(art['content'].encode('utf-8'))
		count = len(d.text().split())
		art['count_words'] = count
		collection.save(art)

# EOF
