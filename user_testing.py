from ws4py.client.threadedclient import WebSocketClient
import time, random

class DummyClient(WebSocketClient):
    def opened(self):
        self.send("user-bb0000000001")

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        print m
        
if __name__ == '__main__':
    try:
        print("user client 1")
        ws = DummyClient('ws://192.168.1.2:8001/', protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
