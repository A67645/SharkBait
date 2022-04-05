# multicast sender in server side
import socket
import json

while True:
    dict = { "fishes" : {1 : [140,120], 2 : [440,220], 3 : [335,127], 4 : [240,620], 5 : [344,523]},
             "Players" :{1 : [100,200,10], 2 : [155,255,8], 3 : [10,20,12]}
           }
    JSON_string = json.dumps(dict)
    # Create ipv6 datagram socket
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    # Allow own messages to be sent back (for local testing)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
    sock.sendto(JSON_string.encode('utf-8'), ("ff02::abcd:1", 8080))