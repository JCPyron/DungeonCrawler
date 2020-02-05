import paramiko
import json
import struct


class Interact:
    # Logon Info
    hostname = ''
    username = ''
    key = ''
    stdin = ''
    stdout = ''
    stderr = ''
    client = ''

    # init connection and get file descriptors
    def __init__(self, hostname, username, key_path):
        self.hostname = hostname
        self.username = username
        self.key = paramiko.RSAKey.from_private_key_file(key_path)
        # connect to the server
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.hostname, port=22, username=self.username, pkey=self.key)
        self.stdin, self.stdout, self.stderr = self.client.exec_command("~/startServer")

    # runs on exit, closes connection
    def __exit__(self, exc_type, exc_value, traceback):
        self.stdin.close()
        self.stdout.close()
        self.stderr.close()
        self.client.close()

    # sends the given json command and returns the result
    def send_command(self, send_str):
        send_data = json.dumps(send_str).encode('utf_8')
        print(send_data)
        self.stdin.write(send_data)
        return self.read_out()

    # a debug method, sends the command and returns from stderr
    def send_command_read_err(self, send_str):
        send_data = json.dumps(send_str).encode('utf_8')
        self.stdin.write(send_data)
        return self.read_err()

    # reads from stdout
    # reads one character at a time because the server ends response with null character, not EOF
    def read_out(self):
        out_str = ""
        read_char = self.stdout.read(1)
        while read_char != b'\x00':
            out_str += str(read_char.decode("utf-8"))
            read_char = self.stdout.read(1)
        return json.loads(out_str)

    # read from stderr
    # reads one character at a time because the server ends response with null character, not EOF
    def read_err(self):
        out_str = ""
        read_char = self.stderr.read(1)
        while read_char != b'\x00':
            out_str += str(read_char.decode("utf-8"))
            read_char = self.stderr.read(1)
        return json.loads(out_str)

    # authenticate with the server
    def auth(self, username, password, email):
        auth_str = {"auth": {"username": username, "password": password, "email": "NULL"}}
        server_response = self.send_command(auth_str)
        if server_response["auth"]["return"] == 3:
            return True
        # if the user was not found, registers the user
        elif server_response["auth"]["return"] == 1:
            self.stdin, self.stdout, self.stderr = self.client.exec_command("~/startServer")
            return self.register(username, password, email)
        return False

    # registers the user with the server
    def register(self, username, password, email):
        reg_str = {"register": {"username": username, "password": password, "email": email}}
        server_response = self.send_command(reg_str)
        if server_response["register"]["return"] == 3:
            return True
        return False

    # returns the options struct, can can be changed if desired
    def get_options(self):
        opt_str = {"get_options": {}}
        server_response = self.send_command(opt_str)
        return server_response

    # creates the game instance
    def create_game(self):
        create_str={}
        server_response = self.send_command_read_err(create_str)
        return json.dumps(server_response)

    # begins the game - WARNING!!!!: INCOMPLETE
    def start_game(self):
        self.stdin.write('{"get_options":{"list":1}}')
        print(str(self.read_out()))
