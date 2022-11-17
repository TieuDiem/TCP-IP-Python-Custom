__all__=[]

__doc__="""


"""
from client.lib import *
from function import *

class Sock(threading.Thread):

    def __init__( self,host_:str, port_:int, parent_=None,)->None:
                    
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host_, port_)
        self.host = host_
        self.port = port_
       
        self.isConnected=False
        self.setDaemon =True

        try:
            print(f"*** Try connecting to {self.host}:{self.port}...")
            self.__socket.connect(server_address)
            print(f"*** Try connecting to {self.host}:{self.port}...Connected")
            self.isConnected =True
            self.start()
            print(f'Setup Communication Successfully ...')

        except Exception as e :
            print(f'*** Can not connect with sever: {e}')
            self.isConnected =False

    def run(self):       
        while(True):
            if self.isConnected==False:
                break
            Identify ="START_CONNECTION"
            self.send_message(Identify)
            recv_msg=self.receive(MAX_BUFFER_SIZE)

            str_receive , img_receive =ExtractData(recv_msg)
          
    def receive(self, size):
        try:
            data =""
            if self.isConnected:
                data=  self.__socket.recv(size)
            else:
                data=""
            print(f'data receive: {data}')
        except Exception as e:
            self.join()
            return ""
        return data

    def send_message(self, msg):
        try:
            if  self.isConnected:
                self.__socket.sendall(bytes(msg, "utf-8"))
        except Exception as e:
            self.join()
    def close_socket(self):
        if self.isConnected:
            self.__socket.shutdown(SHUT_RDWR)
            self.__socket.close()

if __name__ =="__main__":
    sock = Sock(HOST, PORT)
