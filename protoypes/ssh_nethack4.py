import json
import sys
import paramiko
import re
import time

# Logon Info
hostname = 'ec2-34-229-53-61.compute-1.amazonaws.com'
username = 'ubuntu'
password = ''
PKey = 'NetCrawler.pem'

# Connect via SSH
def connectSSH(hostname, username, password, keyFile):
   try:
      key = paramiko.RSAKey.from_private_key_file(keyFile)
      client = paramiko.SSHClient()
      client.load_system_host_keys()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(hostname, port=22, username=username, password=password, pkey=key)
      print("LOG: Connected!", flush=True)
      return client
   except Exception as e:
      print("LOG: ", e, flush=True)
      print("LOG: Exiting...", flush=True)
      quit() 

def readSSH(stdout, stderr):
   start = time.time()
   print("LOG: Reading...", flush=True)
   time.sleep(5)
   while stdout.channel.recv_ready() == True:
      line = stdout.read(1)
      print(ansi_escape.sub('', line.decode('utf-8')), end='')
   end = time.time()
   timeTaken = end - start
   print("\nTime Elapsed Reading: ", timeTaken, flush=True)

client = connectSSH(hostname, username, password, PKey)

# Removes ANSI chars
ansi_escape = re.compile(r'''
    \x1B    # ESC
    [@-_]   # 7-bit C1 Fe
    [0-?]*  # Parameter bytes
    [ -/]*  # Intermediate bytes
    [@-~]   # Final byte
''', re.VERBOSE)

# Start NetHack4
print("LOG: Writing...", flush=True)
stdin, stdout, stderr = client.exec_command('./startServer')

# Auth
auth = {"auth": {"username": "xxxx", "password": "yyyy", "email": "NULL"}}
data = json.dumps(auth)
data.encode('utf-8')
stdin.write(data)
stdin.write('\n')

readSSH(stdout, stderr)

# Create a game
#json_message = {"get_options": {"options": ["gamemode", "character", "character name"]}}
#data = json.dumps(json_message)
#data.encode('utf-8')
#stdin.write(data)
#stdin.write('\n')

#readSSH(stdout, stderr)

# Close client
stdin.close()
stdout.close()
stderr.close()
client.close()

