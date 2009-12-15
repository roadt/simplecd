#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# download.py: download with report
#
# author: observer
# email: jingchaohu@gmail.com
# blog: http://obmem.com
# last edit @ 2009.12.16
import os,sys
import urllib2
from time import time,sleep

path = os.path.dirname(os.path.realpath(sys.argv[0]))

#proxies = {'http':'http://proxyaddress:port'}
#proxy_support = urllib2.ProxyHandler(proxies)
#opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
#urllib2.install_opener(opener)

#functions
def report(blocknum, bs, size, t):
    if size == -1:
        print '%10s' % (str(blocknum*bs)) + ' downloaded | Speed =' + '%5.2f' % (bs/t/1024) + 'KB/s'
    else:
        percent = int(blocknum*bs*100/size)
        print '%10s' % (str(blocknum*bs)) + '/' + str(size) + 'downloaded | ' + str(percent) + '% Speed =' + '%5.2f'%(bs/t/1024) + 'KB/s'
    
def httpfetch(url, headers={}, reporthook=report, postData=None, report=True):
    ok = False
    for _ in range(10):
        try:
            reqObj = urllib2.Request(url, postData, headers)
            fp = urllib2.urlopen(reqObj)
            headers = fp.info()
            ok = True
            break
        except:
            sleep(1)
            continue            

    if not ok:
        open(path+'/errors','a').write(url+'\n')
        return ''

    rawdata = ''
    bs = 1024*8
    size = -1
    read = 0
    blocknum = 0
    
    if reporthook and report:
        if "content-length" in headers:
            size = int(headers["Content-Length"])
        reporthook(blocknum, bs, size, 1)
        
    t0 = time()
    while 1:
        block = ''
        try:
            block = fp.read(bs)
        except:
            open(path+'/errors','a').write(url+'\n')
            return ''
        if block == "":
            break
        rawdata += block
        read += len(block)
        blocknum += 1
        if reporthook and report:
            reporthook(blocknum, bs, size, time()-t0)
        t0 = time()
            
    # raise exception if actual size does not match content-length header
    if size >= 0 and read < size:
        raise ContentTooShortError("retrieval incomplete: got only %i out "
                                    "of %i bytes" % (read, size), result)

    return rawdata
    
if __name__ == '__main__':    
    url = 'http://www.verycd.com'

    #test it
    data = httpfetch(url)
    open('down','w').write(data)

