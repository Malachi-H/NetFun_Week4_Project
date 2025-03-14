# import socket module
from socket import * # type: ignore

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket

# Fill in start
serverPort = 8080 # Does the port number here matter as long as we are have the same number in our localhost url (http://localhost:8080)? IDK
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
# Fill in end

while True:
    # Establish the connection
    print("Ready to serve...")
    connectionSocket, addr = (
        serverSocket.accept()
    )  # Fill in start              #Fill in end
    try:
        # What URL do we use to ge to the html file? (http://localhost:8080/simpleWeb.html doesn't work) IDK
        message = connectionSocket.recv(
            1024 # Why 1024? IDK
        ).decode() # What is it decoding from Binary? IDK
        # message looks something like the following:
        '''
        GET /simpleweb.html HTTP/1.1​
        Host: localhost:6789​
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0​
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8​
        Accept-Language: en-US,en;q=0.5​
        Accept-Encoding: gzip, deflate, br​
        DNT: 1​
        Connection: keep-alive​
        Upgrade-Insecure-Requests: 1​
        Sec-Fetch-Dest: document​
        Sec-Fetch-Mode: navigate​
        Sec-Fetch-Site: none​
        Sec-Fetch-User: ?1​ 
        '''
        filename = message.split()[1]
        # calling split and getting the second element gets the file name (url path) that the client is requesting.
        # in this case it's "/simpleweb.html"
        f = open(filename[1:])
        # open's the file (removes the slash) (using open with would have been better I think)
        outputdata = f.read()
        # reads the locally stored simpleweb.html file. It was part of the skeleton code

        # Send one HTTP header line into socket
        connectionSocket.send(
            "HTTP/1.1 200 OK\r\nContent-Type:text/html/\r\n\r\n".encode()
        )

        # Fill in start
        # Fill in end

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found

        # Fill in start
        connectionSocket.send(
            "HTTP/1.1 404 Not Found\r\nContent-Type:text/html\r\n\r\n".encode()
        )
        connectionSocket.send(
            "<html><head></head><body><h1>404 Not Found</h1></body></html>".encode()
        )

        # Fill in end
        # Close client socket
        connectionSocket.close()

        # Fill in start
        # Fill in end

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
