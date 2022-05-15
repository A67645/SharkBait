import netifaces
from host_movel import Host_Movel
from random import choice


def get_ip():
        ipv6 = netifaces.ifaddresses('eth0')
        
        return ipv6[netifaces.AF_INET6][0]['addr']

def main():
    localhost = get_ip()

    host = Host_Movel(localhost=localhost, mcast_group='ff02::abcd:1', mcast_port=6666, hello_interval=2, dead_interv=8)

    host.start()


if __name__ == '__main__':
    main()