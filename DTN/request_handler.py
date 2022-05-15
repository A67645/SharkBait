import socket
from threading import Thread, RLock
from json import loads, dumps
from time import time
import send_data

class Receive_Handler(Thread):
    def __init__(self, lock, request, localhost, mcast_addr, mcast_port):

        Thread.__init__(self)
        self.localhost = localhost
        self.lock = lock
        self.mcast_port = mcast_port
        self.mcast_addr = mcast_addr
        self.skt, _ = request  # importar da Class SOCKET
        self.msg = loads(self.skt.decode("utf-8"))
        self.addr = self.msg['source']
    
    def run(self):
        try:
            if self.msg["type"] == "Request":
                self.lock.acquire()
                self.hello_handler()
                self.send_data()

            elif self.msg["type"] == "Reply":
                self.lock.acquire()
                if self.msg["source"]==self.localhost:
                    print("recebi do servidor")
                
        
        except Exception as e:
            print(e.with_traceback())    
              
        finally:
            self.lock.release()


    def send_data(self):
        self.msg['type'] = "Reply"
        send_data.send(self.msg, self.localhost, self.mcast_port)

    def hello_handler(self):
        test_print = self.msg['type'] + " from: " + self.msg['source']
        print(test_print)    