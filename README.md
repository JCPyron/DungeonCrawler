# Dungeon Crawler

## Table of contents
1. [Documentation](#doc)
    1. [Connecting to the AWS instance](#connect)
    2. [Setting up the game server](#server)
    3. [Installing the Crawler](#crawl)
    4. [Creating more actions](#act)
3. [Resources](#resources)


## Documentation <a name="doc"></a>
The Dungeon Crawlers decided to use NetHack4 as the open source code for their project because the game functions very similar to NetHack, and it's much more readable.

### Connecting to AWS <a name="connect"></a>
#### 1) Clone the GitHub Repository to get the .pem or .pkk file
This can be done a variety of ways. The preferred method is to install GitBash (https://git-scm.com/downloads) and run the following command:
`git clone https://git@github.com:JCPyron/DungeonCrawler.git`

#### Windows
install putty
Go to Connection>SSH>Auth
click browse and select the .pkk file
Go back to Session
Hostname should be:  ubuntu@ec2-34-229-53-61.compute-1.amazonaws.com
Port: 22
Connection Type: SSH
Type in a name for "Saved Sessions" and Click Save. That'll keep you from having to do all this again
click open then yes

#### Linux
run the following command `ssh -i "NetCrawler.pem" ubuntu@ec2-34-229-53-61.compute-1.amazonaws.com`



### Setting up the game server - You only have to do this once <a name="server"></a>

#### 1) Spin up the AWS instance (or any server of your choice) if needed

A guide to set up an Amazon Web Service Server (AWS Server) instance can be found here: https://aws.amazon.com/ec2/getting-started/

#### 2) Conect to the AWS server

Connect to the AWS server from your windows or linux client as described in [Connecting to the AWS instance] (#connect)

#### 3) Install git

Once connected to the server, install git. Our server is running Ubuntu 18.04 LTS, so we will use the command `sudo apt-get install git`

#### 4) Clone the GitHub Repository

Download all necessary files and packages from the GitHub repository to the home directory of server.

First, run `cd ~` in the server's terminal to change directories to the home directory

Next, run `git clone https://git@github.com/JCPyron/DungeonCrawler.git` in the server's terminal to clone the DungeonCrawler GitHub repository.

#### 5) Copy all the files in the "ServerFiles" folder to the home directory

Run `cp -r ~/DungeonCrawler/ServerFiles/* ~` in the server's terminal.

#### 6) Run the setup files

Set-up server files by running the bash script `./setup` in the server's terminal.

#### 7) Set up the PostgreSQL Database

```
sudo adduser nethack
```

*Input Password as "pass"*

```
sudo -u postgres createdb netdb
sudo -u postgres createuser --interactive
```

*Input "nethack" as username*

*Input "y" for yes*

```
sudo -u nethack psql -d netdb
CREATE EXTENSION pgcrypto;
\q
```

#### 8) Run the server

To start the nethack serivece, run `./startServer` in the server's terminal.




### Client side Installation of DungeonCrawler (For Windows)<a name="crawl"></a>

#### 1) Install  Python3

Newest version can be found at: https://www.python.org/downloads/

#### 2) Install Git Bash

Newest version can be found at: https://git-scm.com/downloads

#### 3) Add Python to the Path

Open Git Bash and try the `python3 --version` command. If the command is not found, Python needs to be added to the Path. To do this, use the command `export PATH="$PATH:/c/Program Files/PythonXX"` and replace the quoted in section with the correct file path to Python on your system

** Note:	Using export will only keep Python on the path for that session of Git Bash. To keep it 	permanently, it will require the editing of .bashrc**

#### 4) Installing Pip

Before doing this step make sure Git Bash is running as an administrator. In Git Bash run the `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` command to install required python file. Once the download finished, use the python `get-pip.py` command to install Pip. Similar to before, add Pip to the Path: `export PATH="$PATH:/c/Program Files/PythonXX/Scripts/"`.

#### 5)  Clone the Repository

Go the folder you would like to install the DungeonCrawler in Git Bash and clone the repository using `git clone https://github.com/JCPyron/DungeonCrawler.git` .

#### 6) Installing Dependencies

In Git Bash, run the following commands in order Pip to install the required decencies for the Agent and Environment:

```
pip3 install gym
pip3 install paramiko
pip3 install -e DungeonCrawler
```

Where DungeonCrawler is the local path to the DungeonCrawler project directory

#### 7) Update the Config File

If needed (i.e. when setting up a new client connection to a new AWS server) update the config file in the **agents** directory of the DungeonCrawler project directory of the client with the connection and logon information of the AWS server with server information (i.e. fields under [Connect] and [Host] as seen below)

```
; Connect to AWS Server
[Connect]
host=ec2-34-229-53-61.compute-1.amazonaws.com 
user=ubuntu
key_path=NetCrawler.pem

; NetHack Logon
[Logon]
user=random
password=ece431l02
email=NULL

; Options for the Game
[Options]
game_seed=012345678901234
```

#### 8) Run the Agent

Running the Agent is as simple as going to the **agents** directory and running the command `python3 random_agent.py` in Git Bash.

### Creating more game actions <a name="act"></a>

Actions are sent to the server via JSON commands formatted in a magical way as seen in the perfect and well-written Documentation seen here: https://nethackwiki.com/wiki/NetHack_4_Network_Protocol
The best example of how actions can be added to the Interact class (located in gym_crawler/Interaction folder) is the "register" command seen below

```Python
def register(self, username, password, email):
    reg_str = {"register": {"username": username, "password": password, "email": email}}
    send_data = json.dumps(reg_str).encode('utf_8')
    self.stdin.write(send_data)

    server_response = self.read_out()
    if server_response["register"]["return"] == 3:
        return True
    return False
```

The method creates a JSON object with the fields and their values (provided by the Wiki), uses the json.dumps command to write the command to a string and encodes it to utf-8. The command is then written to stdin and the server response is read. If it was successful, it returns True.

All commands will look similar to this method. They should create a JSON object with the proper fields and then write to stdin. The largest problem with the server is that it shuts down after a command is received that is improperly formatted.

For implementation, when the agent decides it wants to preform a specific action, it will simply run the method which will then send the command to the server.

During development, we tried to keep everything as separated as possible to allow for individual, concurrent development. It also allows the code to be easily improved and developed.

## Resources <a name="resources"></a>

### NetHack4 wiki

https://nethackwiki.com/wiki/NetHack_4

### NetHack4 JSON Commands Help

http://nethack4.org/latest/nethack4/doc/server_protocol.txt

http://nethack4.org/latest/nethack4/libnethack_common/include/nethack_types.h

### Reinforcement Learning Articles:

https://skymind.ai/wiki/deep-reinforcement-learning

https://gym.openai.com/docs/#environments

https://towardsdatascience.com/reinforcement-learning-from-scratch-designing-and-solving-a-task-all-within-a-python-notebook-48c40021da4

https://www.kdnuggets.com/2018/03/5-things-reinforcement-learning.html

https://www.kaggle.com/osbornep/-reinforcement-learning-from-scratch-in-python/kernels

https://github.com/deepmind/bsuite

### Papers and Posts:

Combat in NetHack: https://pdfs.semanticscholar.org/d9fa/662a6beb2d8a7d7dca11d4aa9d2172ae2316.pdf

Exploration and Combat in NetHack: http://gram.cs.mcgill.ca/theses/campbell-18-exploration.pdf

First Successful Bot: https://www.reddit.com/r/nethack/comments/2tluxv/yaap_fullauto_bot_ascension_bothack/

### Creating an Environment:

https://medium.com/@apoddar573/making-your-own-custom-environment-in-gym-c3b65ff8cdaa

https://www.novatec-gmbh.de/en/blog/creating-a-gym-environment/

### Stable Baselines for Testing:

https://stable-baselines.readthedocs.io/en/master/

### Readable Code

https://learning.oreilly.com/library/view/clean-code/9780136083238/

### PEP8 Standards

https://www.python.org/dev/peps/pep-0008/

### Git

https://nvie.com/posts/a-successful-git-branching-model/

https://github.github.com/training-kit/downloads/github-git-cheat-sheet.pdf
