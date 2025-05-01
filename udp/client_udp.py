from PySide6.QtCore import QHostAddress
from PySide6.QtNetwork import QUdpSocket
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit

class Client_udp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UDP Receiver")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.udp_socket = QUdpSocket(self)
        self.udp_socket.bind(QHostAddress.Any, 12345)

        self.udp_socket.readyRead.connect(self.read_data)

        print("UDP Receiver listening on port 12345")

    def read_data(self):
        while self.udp_socket.hasPendingDatagrams():
            data, host, port = self.udp_socket.readDatagram(self.udp_socket.pendingDatagramSize())
            data = data.decode('utf-8')
            self.text_edit.append(f"Received from {host}:{port}: {data}")
            self.udp_socket.writeDatagram("Acknowledged".encode('utf-8'), host, port)

if __name__ == "__main__":
    app = QApplication([])
    window = Client_udp()
    window.show()
    app.exec()
