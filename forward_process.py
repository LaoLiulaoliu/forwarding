#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is failed to forwarding data
# socket, file handler, database connection... can not be dumped

import sys
import socket
import time
import multiprocessing
import cPickle

pool = multiprocessing.Pool(processes=3)

def log(msg):
    print '[%s]: %s\n' % (time.ctime(), msg.strip())
#    sys.stdout.flush()



# If this function in class Forwarding, the following error will happen
# PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup __builtin__.instancemethod failed
def pipe(self, source, target):
    if isinstance(source, tuple):
        source_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        source_fd.connect(source)
    else:
        source_fd = cPickle.loads(source)

    if isinstance(target, tuple):
        target_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_fd.connect(target)
    else:
        target_fd = cPickle.loads(target)

    while True:
        try:
            data = source_fd.recv(1024)
            if not data: break
            target_fd.send(data)
        except:
            break
    log('PipeThread done')


class Forwarding(object):
    def __init__(self, port, targethost, targetport):
        self.targethost = targethost
        self.targetport = targetport
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(10)

    def run(self):
        while True:
            client_fd, client_addr = self.sock.accept()
            log('new connect.{}'.format(client_addr))

            # two direct pipe
            result = []
            # multiprocess can not pass object, 'TypeError: expected string or Unicode object, NoneType found'
            # TypeError: a class that defines __slots__ without defining __getstate__ cannot be pickled
            result.append( pool.apply_async(pipe, ((self.targethost, self.targetport), cPickle.dumps(client_fd, -1))) )
            result.append( pool.apply_async(pipe, (cPickle.dumps(client_fd, -1), (self.targethost, self.targetport))) )
            pool.close()
            pool.join()
#            for res in result:
#                print res.get()


if __name__ == '__main__':
#    try:
#        port = int(sys.argv[1])
#        targethost = sys.argv[2]
#        try: targetport = int(sys.argv[3])
#        except IndexError: targetport = port
#    except (ValueError, IndexError):
#        print 'Usage: %s port targethost [targetport]' % sys.argv[0]
#        sys.exit(1)
#
#    #sys.stdout = open('forwaring.log', 'w')
#    Forwarding(port, targethost, targetport).start()
    Forwarding(8687, '127.0.0.1', 8580).run()
