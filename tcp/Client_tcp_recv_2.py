from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtNetwork import QTcpServer, QTcpSocket
from PySide6.QtCore import QHostAddress


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TCP Server Receiver")
        self.setGeometry(300, 300, 600, 400)

        # Text area to display incoming messages
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)

        # TCP server setup
        self.tcp_server = QTcpServer(self)
        self.tcp_server.newConnection.connect(self.handle_new_connection)

        # Port to listen on
        self.listen_port = 12345

        # Bind to all interfaces (0.0.0.0)
        # Or
        # self.tcp_server.listen(QHostAddress("YOUR.IP.ADDRESS.HERE"), your_port)
        if self.tcp_server.listen(QHostAddress.Any, self.listen_port):
            self.text_edit.append(f"TCP server listening on port {self.listen_port}")
        else:
            self.text_edit.append("Failed to start TCP server")

    def handle_new_connection(self):
        # Accept the new connection
        client_socket = self.tcp_server.nextPendingConnection()
        client_socket.readyRead.connect(lambda: self.read_data(client_socket))
        client_socket.disconnected.connect(lambda: self.handle_disconnection(client_socket))

        client_address = client_socket.peerAddress().toString()
        client_port = client_socket.peerPort()
        self.text_edit.append(f"New connection from {client_address}:{client_port}")

    def read_data(self, socket: QTcpSocket):
        while socket.bytesAvailable():
            data = socket.readAll().data().decode("utf-8")
            self.text_edit.append(f"Received: {data}")
            # Optionally send a response back
            socket.write("✔ Acknowledged\n".encode('utf-8'))

    def handle_disconnection(self, socket: QTcpSocket):
        client_address = socket.peerAddress().toString()
        client_port = socket.peerPort()
        self.text_edit.append(f"Disconnected from {client_address}:{client_port}")
        socket.deleteLater()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
