from PySide6.QtCore import Signal, QObject, QHostAddress
from PySide6.QtNetwork import QTcpServer, QTcpSocket
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit

class Client_tcp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TCP Receiver")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.socket = QTcpSocket(self)
        self.socket.readyRead.connect(self.read_data)
        self.socket.connected.connect(lambda: self.text_edit.append("Connected"))
        self.socket.errorOccurred.connect(lambda err: self.text_edit.append(f" Error: {self.socket.errorString()}"))

        self.socket.connectToHost(QHostAddress("192.168.2.2") ,12345)

        ## if not self.server.listen(QHostAddress("192.168.2.2") ,12345):
        ##    print("Failed to start the TCP server")
        ## else:
        ##    port = self.server.serverPort();
        ##    print(f"TCP Server listening on port {port}")

    ## def on_new_connection(self):
     ##   client_socket = self.server.nextPendingConnection()
     ##   client_socket.readyRead.connect(lambda: self.read_data(client_socket))
     ##   print("New client connected from "+client_socket.peerAddress().toString() +
     ##   " at port "+client_socket.peerPort())

    def read_data(self):
        data = self.socket.readAll().data().decode('utf-8')
        self.text_edit.append(f"Received from client: {data}")
        ##socket.write("Acknowledged".encode('utf-8'))

if __name__ == "__main__":
    app = QApplication([])
    window = Client_tcp()
    window.show()
    app.exec()
