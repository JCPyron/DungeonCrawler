from Interact import Interact

host = "ec2-34-229-53-61.compute-1.amazonaws.com"
pem = "D:\\Docs\\ECE341L\\DungeonCrawler\\agents\\NetCrawler.pem"
user = "random"
pwd = "ece431l02"
email = "NULL"
console = Interact(host, "ubuntu", pem)

# {"auth": {"username": "random", "password": "ece431l02", "email": "NULL"}}

while input("Continue (Y/N)? ").upper() != "N":
    cmd = input("Enter Command: ").lower().strip()
    if cmd == "auth":
        print(console.auth(user, pwd, email))
    elif cmd == "register":
        print(console.register(user, pwd, email))
    elif cmd == "get_options":
        print(console.get_options())
    elif cmd == "create_game":
        print(console.create_game())
    else:
        print("unrecognized command")
