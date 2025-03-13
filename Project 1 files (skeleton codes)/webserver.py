#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket

#Fill in start
serverPort = 8080
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
#Fill in end

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()   #Fill in start              #Fill in end          
    try:
        message = connectionSocket.recv(1024).decode()   #Fill in start          #Fill in end               
        filename = message.split()[1]                 
        f = open(filename[1:])                        
        outputdata = f.read() #Fill in start       #Fill in end                   

        #Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\nContent-Type:text/html/\r\n\r\n'.encode())
        
        #Fill in start
        #Fill in end                
        
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            	connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        
        #Fill in start        
        connectionSocket.send('HTTP/1.1 404 Not Found\r\nContent-Type:text/html\r\n\r\n'.encode())
        connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>'.encode())
        
        #Fill in end
        #Close client socket
        connectionSocket.close()
        
        #Fill in start
        #Fill in end 
                   
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data                                    
