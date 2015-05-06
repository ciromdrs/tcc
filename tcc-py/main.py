# -*- coding:utf-8 -*-

import os, webapp2, jinja2

from google.appengine.api import users, urlfetch
from google.appengine.ext import ndb

# Jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Handlers          
class Home(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        # Login/Logout URL
        if user:
            url = users.create_logout_url(self.request.uri)
            texto_link = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            texto_link = 'Login'
        
        # Recados
        recados = Recado.get_recados()
                
        self.responder('home.html',
             {'url' : url,
              'texto_link' : texto_link,
              'recados' : recados,
              })

    def post(self):
        user = users.get_current_user()
        texto = self.request.get('texto', None)
        autor = user.nickname() if user else 'Anônimo'
        url = self.request.get('url')
        imagem = None
        if url:
            imagem = urlfetch.Fetch(url).content
        
        Recado(parent = parent_key(), autor = autor, texto = texto, imagem = imagem).put()
        self.redirect('/')
    
    def responder(self, template, valores={}):
        self.response.write(
            JINJA_ENVIRONMENT.get_template(template).
                render(valores))

class ImgHandler(webapp2.RequestHandler):
    def get(self, key):
        r = ndb.Key(urlsafe=key).get()
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(r.imagem)

# Models
class Recado(ndb.Model):
    '''Modelo que representa um recado.'''
    autor = ndb.StringProperty()
    texto = ndb.TextProperty()
    data = ndb.DateTimeProperty(auto_now_add=True)
    imagem = ndb.BlobProperty()

    @classmethod
    def get_recados(cls):
        '''Pegando recados via NDB com cache automático'''
        q = Recado.query(ancestor=parent_key()).order(-Recado.data)
        return ndb.get_multi(q.fetch(10, keys_only=True)) # Auto-cache

class TimeLine(ndb.Model):
    '''Modelo que serve apenas para ser o Parent de todos os recados.'''
    pass

def parent_key():
    '''Criando Model ancestral para manter consistência no banco'''
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