#chaim 08/14/19
#Create a file named usernames.txt and put all the names to be checked on there
import requests, threading, os, time

with open("usernames.txt", "r+") as f:
    usernames =  f.read().splitlines()
available = open("available.txt", "w+")
clear = lambda:os.system("cls")
count, availableCount, unavailableCount = 0, 0, 0
headers = {
"Client-Id":"kimne78kx3ncx6brgo4mv6wki5h1ko"
}
def check():
    global count, availableCount, unavailableCount
    while len(usernames) != 0:
        try:
            username = usernames[0]
            usernames.remove(username)
            data = '[{"operationName":"UsernameValidator_User","variables":{"username":"' + username + '"},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"fd1085cf8350e309b725cf8ca91cd90cac03909a3edeeedbd0872ac912f3d660"}}}]'
            r = requests.post("https://gql.twitch.tv/gql", headers=headers, data=data).json()
            if (r[0]["data"]["isUsernameAvailable"] == False):
                unavailableCount += 1
            elif (r[0]["data"]["isUsernameAvailable"] == True):
                availableCount += 1
                available.write(username + "\n")
                available.flush()
            count += 1
        except:
            count -= 1
            usernames.append(username)
            print("Error")


threads = input("Threads [1-150]: ")
for x in range(int(threads)):
    t = threading.Thread(target=check)
    t.start()

while True:
    clear()
    print("Checked: {0}\nAvailable: {1}\nUnavailable: {2}".format(count, availableCount, unavailableCount))
    time.sleep(0.5)
