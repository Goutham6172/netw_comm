from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtNetwork import QUdpSocket, QHostAddress#, QAbstractSocket
#from PySide6.QtCore import QIODevice


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UDP Broadcast Receiver")
        self.setGeometry(300, 300, 600, 400)

        # Display for received messages
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)

        # Create UDP socket
        self.udp_socket = QUdpSocket(self)

        # Port to listen on for broadcast
        self.listen_port = 12345

        # Bind to any address (to receive broadcast from any interface)
        success = self.udp_socket.bind(
            QHostAddress.AnyIPv4,
            self.listen_port,
            QUdpSocket.ShareAddress | QUdpSocket.ReuseAddressHint
        )

        if success:
            self.text_edit.append(f"Listening for UDP broadcasts on port {self.listen_port}")
            self.udp_socket.readyRead.connect(self.read_udp_data)
        else:
            self.text_edit.append(f"Failed to bind UDP socket to port {self.listen_port}")

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
"""
self.udp_socket.bind(...)

This binds the QUdpSocket to a network interface and port so that it can receive incoming datagrams.

Binding is essential — without it, the socket won’t listen for data.




QHostAddress.AnyIPv4

This tells the socket to bind to all available IPv4 interfaces on the machine (i.e., 0.0.0.0), not just a specific IP like 127.0.0.1.

That includes:

Loopback (localhost)
Ethernet/WiFi IPs
Virtual interfaces
It is necessary for receiving broadcast messages, which may arrive on any interface.





This is the UDP port number you're binding to. It must match the port that the sender (server or broadcaster) is using.




QUdpSocket.ShareAddress | QUdpSocket.ReuseAddressHint

These are socket options combined using the | (bitwise OR) operator.

Let’s explain them:

    QUdpSocket.ShareAddress
    Purpose: Allows multiple sockets on the same machine to bind to the same address and port simultaneously.
    This is necessary in broadcast/multicast situations because:

    You might have more than one process or application listening to the same UDP stream.
    Some OSes require this option to receive broadcast packets properly.


    QUdpSocket.ReuseAddressHint
    Purpose: Provides a hint to the operating system to reuse the port even if it’s in use or recently closed.
    Without this, binding may fail with "address already in use" errors.
    This is especially useful in development or when restarting your application frequently.




"""
