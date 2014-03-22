#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://everet.org/2012/03/python-forwarding-redirecting-tcp-monitor.html

import sys
import socket
import time
import gevent
import threading


def log(msg):
    print '[%s]: %s\n' % (time.ctime(), msg.strip())
#    sys.stdout.flush()

class PipeThread(threading.Thread):
    def __init__(self, source, target):
        super(PipeThread, self).__init__()
        self.source = source
        self.target = target

    def run(self):
        while True:
            try:
                data = self.source.recv(1024)
                if not data: break
                self.target.send(data)
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
            
            self.target_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.target_fd.connect((self.targethost, self.targetport))
            log('new connect.{}'.format(client_addr))
            # two direct pipe
            PipeThread(self.target_fd, client_fd).start()
            PipeThread(client_fd, self.target_fd).start()


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
    Forwarding(8680, '127.0.0.1', 8580).run()
