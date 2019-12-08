# Dungeon Crawler
## Introduction
RL environment created for ECE/MEE 341L

## Documentation
The Dungeon Crawlers decided to use NetHack4 as the open source code for their project because the game functions very similar to NetHack, and it's much more readable.

## Installation of DungeonCrawler (For Windows)

### 1) Install  Python 

Newest version can be found at: https://www.python.org/downloads/

### 2) Install Git Bash

Newest version can be found at: https://git-scm.com/downloads

### 3) Add Python to the Path 

Open Git Bash and try the `python --version` command. If the command is not found, Python needs to be added to the Path. To do this, use the command `export PATH="$PATH:/c/Program Files/PythonXX"` and replace the quoted in section with the correct file path to Python on your system

###### Note:	Using export will only keep Python on the path for that session of Git Bash. To keep it 	permanently, it will require the editing of .bashrc

### 4) Installing Pip

Before doing this step make sure Git Bash is running as an administrator. In Git Bash run the `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` command to install required python file. Once the download finished, use the python `get-pip.py` command to install Pip. Similar to before, add Pip to the Path: `export PATH="$PATH:/c/Program Files/PythonXX/Scripts/"`.

### 5)  Clone the Repository

Go the folder you would like to install the DungeonCrawler in Git Bash and clone the repository using `git clone https://github.com/JCPyron/DungeonCrawler.git` .

### 6) Installing Dependencies

In Git Bash, run the following commands in order Pip to install the required decencies for the Agent and Environment:
```
pip install gym
pip install paramiko
pip install -e DungeonCrawler
```

### 7) Run the Agent

Running the Agent is as simple as going to the **agents** directory and running the command `python random_agent.py` in Git Bash. 

## Resources

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
