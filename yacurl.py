from socket import gethostbyname, socket, AF_INET, SOCK_STREAM
from bs4 import BeautifulSoup
from parser import *
import os

HTTP_HEADER_DELIMITER = b'\r\n\r\n'
CONTENT_LENGTH_FIELD = b'Content-Length:'
HTTP_PORT = 80
ONE_BYTE_LENGTH = 1

def request(host, path, method='GET'):
    
    r =  '{} {} HTTP/1.1\nHost: {}\r\n\r\n'.format(method, path, host)
    request = r.encode()

    return request
    
def response(sock):

    header = bytes() 
    chunk = bytes()

    try:
        while HTTP_HEADER_DELIMITER not in header:
            chunk = sock.recv(ONE_BYTE_LENGTH)
            if not chunk:
                break
            else:
                header += chunk
    except socket.timeout:
        pass

    return header  

def content_length(header):

    for line in header.split(b'\r\n'):
        if CONTENT_LENGTH_FIELD in line:
            return int(line[len(CONTENT_LENGTH_FIELD):])
    return 0

def get_body(sock, length):

    body = bytes()
    data = bytes()

    while True:
        data = sock.recv(length)
        if len(data)<=0:
            break
        else:
            body += data

    return body 

def write_body(name_file, extension, body):

    if not(os.path.exists('Files')): 
        os.mkdir('Files')

    try:
        file = open('Files/{}.{}'.format(name_file, extension), 'w+')
        file.write(body.decode('latin-1'))
        file.close()
    except:
        return 0
    return 1

def parser_b(body):
    parser.feed(body.decode())

def main():
    
    host = input('Ingresa el host: ')
    path = input('Ingresa el Path acuerdate del --> / <--inicial: ')
    port = input('Ingrese el puerto: ')
    name_file = input('Ingrese nombre deseado para el body a descargar(Sin el punto): ')
    extension = input('Ingrese extension que se descargara(no adicione el punto): ')
    aux = 0
    if(extension == 'html'):
        parser = input('Desea parsear el html(1 para si 2 para no): ')
        if(parser == '1' ):
           aux = 1 
        else:
            pass

    print(f'\n# Recibiendo informacion de http://{host}{path}')
    ip_address = gethostbyname(host)
    print(f'> Servidor remoto {host} direccion ip {ip_address}')

    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip_address, int(port)))
    print(f'> Conexion TCP con {ip_address}:{port} establecida')

    http_get_request = request(host, path)
    print('\n# HTTP request ({} bytes)'.format(len(http_get_request)))
    print(http_get_request)     
    sock.sendall(http_get_request)
 
    header = response(sock)
    print(type(header))
    print('\n# HTTP Response cabecera ({} bytes)'.format(len(header)))
    print(header)

    length = content_length(header)
    print('\n# Largo del cuerpo')
    print(f"{length} bytes")

    body = get_body(sock, length)

    if(len(body) > 1):

        print('\n# Cuerpo ({} bytes)'.format(len(body)))
        print(body)

        wfile = write_body(name_file, extension, body)

        if wfile == 1: 
            print('\n# Archivo guardado')
        else: 
            print('\n# Error guardando el archivo') 
        
        if (aux == 1 and wfile ==1):
            parser_b(body)
            
    else:
        print('\n# El archivo no tiene cuerpo ({} bytes)'.format(len(body)))



if __name__ == '__main__':
    main()