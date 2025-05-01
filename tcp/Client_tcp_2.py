# This Python file uses the following encoding: utf-8


import sys
from PySide6.QtCore import QByteArray, QIODevice, QObject, Signal, Slot
from PySide6.QtNetwork import QTcpSocket
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Client_tcp_2(QObject):
    message_received = Signal(str)
    status_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.socket = QTcpSocket(self)
        self.socket.readyRead.connect(self.receive_message)
        self.socket.connected.connect(self.connected)
        self.socket.disconnected.connect(self.disconnected)
        self.socket.errorOccurred.connect(self.socket_error)
        self.status_changed.emit("Disconnected")

    def connect_to_host(self, host, port):
        self.socket.connectToHost(host, int(port))
        self.status_changed.emit(f"Connecting to {host}:{port}...")

    def disconnect_from_host(self):
        self.socket.disconnectFromHost()

    def send_message(self, message):
        if self.socket.state() == QTcpSocket.ConnectedState:
            data = QByteArray(message.encode('utf-8'))
            self.socket.write(data)
            self.status_changed.emit(f"Sent: {message}")
        else:
            self.status_changed.emit("Not connected. Cannot send message.")

    @Slot()
    def receive_message(self):
        while self.socket.canReadLine():
            message = self.socket.readLine().trimmed().toText()
            self.message_received.emit(message)
            self.status_changed.emit(f"Received: {message}")

    @Slot()
    def connected(self):
        self.status_changed.emit("Connected")

    @Slot()
    def disconnected(self):
        self.status_changed.emit("Disconnected")

    @Slot()
    def socket_error(self, error):
        self.status_changed.emit(f"Error: {error.name}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.client = Client_tcp_2()
        self.client.message_received.connect(self.update_received_text)
        self.client.status_changed.connect(self.update_status_text)

        self.host_input = QLineEdit("127.0.0.1")
        self.port_input = QLineEdit("12345")
        self.connect_button = QPushButton("Connect")
        self.disconnect_button = QPushButton("Disconnect")
        self.message_input = QLineEdit()
        self.send_button = QPushButton("Send")
        self.received_text = QTextEdit()
        self.received_text.setReadOnly(True)
        self.status_text = QLineEdit()
        self.status_text.setReadOnly(True)

        self.connect_button.clicked.connect(self.connect_to_server)
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        self.send_button.clicked.connect(self.send_message)

        hbox = QVBoxLayout()
        hbox.addWidget(self.status_text)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.host_input)
        input_layout.addWidget(self.port_input)

        connection_layout = QVBoxLayout()
        connection_layout.addWidget(self.connect_button)
        connection_layout.addWidget(self.disconnect_button)

        message_layout = QVBoxLayout()
        message_layout.addWidget(self.message_input)
        message_layout.addWidget(self.send_button)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(connection_layout)
        main_layout.addLayout(message_layout)
        main_layout.addWidget(self.received_text)
        main_layout.addLayout(hbox)

        self.setWindowTitle("TCP Client")

    @Slot()
    def connect_to_server(self):
        host = self.host_input.text()
        port = self.port_input.text()
        self.client.connect_to_host(host, port)

    @Slot()
    def disconnect_from_server(self):
        self.client.disconnect_from_host()

    @Slot()
    def send_message(self):
        message = self.message_input.text()
        self.client.send_message(message)
        self.message_input.clear()

    @Slot(str)
    def update_received_text(self, message):
        self.received_text.append(message)

    @Slot(str)
    def update_status_text(self, status):
        self.status_text.setText(status)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
