"""
Name: Jake Hathaway
Date: 7/30/2022
Description: This is a chat client program that sends and receives
text to and from the server program.
References:
-> https://realpython.com/python-sockets/
-> https://docs.python.org/3/tutorial/errors.html#exceptions
"""

from socket import socket, AF_INET, SOCK_STREAM, gethostname, gethostbyname


# Create a Client class with methods to handle communications
class ChatClient:
    """The chat client object handles communication with the chat server."""

    # class variables
    BUFFER_SIZE = 1024

    def __init__(self):
        self._client_port = None
        self._server_port = None
        self._ip_address = gethostbyname(gethostname())
        self._server_ip_address = None
        self._socket = None
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
        while (self._client_port is None):
            response = input(
                "-> Would you like to use your default port? ").lower()
            default = response == "y" or response == "yes"
            if (default):
                self._client_port = 6000
            else:
                port = input("-> Enter your port (5000 - 8000): ")
                # Check for validity
                valid = (port.isnumeric() and int(port) >= 5000
                         and int(port) <= 8000)

                if (valid):
                    self._client_port = int(port)
                else:
                    print(f"\n-X {port} is not valid. Please try again.\n")

    def get_server_ip_address(self) -> None:
        response = input(
            f"-> Please enter {self._friends_name}'s IP Address: ")
        if (response.lower() == "localhost"):
            self._server_ip_address = gethostbyname(gethostname())
        else:
            self._server_ip_address = response

    def get_server_port(self) -> None:

        response = input(
            f"-> Would you like to use {self._friends_name}'s" +
            " default port? ").lower()
        default = response == "y" or response == "yes"
        if(default):
            self._server_port = 5000
        else:
            while (self._server_port is None):
                port = input(
                    f"-> Please enter {self._friends_name}'s" +
                    " port (5000 - 8000): ")
                valid = (port.isnumeric() and int(port) >= 5000
                         and int(port) <= 8000)
                valid = valid and (
                    self._ip_address != self._server_ip_address or
                    self._client_port != int(port))
                if (valid):
                    self._server_port = int(port)
                else:
                    print(
                        f"\n-X {self._friends_name} is not available on " +
                        f"port {port}. Please try again.\n")

    def get_user_message(self) -> str:
        """This method gets the text from the user."""
        message = input(
            f"\n-> {self._user_name} ({self._ip_address}:" +
            f"{self._client_port}): ")
        return message

    def connect_to_server(self) -> None:
        """Connects to the server and retains the socket for future use."""
        client_socket = socket(AF_INET, SOCK_STREAM)
        try:
            client_socket.bind((self._ip_address, self._client_port))
            client_socket.connect((self._server_ip_address, self._server_port))
            self._socket = client_socket
        except ConnectionRefusedError:
            print("-X Server not available...")
            quit()
        except Exception:
            print("-X Client port already in use, terminating.")
            quit()

    def send_message(self, message: str) -> None:
        """Sends the message to the server."""
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
            print(f"{self._friends_name} ({self._server_ip_address}:" +
                  f"{self._server_port}): {response}")
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

        print("\n-> Chat started!")
        print("-> If you would like to close the chat,",
              "type '/q' on its own line and press enter.")


def main() -> None:
    """"Main method to start client chat services."""

    client = ChatClient()
    client.introduce()
    client.get_client_port()
    client.get_server_ip_address()
    client.get_server_port()
    client.connect_to_server()
    client.provide_instructions()

    try:
        while True:
            message = client.get_user_message()
            if (client.should_quit(message)):
                client.close_chat()
                break
            else:
                client.send_message(message)
            client.receive_message()
    except KeyboardInterrupt:
        client.close_chat()


if __name__ == ("__main__"):
    main()
