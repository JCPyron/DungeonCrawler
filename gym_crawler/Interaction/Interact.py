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
    options_json = ''
    MAX_CHAR_SEND = 4096

    # init connection and get file descriptors
    def __init__(self, hostname, username, key_path):
        self.options_json = json.loads(''.join(open("options.json").readlines()))
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

    # server only reads in 4096 characters at a time.
    # This means, for larger commands, they must be split up
    def __send_large_command__(self, send_str):
        for i in range(0, len(send_str), self.MAX_CHAR_SEND):
            self.stdin.write(send_str[i:i + self.MAX_CHAR_SEND - 1] + b'\n')

    # sends the given json command and returns the result
    def send_command(self, send_str):
        send_data = json.dumps(send_str).encode('utf_8')
        if len(send_data) > self.MAX_CHAR_SEND:
            self.__send_large_command__(send_data)
        else:
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

    # function to run the functions to start the game, play it, and end it
    def nethack4_main(self):
        self.auth("random", "ece431l02", "NULL")
        game_id = self.create_game("", "ken", -2, -2, -2, -2)
        self.play_game(game_id, 0)
        self.exit_game(1)
        return True

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
        opt_str = {'get_options': {}}
        server_response = self.send_command_read_err(opt_str)
        return server_response

    # creates the game instance
    def create_game(self, seed='', name='Ken', role=-2, race=-2, align=-2, gender=-2):
        for option in self.options_json["options"]:
            if option["name"] == 'seed':
                option["value"] = seed
            elif option["name"] == 'name':
                option["value"] = name
            elif option["name"] == 'role':
                option["value"] = role
            elif option["name"] == 'race':
                option["value"] = race
            elif option["name"] == 'alignment':
                option["value"] = align
            elif option["name"] == 'gender':
                option["value"] = gender
        create_str = {"create_game": self.options_json}
        server_response = self.send_command(create_str)
        return json.dumps(server_response)

    # Lists which command can be used in "request_command" command
    def get_commands(self):
        get_cmd_str = {"get_commands": {}}
        server_response = self.send_command(get_cmd_str)
        print(server_response)

    # begins the game
    def play_game(self, gameid, FM_PLAY):
        play_str = {"play_game": {"gameid": gameid, "followmode": FM_PLAY}}
        server_response = self.send_command(play_str)
        if server_response["play_game"]["return"] == 0:
            return True
        return server_response

    # exits the game(?)
    def exit_game(self, EXIT_QUIT):
        exit_str = {"exit_game": {"exit_type": EXIT_QUIT}}
        server_response = self.send_command(exit_str)
        return server_response
