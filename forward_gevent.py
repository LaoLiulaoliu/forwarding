#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is failed to forwarding data

from gevent import monkey; monkey.patch_all();
from gevent.coros import Semaphore

import sys
import socket
import time


__lock = Semaphore(1)

def log(msg):
    with __lock:
        print '[%s]: %s\n' % (time.ctime(), msg.strip())
#        sys.stdout.flush()


class Forwarding(object):
    def __init__(self, port, targethost, targetport):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(10)

        self.targethost = targethost
        self.targetport = targetport

    def pipe(self, source, target):
        while True:
            try:
                data = source.recv(1024)
                if not data: break
                target.send(data)
            except:
                break
        log('PipeThread done.')

    def run(self):
        while True:
            target_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_fd.connect((self.targethost, self.targetport))
            log('begin')

            client_fd, client_addr = self.sock.accept()
            log('new connect.{}'.format(client_addr))
            # two direct pipe
            g1 = gevent.spawn(self.pipe, target_fd, client_fd)
            g2 = gevent.spawn(self.pipe, client_fd, target_fd)
            time.sleep(10)
            gevent.joinall([g1, g2])


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
    app = Forwarding(8680, '127.0.0.1', 8580)
    app.run()
