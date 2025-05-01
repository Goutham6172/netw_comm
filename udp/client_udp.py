from PySide6.QtCore import QHostAddress
from PySide6.QtNetwork import QUdpSocket
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit

class Client_udp_recv(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UDP Receiver")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.udp_socket = QUdpSocket(self)
        #self.udp_socket.readyRead.connect(self.read_data)

        if self.udp_socket.bind(QHostAddress("192.168.10.10"), 12345):
            self.text_edit.append(f"Listening for UDP on {self.server_ip}:{self.server_port}")
            self.udp_socket.readyRead.connect(self.read_data)
        else:
            self.text_edit.append("Connection failed")


    def read_data(self):
        while self.udp_socket.hasPendingDatagrams():
            data, host, port = self.udp_socket.readDatagram(self.udp_socket.pendingDatagramSize())
            data = data.decode('utf-8')
            self.text_edit.append(f"Received from {host}:{port}: {data}")
            #self.udp_socket.writeDatagram("Acknowledged".encode('utf-8'), host, port)

if __name__ == "__main__":
    app = QApplication([])
    window = Client_udp_recv()
    window.show()
    app.exec()
