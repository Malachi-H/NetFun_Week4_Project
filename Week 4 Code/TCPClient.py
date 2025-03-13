from socket import *
serverName = '' #replace with your ip address
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Input a lower case sentence : ')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server : ' + modifiedSentence.decode())
clientSocket.close()
print("complete")
