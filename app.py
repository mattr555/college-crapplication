import sys, os
lib_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
if lib_folder not in sys.path:
    sys.path.insert(0, lib_folder)

import bottle
import markovify
import json
from google.appengine.ext import ndb
from google.appengine.api import memcache
from secret import essay_password

class Essay(ndb.Model):
    content = ndb.TextProperty()
    colleges = ndb.StringProperty(repeated=True)
    author = ndb.StringProperty()

@bottle.route('/run/<sentences:int>')
@bottle.route('/run/<sentences:int>/<college>')
def run(sentences, college=None):
    essays = None
    if college:
        essays = Essay.query(Essay.colleges == college)
    else:
        essays = Essay.query()

    text = ''
    for i in essays:
        text += i.content + '\n'

    gen = markovify.Text(text)
    resp = ''
    for i in range(sentences):
        this = gen.make_sentence() #returns None if the generated is too much like the corpus -_-
        if this:
            resp += this + ' '
    return resp or 'sorry, not enough corpus yet'

@bottle.route('/add_essay', method="POST")
def add_essay():
    req = bottle.request.forms
    if not req.get('password') == essay_password:
        return bottle.abort(401, 'denied')
    essay = Essay(content=req.get('content'), colleges=req.get('colleges').split(','), author=req.get('author'))
    essay.put()
    return 'ok'

@bottle.route('/colleges_available')
def colleges_available():
    cache = memcache.get('colleges')
    if cache:
        return json.dumps(cache.split(','))
    s = set()
    for e in Essay.query():
        for c in e.colleges:
            s.add(c)
    memcache.set(key='colleges', value=','.join(s), time=60*10)
    return json.dumps(list(s))

@bottle.route('/patrons')
def patrons():
    cache = memcache.get('patrons')
    if cache:
        resp = cache
    else:
        s = set()
        for e in Essay.query():
            s.add(e.author)
        resp = '\n'.join(s)
        memcache.set(key='patrons', value=resp, time=60*10)
    bottle.response.content_type = 'text/plain'
    return 'This work would not be possible without the generous donations of the following patrons of the arts:\n\n' + resp

@bottle.route('/')
@bottle.route('/<fn:path>')
def index(fn='index.html'):
    return bottle.static_file(fn, root='./static')

bottle.debug(True)
bottle.run(server='gae')
application = bottle.app()
