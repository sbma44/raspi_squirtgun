import sys
import json
import time
import argparse
import socket
import websocket
import threading
import uuid
from squirtgun import Squirtgun
from settings import *

class Thread(threading.Thread):
    """ Convenience method for process threads """
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.setDaemon(True)
        self.start()

def keepalive(sgc):  
    # wait until keepalives are enabled...
    while not sgc.send_keepalives:
        time.sleep(0.01)

    while not sgc.terminate:
        if sgc.send_keepalives:
            print 'sending keepalive'
            sgc.ws_tx.send(json.dumps({'keepalive': sgc.uuid}))
        time.sleep(RECONNECT_SLEEP)

class SquirtgunClient(object):
    """Maintains a websocket connection with the server"""
    def __init__(self, host):
        super(SquirtgunClient, self).__init__()
        # self.squirtgun = Squirtgun(debug='--debug' in sys.argv)
        self.squirtgun = Squirtgun(debug='--debug' in sys.argv)        
        self.host = host
        self.terminate = False
        self.send_keepalives = False
        self.uuid = uuid.uuid1().get_hex()
        self.pingpong = Thread(keepalive, self)

        self.ws_rx = None
        self.ws_tx = None

    def run(self):        
        while self.terminate == False:
            try:
                if hasattr(self, 'ws_rs'):
                    del self.ws_rx
                if hasattr(self, 'ws_tx'):
                    del self.ws_tx

                self.ws_rx = websocket.create_connection('%s/receive' % self.host)
                self.ws_tx = websocket.create_connection('%s/submit' % self.host)
                self.send_keepalives = True

                print 'connected!'
                while True and not self.terminate:
                    msg = json.loads(self.ws_rx.recv())
                    if msg.get('handle') == 'FIRE':
                        self.squirtgun.pulse(float(msg.get('text', '0.5')))
            except websocket.WebSocketConnectionClosedException, e:
                print 'connection closed'
                self.send_keepalives = False
            except socket.error, e:
                if e.errno == 61:
                    print 'connection refused'
                else:
                    print 'socket error number %d' % e.errno
                self.send_keepalives = False
            except Exception, e:            
                self.send_keepalives = False    
                self.terminate = True
                raise e

            print 'sleeping %d seconds...' % RECONNECT_SLEEP
            time.sleep(RECONNECT_SLEEP)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Listen for squirtgun commands.')
    parser.add_argument('--host', type=str, nargs=1, help='Specify a host URL', metavar=('URL',))
    args = parser.parse_args()

    target_host = HOST
    if args.host is not None:
        target_host = args.host[0]

    print target_host

    sgc = SquirtgunClient(target_host)
    sgc.run()

