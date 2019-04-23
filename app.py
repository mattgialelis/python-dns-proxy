import socket
import ssl
import threading

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 53
DNS = '1.1.1.1'


def sendquery(tls_conn_sock, dns_query):
    tcp_query = dns_query
    tls_conn_sock.send(tcp_query)
    result = tls_conn_sock.recv(1024)
    return result


def tcpconnection(DNS):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')

    wrappedSocket = context.wrap_socket(sock, server_hostname=DNS)
    wrappedSocket.connect((DNS, 853))

    # print(wrappedSocket.getpeercert())
    return wrappedSocket


def requesthandle(data, address, DNS):
    tls_conn_sock = tcpconnection(DNS)
    tcp_result = sendquery(tls_conn_sock, data)
    if tcp_result:
        return tcp_result
    else:
        print("not a dns query")


def connection(conn, addr):
    while True:
        data = conn.recv(1024)
        if data:
            conn.sendall(requesthandle(data, addr, DNS))
            break
    conn.close()


def main(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=connection, args=(conn, addr)).start()


if __name__ == "__main__":
    main(HOST, PORT)