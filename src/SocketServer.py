import Basic

BASIC = Basic.Basic()

class SocketServer():

    def UDPUnicastServer(self):

        udp_socket = BASIC.socket.socket(socket.AF_INET,
                                         socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET,
                              socket.SO_REUSEADDR, 1)
        return udp_socket
        
