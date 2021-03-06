from threading import Thread, RLock
from time import sleep
from json import dumps
import struct
import socket

class HelloSender(Thread):
    def __init__(self, lock, hello_interval, localhost, ttl, mcast_group, mcast_port):
        Thread.__init__(self)
        self.gameState = {"fishes" : {}, "players" : {}}
        self.lock           = lock
        self.hello_interval = hello_interval
        self.ttl            = ttl
        self.localhost      = localhost
        self.mcast_group    = mcast_group
        self.mcast_port     = mcast_port

    def set_gameState(self, gs):
        self.gameState = gs

    def run(self):
        while True:
            try:
                self.lock.acquire()
                self.hello_sender()

            except Exception as e:
                print('Failed: {}'.format(e.with_traceback()))

            finally:
                self.gameState = Host_Movel.gameState
                self.lock.release()
                sleep(self.hello_interval)
                print(f'GAME MAP: {self.gameState}')



    def create_socket(self):

        try:
            # Criar o socket do client
            client_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            client_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, self.ttl)
            client_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)

            return client_sock

        except Exception as sock_error:
            print('Failed to create socket: {}'.format(sock_error))

    def hello_sender(self):
        try:
            client_sock = self.create_socket()

                # Messagem a ser enviada
            self.msg = {
                "type": "Request",
                "source": self.localhost,
                "destination" : "2001:0::10",
                "data" : (0,0)
            }

                #print('Sending multicast message to the multicast group ...')
                #print(self.msg)
            client_sock.sendto(dumps(self.msg).encode('utf-8'), (self.mcast_group,self.mcast_port))

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

        finally:
            client_sock.close()
