#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Simulate app.yaml of Google App Engine

import web
import mainweb
import serviceweb

urls = (
  "/favicon.ico", "static",
  "/js/tipitaka.js", "static"
)

class static:
  def GET(self):
    if web.ctx.path == '/js/tipitaka.js':
      with open('app/all_compiled.js', 'r') as f:
        return f.read()

    if web.ctx.path == '/favicon.ico':
      with open('common/app/img/favicon.ico', 'r') as f:
        return f.read()

    raise web.notfound()


staticApp = web.application(urls, globals())


mapping = (
    "/favicon.ico", staticApp,
    "/js/tipitaka.js", staticApp, 
    "/robots.txt", serviceweb.app, 
    "/wordJson/", serviceweb.app, 
    "/html/", serviceweb.app, 
    "/", mainweb.app) 


class customApp(web.application):
  def _delegate_sub_application(self, dir, app):
    return app.handle_with_processors()


app = customApp(mapping)
application = app.wsgifunc()

if __name__ == '__main__':
  app.run()

