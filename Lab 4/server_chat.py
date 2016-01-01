
# server_chat.py
 
import sys, socket, select
import threading
from threadpool import makeRequests, ThreadPool
import time
import socket
import re

exit = 0

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 8000
studentID = '677cfc77e52778a3d5741cb5d5f358c537c28f5134d63e4b7f8376f73315922c'
backlog = 5
threads = 5

def chat_server():

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)
 
    # add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket)
	
	main = ThreadPool(threads)
	main.createWorkers(threads)
    
	print ("Chat server started on port " + str(PORT))
	
	while 1:
	
		if exit == 1:
			sys.exit()
		else:
			# get the list sockets which are ready to be read through select
			# 4th arg, time_out  = 0 : poll and never block
			ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
			
			requests = makeRequests(use_client, ready_to_read)
			for req in requests:
				main.putRequest(req)
				main.poll()
			server_socket.close
		if main.dismissedWorkers:
			print("Joining all dismissed worker threads...")
			main.joinAllDismissedWorkers()

def use_client(ready_to_read):
	global exit

	CHATROOM_NAME = ''
	SERVER_IP = socket.gethostbyname(socket.gethostname()) 
	SERVER_PORT = str(PORT)
	ROOM_REF = '1'
	JOIN_ID = '1'
	CLIENT_NAME = ''
	
	while 1:
		for sock in ready_to_read:
			# a new connection request recieved
			if sock == server_socket: 
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
				print ("Client (%s, %s) connected" % addr)
				 
				broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
			 
			# a message from a client, not a new connection
			else:
				# process data recieved from client, 
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER)
					if "KILL_SERVICE" in data:
						print ("closing...")
						exit = 1
					if "HELO" in data:
						print(data + "IP: " + socket.gethostbyname(socket.gethostname()) + "\nPort: " + str(port) + "\nStudentID: " + studentID + "\n")
						#client.send(data + "IP: " + socket.gethostbyname(socket.gethostname()) + "\nPort: " + str(port) + "\nStudentID: " + studentID + "\n")
					if "JOIN_CHATROOM:" in data:
						join_lines = data.split('\n')
						CHATROOM_NAME = re.sub('JOIN_CHATROOM: ', '', join_lines[0])
						CLIENT_NAME = re.sub('CLIENT_NAME: ', '', join_lines[3])
						print (CLIENT_NAME)
						#client.send('JOINED_CHATROOM: ' + CHATROOM_NAME + '\nSERVER_IP: ' + SERVER_IP + '\nPORT: ' + SERVER_PORT + '\nROOM_REF: ' + ROOM_REF + '\nJOIN_ID: ' + JOIN_ID + '\n')
					if "CHAT:" in data:
						if ROOM_REF != '':
							chat_lines = data.split('\n')
							message = re.sub('MESSAGE: ', '', chat_lines[3])
							#client.send('CHAT: ' + ROOM_REF + '\nCLIENT_NAME: ' + CLIENT_NAME + '\nMESSAGE: ' + message + '\n')
					if data:
						# there is something in the socket
						print(data)
						broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
					else:
						# remove the socket that's broken    
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)

						# at this stage, no data means probably the connection has been broken
						broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

				# exception 
				except:
					broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
					continue

		server_socket.close()


# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":
    sys.exit(chat_server())
