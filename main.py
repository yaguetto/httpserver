import socket
import threading

def main():
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50008              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(0)
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        t = threading.Thread(target=handle_connection, args=(conn,))
        t.start()

def handle_connection(conn):
    buffer = b''

    while 1:
        data = conn.recv(4)
        if not data: break
        buffer = buffer + data
        if b'\r\n\r\n' in buffer:
            cabecalhos = buffer.split(b'\r\n')
            cabecalho = cabecalhos[0]
            buffer = b''
            caminho = cabecalho.split(b' ')[1]
            tamanho = 5 + len(caminho)
            tamanho_string = str(tamanho)
            tamanho_bytes = tamanho_string.encode()
            conn.sendall(b'HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nContent-Length: '+tamanho_bytes+b'\r\n\r\nola, '+ caminho)
        #conn.sendall(data)
        #print(buffer)
    conn.close()


if __name__ == "__main__":
    main()