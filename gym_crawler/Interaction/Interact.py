import paramiko
import json


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
        send_data = json.dumps(auth_str).encode('utf_8')
        self.stdin.write(send_data)
        server_response = self.read_out()
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
        send_data = json.dumps(reg_str).encode('utf_8')
        self.stdin.write(send_data)

        server_response = self.read_out()
        if server_response["register"]["return"] == 3:
            return True
        return False

    # begins the game - WARNING!!!!: INCOMPLETE
    def start_game(self):
        self.stdin.write('{"get_options":{"list":1}}')
        print(str(self.read_out()))
