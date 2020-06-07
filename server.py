import socket
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 1234
HEAD = 10

sock.listen()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))

socket_list = [sock]
clients = {}

def receive_message(client_socket):
	try:
		message_header =  client_socket.recv(HEAD)
		if not len(message_header):
			return False
		msglen = int(message_header.decode('utf-8').strip())
		return {'head': message_header, 'data': client_socket(msglen)
	except:
		return False


while True:
	read_socket, _, exception_socket = select.select(socket_list, [], socket_list)
	for notified_socket in read_socket:
		if notified_socket == sock:
			client_socket, client_address = sock.accept()
			user = receive_message(client_socket)
			if user is False:
				continue
			clients[client_socket] = user
			print(f'Connection from: {client_address[0]}:{client_address[1]}, username: {user["data"]}')
		else:
			message = receive_message(notified_socket)
			if message is False:
				print(f'Closed connection from: {clients[notified_socket]["data"].decode("utf-8")}'
'				socket_list.remove(notified_socket)
				del clients[notified_socket]
				continue
			user = clients[notified_socket]
			print(f'Receive message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
			for client_socket in clients:
				if client_socket != notified_socket:
					client_socket.send(user["head"] + user["data"] + message["head"] + message["data"]
