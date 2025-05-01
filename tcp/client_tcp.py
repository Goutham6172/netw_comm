from PySide6.QtCore import Signal, QObject
from PySide6.QtNetwork import QTcpServer, QTcpSocket
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit

class client_tcp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TCP Receiver")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.server = QTcpServer(self)
        self.server.newConnection.connect(self.on_new_connection)

        if not self.server.listen(port=12345):
            print("Failed to start the TCP server")
        else:
            print("TCP Server listening on port 12345")

    def on_new_connection(self):
        client_socket = self.server.nextPendingConnection()
        client_socket.readyRead.connect(lambda: self.read_data(client_socket))
        print("New client connected")

    def read_data(self, socket):
        data = socket.readAll().data().decode('utf-8')
        self.text_edit.append(f"Received from client: {data}")
        socket.write("Acknowledged".encode('utf-8'))

if __name__ == "__main__":
    app = QApplication([])
    window = client_tcp()
    window.show()
    app.exec()
