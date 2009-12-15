#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import sqlite3

web.config.debug = False

db = web.database(dbn='sqlite', db='verycd.sqlite3.db')

urls = (
	'/', 'index', 
)


render = web.template.render('templates/')

app = web.application(urls, globals())

class index:
	def GET(self):
		i = web.input(id=None,page='1',q=None,download=None)
		if i.id:
			myvar = dict(id=i.id)
			rec = db.select('verycd',vars=myvar,where="verycdid=$id")
			for r in rec:
				fl = None
				if i.download:
					links = r['ed2k'].split('`')
					links = [ x for x in links if 'ed2k:' in x ]
					fl = '<br>\n'.join(links)
				return render.id([r,fl,str(r['verycdid'])])
			return render.error(404)
		else:
			if not i.q:
				vc = db.select('verycd',order='updtime DESC',limit=20,offset=20*(int(i.page)-1))
				num = db.select('verycd',what="count(*) as count")[0].count
				arg = '/?page'
			else:
				qs = i.q.split(' ')
				qs = [ 'title like \'%'+x+'%\'' for x in qs ]
				where = ' and '.join(qs)
				vc = db.select('verycd',order='updtime DESC',limit=20,\
					offset=20*(int(i.page)-1),where=where)
				num = db.select('verycd',what="count(*) as count",where=where)[0].count
				arg = '/?q='+i.q+'&page'
			prev = int(i.page)-1 == 0 and '1' or str(int(i.page)-1)
			next = int(i.page)+1 <= (num-1)/20+1 and str(int(i.page)+1) or i.page
			end = str((num-1)/20+1)
			pages = [prev,next,end]
			left = min(4,int(i.page)-1)
			right = min(4,int(end)-int(i.page))
			if left < 4:
				right = min(8-left,int(end)-int(i.page))
			if right < 4:
				left = min(8-right,int(i.page)-1)
			while left > 0:
				pages.append(str(int(i.page)-left))
				left -= 1
			j = 0
			while j <= right:
				pages.append(str(int(i.page)+j))
				j += 1
			return render.index([vc,pages,arg,i.q,num])

if __name__ == "__main__":
	web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
	app.run()
