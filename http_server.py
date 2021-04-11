# Ex 4.4 - HTTP Server Shell
# Author: Maoz Shechtman .
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os

IP = "0.0.0.0"
PORT = 80
# Location of the files in the server computer
WEB_ROOT_LOCATION = r'C:\Networks\work\Project3_http_server\webroot{}'
# region forbidden list and redirection dictionary for 403 and 302 codes
REDIRECTION_DICTIONARY = {'\index1.html': 'index2.html'}
FORBIDDEN_LIST = [""]
# endregion
SOCKET_TIMEOUT = 0.1
HTTP_VERSION = "HTTP/1.1 "
DEFAULT_URL = '\index.html'
# Built in filed of Content
CONTENT_LENGTH_FILED = 'Content-Length: {}\r\n'
# region Status Codes
CODE_OK = '200 OK\r\n'
CODE_NOT_FOUND = '404 NOT Found\r\n\r\n'
CODE_Temporarily_Moved = "302 Found\r\nLocation: {}\r\n\r\n"
CODE_FORBIDDEN = '403 Forbidden\r\n\r\n'
CODE_INTERNAL_SERVER_ERROR = "500 Error Server Internal\r\n\r\n"


# endregion

def get_file_data(filename):
    """ Get data from file """
    try:
        lines = ''
        with open(filename, 'rb') as my_file:
            lines = my_file.read()

        return lines


    except Exception:
        print("Fail to Get the data from:{}".format(filename))


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == '':
        url = DEFAULT_URL
    else:
        url = resource

    # TO DO: check if URL had been redirected, not available or other error code. For example:

    if url in REDIRECTION_DICTIONARY.keys():
        # TO DO: send 302 redirection response
        http_response = HTTP_VERSION + CODE_Temporarily_Moved.format(REDIRECTION_DICTIONARY[url])
        client_socket.send(http_response.encode())
    elif url in FORBIDDEN_LIST:
        http_response = HTTP_VERSION + CODE_FORBIDDEN
        client_socket.send(http_response.encode())
    elif not os.path.isfile(WEB_ROOT_LOCATION.format(url)):
        http_response = HTTP_VERSION + CODE_NOT_FOUND
        client_socket.send(http_response.encode())
    else:
        file_size = os.stat(WEB_ROOT_LOCATION.format(url)).st_size
        content_length = CONTENT_LENGTH_FILED.format(file_size)
        filetype = url[url.rfind('.') + 1::]
        prefix = HTTP_VERSION + CODE_OK + content_length
        if filetype == 'html' or filetype == 'txt':
            http_header = prefix + 'Content-Type: text/html; charset=utf-8\r\n\r\n'
        elif filetype == 'jpg':
            http_header = prefix + 'Content-Type: image/jpeg\r\n\r\n'
        elif filetype == 'js':
            http_header = prefix + 'Content-Type: text/javascript; charset=UTF-8\r\n\r\n'
        elif filetype == 'css':
            http_header = prefix + 'Content-Type: text/css\r\n\r\n'
        elif filetype == 'ico':
            http_header = prefix + 'Content-Type: image/vnd.microsoft.icon\r\n\r\n'
        elif filetype == 'gif':
            http_header = prefix + 'Content-Type: image/gif\r\n\r\n'
        filename = WEB_ROOT_LOCATION.format(url)
        # The Data from the file is not need to coded
        data = get_file_data(filename)
        print("I send file{}".format(filename))
        http_header = http_header.encode()
        http_response = http_header + data
        client_socket.send(http_response)


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    # First we will get the client request from all the data
    split_request = request.split("\n")[0].split(" ")
    if split_request[1] == '/':
        return True, ''
    split_request[1] = split_request[1].replace('/', "\\")
    if split_request[0] == 'GET' and split_request[2] == "HTTP/1.1\r":
        return True, split_request[1]
    else:
        return False, 'ERROR'


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        # TO DO: insert code that receives client request
        try:
            client_request = client_socket.recv(1024).decode()
            valid_http, resource = validate_http_request(client_request)
            if valid_http:
                print('Got a valid HTTP request')
                handle_client_request(resource, client_socket)
                break
            else:
                print('Error: Not a valid HTTP request')
                http_response = HTTP_VERSION + CODE_INTERNAL_SERVER_ERROR
                client_socket.send(http_response.encode())
                break
        except Exception:
            break

    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
