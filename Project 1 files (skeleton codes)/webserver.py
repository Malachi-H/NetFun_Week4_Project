# import socket module
from socket import *  # type: ignore

# Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# AF_INET = Address_Family_Internet. It says the socket should use an IPv4 Address (eg. 100.50.200.5) or a Hostname (eg. google.com)
# SOCK_STREAM says the socket should use TCP instead of UDP (SOCK_DGRAM)

serverPort = 8080
# port number is used to announce the type of connection. eg. SMTP uses port 25.
# port 80 is the protocol for HTTP, but it often blocked by ISP's or web-browsers, so 8080 or 8008 are used instead.

serverSocket.bind(("", serverPort))
# tells the socket to listen to "serverPort" and receive packets from all interfaces (what is an interface? IDK)
# "" is a special form that is interpreted by the socket module as "INADDR_ANY" (In_Address_Any). This is used to keep the isolation between application and network layers (I think). So The program doesn't care what network interface is being used to send an receive, as long as it's a TCP connection coming through the "serverPort" port.
serverSocket.listen(1)  
# tells the server to start listening for connection requests.
# the "1" is the length of the queue (0 indexed so length is 2 connections). If a second person tries to connect to the server (load the webpage) while the first person's request is still being processed, they will be put in the queue and processed after the first person's webpage is loaded. 

while True:
    # Establish the connection
    print("Ready to serve...")
    connectionSocket, addr = serverSocket.accept()
    # connectionSocket = <socket.socket. fd=728, family=2, type=1, proto=0, laddr=('127.0.0.1', 8080), raddr=('127.0.0.1', 51284)>, 
        # class instance of Socket that allows communication with the specific client. 
        # create a new instance instead of binding the "serverSocket" to the specific client, because "serverSocket" still needs to listen for other clients.
    # addr = ('127.0.0.1', 51284)
        # addr is a return address and port number of the client that connected to the server. It isn't used because this information is already stored int he returned socket class instance "connectionSocket"
    try:
        message = connectionSocket.recv(
            1024  #! Why 1024? IDK
        ).decode()  #! What is it decoding from Binary? IDK
        # message looks something like the following:
        """
        GET /simpleWeb.html HTTP/1.1
        Host: localhost:8081
        Connection: keep-alive
        Cache-Control: max-age=0
        sec-ch-ua: "Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"
        sec-ch-ua-mobile: ?0
        sec-ch-ua-platform: "Windows"
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
        Sec-Fetch-Site: none
        Sec-Fetch-Mode: navigate
        Sec-Fetch-User: ?1
        Sec-Fetch-Dest: document
        Accept-Encoding: gzip, deflate, br, zstd
        Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
        """
        filename = message.split()[1]
        # calling split and getting the second element gets the file name (url path) that the client is requesting.
        # in this case it's "/simpleweb.html"
        f = open(filename[1:])
        # open's the file (removes the slash) (using open with would have been better I think)
        outputdata = f.read()
        # reads the locally stored simpleweb.html file. It was part of the skeleton code

        # Send one HTTP header line into socket
        connectionSocket.send(
            "HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n".encode()  #! What does the 1.1 here mean? We learn it in class but I've forgotten. (THIS IS A LIKELY QUESTION) IDK
        )

        # Send the content of the requested file to the client
        #! Why is it encoding and sending the characters 1 by 1 instead of encoding them all and sending them all in one "send"? IDK
        for i in range(0, len(outputdata)):  # the 0 here is unneeded.
            connectionSocket.send(
                outputdata[i].encode()
            )  # * Seems to send character by character, encoded using utf-8. (I think the encoding means new lines are converted to \n ect. but IDK)
        connectionSocket.send(
            "\r\n".encode()
        )  #! What does \r mean and why is \r\n used? Does it indicate the end of a chunk of data? It was used earlier when sending the heading, but repeated twice. WHy is that? IDK
        connectionSocket.close()  #! can connectionSocket be managed using a context manager like: `with open("filename", "r") as file`
    except IOError:
        # Send response message for file not found

        connectionSocket.send(
            "HTTP/1.1 404 Not Found\r\nContent-Type:text/html\r\n\r\n".encode()
        )
        connectionSocket.send(
            "<html><head></head><body><h1>404 Not Found</h1></body></html>".encode()
        )

        connectionSocket.close()

#! Why have this if it's outside of the while true loop? It'll never run. IDK
serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
