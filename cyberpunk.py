#!/usr/bin/python
# -*- coding: UTF-8 -*-

from os import listdir
import sys
reload(sys)
from os.path import isfile, join
import codecs
import pytumblr

sys.setdefaultencoding('utf-8')

# Authenticate via OAuth
tumblr_oauth = open('OAuth.tumblr')
consumer_key, consumer_secret, oauth_token, oauth_secret = tumblr_oauth.readlines()

client = pytumblr.TumblrRestClient(
                                    consumer_key.strip(),
                                    consumer_secret.strip(),
                                    oauth_token.strip(),
                                    oauth_secret.strip()
)

source_dir = '.'
source_folder = [ f for f in listdir(source_dir) if isfile(join(source_dir, f)) ]

for source_file in source_folder:

    if source_file.split('.')[1] != 'csv':
        continue

    if source_file == 'redakce.csv':
        continue

    category_name = source_file.split('.')[0]
    source = codecs.open(source_dir + '/' + source_file, 'r', 'iso-8859-2')

    for line in source.readlines():

        # fields: CDATE;CNAME;CPATH;CMARK;CAUTOR;CPEREX;|
        parsed = line.strip().split(';')

        if parsed[0] == 'CDATE':
            continue

        if parsed[0] == '':
            continue

        day, time = parsed[0].split()
        day = day.replace('22001', '2001')

        try:
            author = parsed[3]
        except IndexError:
            author = 'countzero'

        custom_post = day.replace('/', '-') + ' | ' + author + '<br>' + parsed[2] + '<br>'

        try:
            custom_post += ' [ ' + '<a href="' + parsed[4] + '">link</a> ]'
        except IndexError:
            pass

        client.create_text("kyblpunk", state="published", slug="testing-text-posts", title=parsed[1], body=custom_post, date=day, tags=[category_name])