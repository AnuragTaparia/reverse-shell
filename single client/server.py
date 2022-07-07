import socket
import sys

#this function create socket for connecting two pc
def socket_create():
    try:
        global host 
        global port 
        global soc
        host = ''
        port = 9999
        soc = socket.socket()
    except socket.error as err:
        print("Socket creation failed due to : "+str(err))

#this function bind socket to port and wait for connection
def bind_socket():
    try:
        global host
        global port
        global soc
        print("Binding to the port "+ str(port))
        soc.bind((host,port))
        soc.listen(10)
    except socket.error as err:
        print("SOcket binding error: "+ str(err) + "\nRetrying...")
        bind_socket()

#this function establish connection with client since socket must be listening to them
def socket_accept():
    conn, address = soc.accept()
    print("Connection has been establish || IP "+ address[0] +" | port "+ str(address[1]))
    send_command(conn)
    #conn.close()

#this function send the commands
def send_command(conn):
    while True:
        cmd = input()
        if cmd == "bye":
            print("connection closing...")
            conn.send(str.encode(cmd))# for sending the "bye" cmd so that client can also exit the program
            conn.close()
            soc.close()
            sys.exit()
        #str.encode() is used because data is send in bytes and we(user) see it in string 
        #that means 'cmd' is in string
        if len(str.encode(cmd)) > 0: 
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8") #storing client response after converting byte to string
            print(client_response, end="")

def main():
    socket_create()
    bind_socket()
    socket_accept()

main()
