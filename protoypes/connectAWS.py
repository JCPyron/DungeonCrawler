import paramiko
import json


class Interact:
    # Logon Info
    hostname = 'ec2-34-229-53-61.compute-1.amazonaws.com'
    username = 'ubuntu'
    key = paramiko.RSAKey.from_private_key_file("NetCrawler.pem")
    stdin = ''
    stdout = ''
    stderr = ''
    client = ''

    # init connection and get file descriptors
    def __init__(self):
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
    def readOut(self):
        s = ""
        c = self.stdout.read(1)
        while c != b'\x00':
            s += str(c.decode("utf-8"))
            c = self.stdout.read(1)
        return json.loads(s)

    # read from stderr
    def readErr(self):
        s = ""
        c = self.stderr.read(1)
        while c != b'\x00':
            s += str(c.decode("utf-8"))
            c = self.stderr.read(1)
        return json.loads(s)

    # authenticate with the server
    def auth(self):
        self.stdin.write('{"auth":{"username":"XXX","password":"YYY","email":"NULL"}}\n')
        ret = self.readOut()
        if ret["auth"]["return"] == 3: return True
        return False

    def startGame(self):
        self.stdin.write('{"get_options":{"list":1}')
        print(str(self.readOut()))
i=Interact()
if i.auth(): print("connected")
else: print("err connecting")
i.startGame()