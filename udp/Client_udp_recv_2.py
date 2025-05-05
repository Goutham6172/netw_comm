from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtNetwork import QUdpSocket, QHostAddress
#from PySide6.QtCore import QIODevice


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qt for Python - UDP Receiver")
        self.setGeometry(300, 300, 600, 400)

        # Display area for messages
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)

        # UDP receiver setup
        self.udp_socket = QUdpSocket(self)

        # IP and port to listen on
        self.listen_ip = "127.0.0.1"
        self.listen_port = 12345
        #It listens on 127.0.0.1:12345

        # Attempt to bind
        success = self.udp_socket.bind(QHostAddress(self.listen_ip), self.listen_port)
        if success:
            self.text_edit.append(f"Listening for UDP on {self.listen_ip}:{self.listen_port}")
            self.udp_socket.readyRead.connect(self.read_udp_data)
        else:
            self.text_edit.append(f"Failed to bind to {self.listen_ip}:{self.listen_port}")

    def read_udp_data(self):
        while self.udp_socket.hasPendingDatagrams():
            datagram, sender, sender_port = self.udp_socket.readDatagram(self.udp_socket.pendingDatagramSize())
            message = datagram.data().decode('utf-8')
            self.text_edit.append(f"From {sender.toString()}:{sender_port} → {message}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
