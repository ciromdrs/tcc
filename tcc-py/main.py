# -*- coding:utf-8 -*-

import os, webapp2, jinja2

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp.util import login_required

# Jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Handlers
class BaseHandler(webapp2.RequestHandler):
    def responder(self, template, valores={}):
        self.response.write(
            JINJA_ENVIRONMENT.get_template(template).
                render(valores))

class Home(BaseHandler):
    #@login_required
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
        recados = get_recados()
                
        self.responder('home.html',
             {'url' : url,
              'texto_link' : texto_link,
              'recados' : recados,
              })

    def post(self):
        user = users.get_current_user()
        texto = self.request.get('texto', None)
        
        if user:
            Recado(parent = parent_key(), autor = user.nickname(), texto = texto).put()
        else:
            pass
        self.redirect('/')

# Models
class Recado(ndb.Model):
    '''Modelo que representa um recado.'''
    autor = ndb.StringProperty()
    texto = ndb.TextProperty()
    data = ndb.DateTimeProperty(auto_now_add=True)

# Pegando recados via memcache ou DB
def get_recados():
    recados = memcache.get('recados')
    if not recados:
        recados = Recado.query(ancestor=parent_key()).order(-Recado.data).fetch(10)
        memcache.add(key='recados', value=recados, time=3)
    return recados

class TimeLine(ndb.Model):
    '''Modelo que serve apenas para ser o Parent de todos os recados.'''
    pass

# Criando Model ancestral para manter consistência no banco
def parent_key():
    tm = TimeLine.query().get()
    if not tm:
        tm = TimeLine()
        tm.put()
    return tm.key

# App
app = webapp2.WSGIApplication([
        ('/', Home),
    ], debug=True)