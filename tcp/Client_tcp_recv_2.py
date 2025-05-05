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
            """
            What Does listen(QHostAddress, port) Do?

            The listen() function tells the TCP server to:

            Start listening for incoming TCP connections
            On a specific IP address (interface)
            And a specific port

            self.tcp_server.listen(QHostAddress("192.168.1.100"), 5000)

            This line tells Qt:
            “Bind this server to the network interface that has IP 192.168.1.100, and wait for TCP clients to connect on port 5000.”

            """
    def handle_new_connection(self):
        # Accept the new connection
        client_socket = self.tcp_server.nextPendingConnection()
        client_socket.readyRead.connect(lambda: self.read_data(client_socket))
        client_socket.disconnected.connect(lambda: self.handle_disconnection(client_socket))

        client_address = client_socket.peerAddress().toString()
        client_port = client_socket.peerPort()
        self.text_edit.append(f"New connection from {client_address}:{client_port}")
        """
        handle_new_connection(self)
        This function is called automatically when a client connects to the TCP server.

        What it does:

        Accepts the incoming connection using nextPendingConnection(), which returns a QTcpSocket representing the client.
        Connects:
        The client's readyRead signal to read_data() → triggered when the client sends data.
        The client's disconnected signal to handle_disconnection() → triggered when the client disconnects.
        Logs the client’s IP address and port.
            client_socket = self.tcp_server.nextPendingConnection()
            client_socket.readyRead.connect(lambda: self.read_data(client_socket))
        This prepares the server to read incoming data from the client whenever available.

        """
    def read_data(self, socket: QTcpSocket):
        while socket.bytesAvailable():
            data = socket.readAll().data().decode("utf-8")
            self.text_edit.append(f"Received: {data}")
            # Optionally send a response back
            socket.write("Acknowledged\n".encode('utf-8'))
            """
            read_data(self, socket: QTcpSocket)
            This function is called when data is available from a connected client.

            What it does:

            Reads all available bytes from the socket using readAll().
            Decodes the raw data into a string (UTF-8).
            Displays the message in the text area (self.text_edit).
            Optionally sends a response ("✔ Acknowledged") back to the client.
            """
    def handle_disconnection(self, socket: QTcpSocket):
        client_address = socket.peerAddress().toString()
        client_port = socket.peerPort()
        self.text_edit.append(f"Disconnected from {client_address}:{client_port}")
        socket.deleteLater()
"""
handle_disconnection(self, socket: QTcpSocket)
This function is called when a connected client disconnects from the server.

What it does:

Retrieves the client’s address and port.
Logs that the client has disconnected.
Frees up the socket using deleteLater() to avoid memory leaks
"""

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


"""

tcp_server.listen(address, port)

 What it does:
Starts the TCP server listening for incoming connections on the specified IP and port.

 Think of it as:
"Open the door and start waiting for people to knock."
 Example: tcp_server.listen(QHostAddress.Any, 12345)
Binds the server to all network interfaces on port 12345
If this fails (e.g., port is in use), the server won't receive any connections
 Without calling listen(), the server won’t work at all.





tcp_server.newConnection.connect(your_slot_function)

 What it does:
Connects the Qt signal newConnection to a function (slot) that will be called whenever a new client connects.

 Think of it as:
"Define what to do when someone knocks on the door."
Example:
    tcp_server.newConnection.connect(self.handle_new_connection)
This tells Qt to call handle_new_connection() every time a new client connects.
Inside that function, you’ll usually call tcp_server.nextPendingConnection() to get the new socket.

Final Analogy
Imagine you're opening a restaurant:

listen() = You unlock the doors and turn on the "Open" sign
newConnection.connect(...) = You tell the staff how to greet customers when they walk in
Both are needed for the restaurant (or server) to function properly.



"""
