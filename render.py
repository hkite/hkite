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
    if not os.path.exists('l'):
        os.mkdir('l')
    url = 'https://spreadsheets.google.com/feeds/list/1We6YTBTZUMwxqRqWkRJs_lzmrzWhq5V_t93q7jw_dLw/od6/public/values?alt=json'
    res = requests.get(url).json()
    articles = defaultdict(list)
    for e in res['feed']['entry']:
        e['gsx$linkdescription']['$t'] = e['gsx$linkdescription']['$t'].replace('\n', '<br>')
        article_id = e['gsx$articleid']['$t'],
        articles[article_id].append({
            'article_id': e['gsx$articleid']['$t'],
            'article_title': e['gsx$articletitle']['$t'],
            'link': e.get('gsx$link', {}).get('$t', ''),
            'link_title': e['gsx$linktitle']['$t'],
            'link_description': e['gsx$linkdescription']['$t']
            })

    for article_id in articles:
        articles[article_id] = list(enumerate(articles[article_id]))

    template = Template(open('template.html').read())
    for article_id, links in articles.iteritems():
        a_dir = 'l/%s' % article_id
        a_fn = '%s/index.html' % a_dir
        if not os.path.exists(a_dir):
            os.mkdir(a_dir)
        open(a_fn, 'w').write(template.render(
            article_title=links[0][1]['article_title'],
            links=links
            ))

if __name__ == '__main__':
    main()

