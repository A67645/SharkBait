from audioop import mul
import json
import socket
import threading
import struct
import time
import unicast.ifaces as ifaces
import ipaddress

class Router():

    unicast_socket = None

    def __init__(self):
        self.unicast_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 7777) # '2001:0::10'
        self.unicast_socket.bind((host,port))
        # Initialise socket for IPv6 datagrams
        self.multicast_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Allows address to be reused
        self.multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #multicast_socket.bind(('', 6666))
        # Allow messages from this socket to loop back for development
        self.multicast_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        # Construct message for joining multicast group
        #print(ifaces.get_ip_router('eth2'))
        #ipv6mr_interface = ipaddress.ip_address(ifaces.get_ip_router('eth2')).packed
        #ipv6_mreq = socket.inet_pton(socket.AF_INET6, "ff02::abcd:1") + ipv6mr_interface
        #multicast_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, ipv6_mreq)
        #mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::abcd:1"), (chr(0) * 16).encode('utf-8'))
        #multicast_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
        mc_address = ipaddress.IPv6Address('ff02::abcd:1')
        listen_port = 6666
        interface_index = socket.if_nametoindex('eth2')
        self.multicast_socket.bind((str(mc_address), listen_port, 0, interface_index))
        self.multicast_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP,
                   struct.pack('16sI', mc_address.packed, interface_index))

    def send_to_server(self, message):
        self.unicast_socket.sendto(message.encode('utf-8'),('2001:0::10',7777))

    def receive_from_server(self):
        data,addr = self.unicast_socket.recvfrom(2048)
        return data.decode('utf-8')

    def receive_from_multicast(self):

        # Receive message from multicast group
        data, addr = self.multicast_socket.recvfrom(2048)

        print(data.decode('utf-8'))

        return data.decode('utf-8')

    def send_to_multicast(self, message):
        self.multicast_socket.sendto(message.encode('utf-8'), ("ff02::abcd:1", 6666))

    def handle(self):

        while True:
            message_host = self.receive_from_multicast()
            self.send_to_server(message_host)
            message_server = self.receive_from_server()
            time.sleep(1)
            self.send_to_multicast(message_server)

    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

router = Router()
router.main()
