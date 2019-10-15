import json
import sys
import paramiko
import re

# Logon Info
hostname = 'nethack4.org'
username = 'nethack43'
password = 'nethack43'

# Connect via SSH
client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect(hostname, port=22, username=username, password=password)
chnl = client.invoke_shell(width=100,height=100)

# Create I/O
stdin = chnl.makefile('w')
stdout = chnl.makefile('r')

# Removes ANSI chars
ansi_escape = re.compile(r'''
    \x1B    # ESC
    [@-_]   # 7-bit C1 Fe
    [0-?]*  # Parameter bytes
    [ -/]*  # Intermediate bytes
    [@-~]   # Final byte
''', re.VERBOSE)


for line in stdout.read().splitlines():
   print(ansi_escape.sub('', line.decode("utf-8")))


stdin.write('\n')
stdin.flush()

for line in stdout.read().splitlines():
   print(ansi_escape.sub('', line.decode("utf-8")))

client.close()
