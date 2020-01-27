from Interact import Interact

host = "ec2-34-229-53-61.compute-1.amazonaws.com"
pem = "/home/ubuntu/NetCrawler.pem"
user = "random"
pwd = "ece431l02"
email = "NULL"
console = Interact(host, "ubuntu", pem)
while input("Continue (Y/N)? ").upper() == "Y":
    cmd = input("Enter Command: ").lower().strip()
    if cmd == "auth":
        print(console.auth(user, pwd, email))
    elif cmd == "register":
        print(console.register(user, pwd, email))
    elif cmd == "create_game":
        print(console.create_game())
