"""
Name: Jake Hathaway
Date: 7/30/2022
Description: This is a chat server program that sends and receives
text to and from the client program.
References:
-> https://realpython.com/python-sockets/
-> https://docs.python.org/3/tutorial/errors.html#exceptions
"""

from socket import (socket, AF_INET, SOCK_STREAM,
                    gethostbyname, gethostname)


# Create a Client class with methods to handle communications
class ChatServer:
    """The server chat object handles communication with the chat client."""

    # class variables
    BUFFER_SIZE = 1024

    def __init__(self):
        self._server_port = None
        self._client_port = None
        self._ip_address = gethostbyname(gethostname())
        self._socket = None
        self._client_addr = None
        self._connection = None
        self._user_name = ""
        self._friends_name = ""

    def introduce(self) -> None:
        print("**********************************************")
        print("*               Welcome to Chat              *")
        print("**********************************************\n")
        self._user_name = input("-> What is your name? ")
        self._friends_name = input(
            "-> What is the name of the " + "person you wish to chat with? ")

    def get_client_port(self) -> None:

        response = input(
            f"-> Would you like to use {self._friends_name}'s" +
            " default port? ").lower()
        default = response == "y" or response == "yes"
        if(default):
            self._client_port = 6000
        else:
            while (self._client_port is None):
                port = input(
                    f"-> Please enter {self._friends_name}'s" +
                    " port (5000 - 8000): ")
                valid = (port.isnumeric() and int(port) >= 5000
                         and int(port) <= 8000)
                valid = valid and (
                    self._ip_address != self._client_addr or
                    self._server_port != int(port))
                if (valid):
                    self._client_port = int(port)
                else:
                    print(
                        f"\n-X {self._friends_name} is not available on " +
                        f"port {port}. Please try again.\n")

    def get_server_port(self) -> None:
        while (self._server_port is None):
            response = input(
                "-> Would you like to use your default port? ").lower()
            default = response == "y" or response == "yes"
            if (default):
                self._server_port = 5000
            else:
                port = input("-> Enter your port (5000 - 8000): ")
                # Check for validity
                valid = (port.isnumeric() and int(port) >= 5000
                         and int(port) <= 8000)

                if (valid):
                    self._server_port = int(port)
                else:
                    print(f"\n-X {port} is not valid. Please try again.\n")

    def get_client_ip_address(self) -> None:
        self._client_addr = input(
            f"-> Please enter {self._friends_name}'s IP Address: ")

    def get_user_message(self) -> str:
        """This method gets the text from the user."""
        message = input(
            f"-> {self._user_name} ({self._ip_address}:" +
            f"{self._server_port}): ")
        return message

    def connect_to_client(self) -> None:
        """Connects to the client"""

        while (self._socket is None):
            try:
                server_socket = socket(AF_INET, SOCK_STREAM)
                server_socket.bind(('', self._server_port))
                print(f"-> Waiting for {self._friends_name}" +
                      " to connect...")
                server_socket.listen()
                (self._socket, (address,
                                port)) = server_socket.accept()
                if (address != self._client_addr or
                        int(port) != self._client_port):
                    server_socket.close()
                    self._socket = None

            except Exception:
                print(f"-X Had trouble connecting to {self._friends_name}.")
                print("-X Terminating application...")
                quit()

    def send_message(self, message: str) -> None:
        """Sends the message to the client."""
        try:
            self._socket.sendall(str.encode(message))
        except Exception as err:
            print(f"Bad stuff happened: {err}")

    def receive_message(self) -> None:
        """Waits until the server sends a response."""

        try:
            response = self._socket.recv(self.BUFFER_SIZE)
            while (response is None):
                response = self._socket.recv(self.BUFFER_SIZE)
            response = bytes.decode(response)
            if (self.should_quit(response)):
                print(f"-> {self._friends_name} closed the connection...")
                self._socket.close()
                quit()
            print(f"\n{self._friends_name} ({self._client_addr}:" +
                  f"{self._client_port}): {response}")
        except Exception:
            print("Error")

    def close_chat(self) -> None:
        """Closes the socket connection and quits."""
        print(f"\n-> Disconnecting from {self._friends_name}...")
        try:
            self.send_message("/q")
            self._socket.close()
            print("-> Thanks for chatting! Come back soon!")
        except Exception:
            print("Bad stuff happened...")

    def should_quit(self, message: str) -> bool:
        """This method checks for a '/q' message before sending."""
        return message == "/q"

    def provide_instructions(self) -> None:
        """Provide basic instructions to user."""

        print("\n-> Chart started!")
        print("-> If you would like to close the chat,",
              "type '/q' on its own line and press enter.")


def main() -> None:
    """"Main method to start server chat services."""

    server = ChatServer()
    server.introduce()
    server.get_server_port()
    server.get_client_ip_address()
    server.get_client_port()
    server.connect_to_client()
    server.provide_instructions()

    try:
        while True:
            server.receive_message()
            message = server.get_user_message()
            if (server.should_quit(message)):
                server.close_chat()
                break
            else:
                server.send_message(message)
    except KeyboardInterrupt:
        server.close_chat()


if __name__ == ("__main__"):
    main()
