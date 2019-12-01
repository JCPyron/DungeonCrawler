import paramiko
import json

class Interact:
    # ssh info
    host_name = ''
    user_name_ssh = ''
    key = ''

    # I/O
    stdin = ''
    stdout = ''
    stderr = ''
    client = ''

    # init connection and get file descriptors
    def __init__(self, host_name, user_name, key_path):
        # connection information
        self.host_name = host_name
        self.user_name_ssh = user_name
        self.key = paramiko.RSAKey.from_private_key_file(key_path)      

        # connect
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host_name, port=22, username=self.user_name_ssh, pkey=self.key)
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
    def auth(self, user_name, password):
        # json to utf-8
        auth = {"auth": {"username": user_name, "password": password, "email": "NULL"}}
        data = json.dumps(auth)
        data.encode('utf-8')

        # write and read data 
        self.stdin.write(data)
        server_response = self.read_out()
        print(server_response)
        if server_response["auth"]["return"] == 3:
            return True
        return False

    # start a game of nethack4
    def start_game(self):
        self.stdin.write('{"get_options":{"list":1}}')
        print(str(self.read_out()))