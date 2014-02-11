import Basic

BASIC = Basic.Basic()

class SocketServer():

    def UDPUnicastServer(self):

        udp_socket = BASIC.socket.socket(BASIC.socket.AF_INET,
                                         BASIC.socket.SOCK_DGRAM)
        udp_socket.setsockopt(BASIC.socket.SOL_SOCKET,
                              BASIC.socket.SO_REUSEADDR, 1)
        return udp_socket


if __name__ == "__main__":

    SS = SocketServer()
    udp_server = SS.UDPUnicastServer()
    udp_server.bind(("", 12345))
    while 1:
        message, address = udp_server.recvfrom(188)
        print "Got data from", address, ": " 
