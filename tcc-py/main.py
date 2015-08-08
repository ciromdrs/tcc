# -*- coding:utf-8 -*-

import os, webapp2, jinja2

from google.appengine.api import memcache
from google.appengine.api import users, urlfetch
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import login_required
 

# Jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Handlers          
class Home(webapp2.RequestHandler):
    @login_required
    def get(self):
        user = users.get_current_user()
        
        # Logout URL
        url = users.create_logout_url(self.request.uri)
        
        # Post
        posts = Post.get_posts()
                
        self.respond('home.html', {'url' : url, 'posts' : posts, 'user' : user})

    def post(self):
        user = users.get_current_user()
        text = self.request.get('text', None)
        author = user.nickname() if user else 'Anonymous'
        url = self.request.get('url')
        image = None
        if url:
            image = urlfetch.Fetch(url).content
        
        Post(parent = parent_key(), author = author, text = text, image = image).put()
        self.redirect('/')
    
    def respond(self, template, values={}):
        self.response.write(
            JINJA_ENVIRONMENT.get_template(template).
                render(values))

class ImgHandler(webapp2.RequestHandler):
    def get(self, key):
        img = memcache.get(key)
        if not img:        
            img = ndb.Key(urlsafe=key).get().image
            memcache.set(key, img) 
        
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(img)

# Models
class Post(ndb.Model):
    '''Post model.'''
    author = ndb.StringProperty()
    text = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    image = ndb.BlobProperty()

    @classmethod
    def get_posts(cls):
        '''Retrieves posts from datastore'''
        q = Post.query(ancestor=parent_key()).order(-Post.date)
        return q.fetch(10)

class TimeLine(ndb.Model):
    '''TimeLine model. It's the Parent entity of all posts.'''
    pass

def parent_key():
    '''Creates an ancestor model to ensure consistency and returns its key'''
    tm = TimeLine.query().get()
    if not tm:
        tm = TimeLine()
        tm.put()
    return tm.key

# App
app = webapp2.WSGIApplication([
        ('/', Home),
        (r'/img/(.+)', ImgHandler),
    ], debug=True)