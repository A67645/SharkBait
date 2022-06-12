import netifaces

#obter o ip do servidor ou host movel, qualquer interface server
def get_ip():
        ipv6 = netifaces.ifaddresses('eth0')
        
        return ipv6[netifaces.AF_INET6][0]['addr']

#obter ip do router associado à rede/interface
def get_ip_router(interface):
    ipv6 = netifaces.ifaddresses(interface)
    return ipv6[netifaces.AF_INET6][0]['addr']
