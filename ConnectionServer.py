import socket
import thread
from MysqlConnector import MysqlConnector
from MysqlConnector import parse_data


class ConnectionServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.sqlConnector = None
        thread.start_new_thread(self.initialise_server, ())

    def initialise_server(self):
        self.sqlConnector = MysqlConnector("127.0.0.1", 3306, "root", "1234")
        self.socket.listen(30)
        while True:
            client_socket, address = self.socket.accept()
            thread.start_new_thread(self.connected_thread, (client_socket, ))

    def connected_thread(self, client_socket):
        data = client_socket.recv(1024)
        username = parse_data(data)[0]
        res = self.sqlConnector.check_credentials(data)
        if not res:
            client_socket.send("Invalid username or password~")
            client_socket.close()
            return
        client_socket.send("Login Success~")
        voting_status = self.sqlConnector.check_voting_status()
        if voting_status == 0:
            client_socket.send("Polling not yet started~")
            client_socket.close()
        elif voting_status == 1:
            status = self.sqlConnector.check_voter_status(username)
            if status == 0:
                client_socket.send(self.sqlConnector.get_candidates())
                data = client_socket.recv(1024)
                candidate = parse_data(data)
                self.sqlConnector.save_vote(username, candidate[1])
                client_socket.send("Your Vote Success fully casted~")
                client_socket.close()
            else:
                client_socket.send("you already casted your vote~")
                client_socket.close()
        elif voting_status == 2:
            #print(self.sqlConnector.voting_results())
            results = "Results\n" + self.sqlConnector.voting_results()
            client_socket.send(results)
            client_socket.close()

