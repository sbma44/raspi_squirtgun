import sys
import json
import time
import socket
import websocket
from squirtgun import Squirtgun
from settings import *

def main():
    sg = Squirtgun(debug='--debug' in sys.argv)
    ws = websocket.create_connection(RX_URL)
    print 'connected!'
    while True:
        msg = json.loads(ws.recv())
        if msg.get('handle') == 'FIRE':
            sg.pulse(float(msg.get('text', '0.5')))

if __name__ == '__main__':
    continue_reconnecting = True
    while continue_reconnecting:
        try:
            main()
        except websocket.WebSocketConnectionClosedException, e:
            print 'connection closed'
        except socket.error, e:
            if e.errno == 61:
                print 'connection refused'
            else:
                print 'socket error number %d' % err.errno
        except Exception, e:
            continue_reconnecting = False
            raise e
        print 'sleeping %d seconds...' % RECONNECT_SLEEP
        time.sleep(RECONNECT_SLEEP)

