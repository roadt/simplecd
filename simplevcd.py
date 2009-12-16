#!/usr/bin/env python
#coding: utf-8
#
#
#
#
#
import sys, time
from daemon import Daemon
from Queue import Queue
import fetchvc

class MyDaemon(Daemon):
	q = Queue()
	def run(self):
		while True:
			keyword = self.q.get()
			fetchvc.search(keyword)
			self.q.task_done()
	def put(self,keyword):
		self.q.put(keyword)

def addsearch(keyword):
	daemon = MyDaemon('/tmp/simplevc.pid')
	daemon.put(keyword) 
 
if __name__ == "__main__":
	daemon = MyDaemon('/tmp/simplevc.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
