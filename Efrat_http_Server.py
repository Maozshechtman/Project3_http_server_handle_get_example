# http Server
# efrat segal

import os
import socket

IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 0.5
PREFIX_URL = './webroot/'
DEFAULT_URL = 'index.html'
REDIRECTION_DICTIONARY = {'index.html': 'index2.html'}
FORBIDDEN_LIST = [""]


def get_file_data(filename):
    """ Get data from file """
    try:
        file = ''
        with open(filename, 'rb') as my_file:
            file = my_file.read()
        return file
    except Exception as e:
        return "The error is " + str(e)


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    data = b''
    if resource == '/':
        url = DEFAULT_URL
    else:
        url = resource
    http_header = b'HTTP/1.1 '
    filename = PREFIX_URL + url
    while True:
        # check if URL had been redirected, not available or other error code.
        if url in REDIRECTION_DICTIONARY:
            http_header += b'302'
            loc = REDIRECTION_DICTIONARY[url]
            http_header += b'Location: ' + loc.encode() + b'\r\n'
            break
        elif url in FORBIDDEN_LIST:
            http_header += b' 403 Forbidden'
            data += b' 403 Forbidden'
        elif not os.path.isfile(filename):
            http_header += b' 404 Not Found'
            data += b' 404 Not Found'
            break
        else:
            http_header += b'200 OK\r\n'
            data += get_file_data(filename)
            file_type = filename[filename.rfind('.') + 1:]
            print("I send file{}".format(filename))
            if file_type == 'html':
                http_header += b'Content-Type: text/html; charset=utf-8\r\n'  # HTTP header
            elif file_type == 'jpg':
                http_header += b'Content-Type: image/jpeg\r\n'  # jpg header
            elif file_type == 'js':
                http_header += b'Content-Type: text/javascript; charset=UTF-8\r\n'  # js header
            elif file_type == 'css':
                http_header += b'Content-Type: text/css\r\n'  # css header
            elif file_type == 'gif':
                http_header += b'Content-Type: image/gif\r\n'  # gif header
            elif file_type == 'ico':
                http_header += b'Content-Type: image/vnd.microsoft.icon\r\n'  # ico header
            break
    http_header += b'\r\n'
    http_response = http_header + data
    client_socket.send(http_response)


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    client_request = request.split()
    if client_request[0] == 'GET' and client_request[2] == 'HTTP/1.1':
        return True, client_request[1]
    return False, None


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')

    while True:
        try:
            client_request = client_socket.recv(1024).decode()
            valid_http, resource = validate_http_request(client_request)
            if valid_http:
                print('Got a valid HTTP request')
                handle_client_request(resource, client_socket)
                break
            else:
                print('Error: Not a valid HTTP request')
                http_header = b'HTTP/1.1 500 Internal Server Error\r\n\r\n'  # The server received a request he did not understand
                client_socket.send(http_header)
                break
        except Exception:
            print(Exception.__cause__)
            break
    print('Closing connection')
    client_socket.close()




def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port", PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()