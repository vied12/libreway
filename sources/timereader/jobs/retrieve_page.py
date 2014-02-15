#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Time Reader
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU Lesser General Public License
# -----------------------------------------------------------------------------
# Creation : 07-Jul-2013
# Last mod : 07-Jul-2013
# -----------------------------------------------------------------------------
from timereader.jobs import Job, job
from timereader import Article
from flask import Flask
import requests

app = Flask(__name__)
app.config.from_envvar('TIMEREADER_SETTINGS')

@job("Retrieve a page using readability")
class RetrievePage(Job):

	def run(self, url, thematic=None, user_id=None, source=None):
		if not (url.startswith("http://") or url.startswith("https://")):
			url = "http://%s" % url
		# parse the web page
		res = requests.get("http://www.readability.com/api/content/v1/parser?url=%s&token=%s" % 
			(url, app.config['READABILITY_PARSER_TOKEN']))
		parsed  = res.json()
		# save the article
		article = Article()
		article.title       = parsed.get('title')
		article.date        = parsed.get('date_published')
		article.content     = parsed.get('content')
		article.summary     = parsed.get('excerpt')
		article.link        = parsed.get('url')
		article.domain      = parsed.get('domain')
		article.count_words = parsed.get('word_count')
		article.user        = user_id
		article.thematic    = thematic
		article.type        = source
		article.save()

# EOF
