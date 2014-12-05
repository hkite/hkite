# -*- coding: utf-8 -*-
'''
Usage:
    render.py

Parameters:

Options:
    -h     Show this message
'''

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import jinja2
from jinja2 import Template
import requests
from collections import defaultdict

def main():
    url = 'https://spreadsheets.google.com/feeds/list/1We6YTBTZUMwxqRqWkRJs_lzmrzWhq5V_t93q7jw_dLw/od6/public/values?alt=json'
    res = requests.get(url).json()
    articles = defaultdict(list)
    for e in res['feed']['entry']:
        e['gsx$linkdescription']['$t'] = e['gsx$linkdescription']['$t'].replace('\n', '<br>')
        article_id = e['gsx$articleid']['$t'],
        articles[article_id].append({
            'article_id': e['gsx$articleid']['$t'],
            'article_title': e['gsx$articletitle']['$t'],
            'link': e['gsx$link']['$t'],
            'link_title': e['gsx$linktitle']['$t'],
            'link_description': e['gsx$linkdescription']['$t']
            })
    template = Template(open('template.html').read())
    for article_id, links in articles.iteritems():
        a_dir = 'l/%s' % article_id
        a_fn = '%s/index.html' % a_dir
        if not os.path.exists(a_dir):
            os.mkdir(a_dir)
        open(a_fn, 'w').write(template.render(links=links))

if __name__ == '__main__':
    main()

