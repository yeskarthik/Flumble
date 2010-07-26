import sys
import os
import urllib2
import urllib
import json

def download_file (id, url, base_filepath):
    file_path = os.path.join (base_filepath, id + '.jpg')
    if os.path.exists (file_path):
        return
    download_url = urllib2.urlopen (url)
    download_file = file(file_path, 'wb')
    download_file.write(download_url.read())
    download_file.close()


QUERY_TEMPLATE = """SELECT * FROM flickr.photos.search(%s) WHERE user_id="%s" and extras="url_m" and text="%s" and tags="%s" and sort="interestingness-desc"
"""

def form_query_url (parameters):
    return QUERY_TEMPLATE % (parameters.get('limit', '1'),
                             parameters.get('user_id', ''),
                             parameters.get('text', ''),
                             parameters.get('tags', ''))

YQL_URL = 'http://query.yahooapis.com/v1/public/yql?format=json'

def url_for_query (query):
    encoded_query = urllib.urlencode({'q': query})
    query_url = '%s&%s' % (YQL_URL, encoded_query)
    return query_url

def photos_for_query (parameters):
    query_url = url_for_query(form_query_url(parameters))
    response = urllib2.urlopen(query_url)
    data = json.loads(response.read())
    for p in data['query']['results']['photo']:
        yield (p['id'], p['url_m'])

USERID_QUERY_TEMPLATE = 'select * from flickr.people.findbyusername where username="%s"'
def userid_for_username (username):
    query = USERID_QUERY_TEMPLATE % username
    query_url = url_for_query(query)
    response = urllib2.urlopen(query_url)
    data = json.loads(response.read())
    return data['query']['results']['user']['nsid']

if __name__ == '__main__':
    for id, url in photos_for_query({'user_id': userid_for_username('karthikssn'), 'limit':150}):
        print id
        download_file (id, url, '.')
