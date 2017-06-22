#!/usr/bin/env python3

import sys
import csv
import re
import requests
from lxml import html

OUTPUT_FILE = "wikipedia_answers.csv"
REGEX = re.compile(r'^/+')    # because of shazams '//shazam.com/' link

def args_error():
    print("""Arguments error.
Usage:
  {} <input_file>""".format(sys.argv[0]),
          file=sys.stderr)
    sys.exit(1)

def get_wiki_urls(input_file):
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile, quotechar='"')
        return [row[0] for row in reader]

def get_url_from_wiki(wiki_url):
    respond = requests.get(wiki_url)
    tree = html.fromstring(respond.content)
    link = map(lambda x: x.xpath('..//a[1]/@href'),
               filter(lambda x: 'Website' in str(x.text),
                      tree.xpath('//table//th')))
    url = link.__next__()[0]
    return trimed_url(url)

def trimed_url(url):
    return REGEX.sub('', url)

def main():
    if len(sys.argv) != 2:
        return args_error()
    wiki_urls = get_wiki_urls(sys.argv[1])

    sites_iter = map(get_url_from_wiki, wiki_urls)

    with open(OUTPUT_FILE, 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(['wikipedia_page', 'website'])
        for wikipage, site in zip(wiki_urls, sites_iter):
            writer.writerow([wikipage, site])

if __name__ == '__main__':
    main()
