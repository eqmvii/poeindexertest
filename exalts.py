# exalts.py
# A proof of concept for running live searches of the path of exile trade api 
# 
import requests 
import time
import sys
import datetime
chunklogger = 0

print("POE TRADE SNIPER 2000 BOOTING UP")

'''time.sleep(1)
print(".")
time.sleep(1)
print("..")
time.sleep(1)
print("...")
time.sleep(1)
print("")
print("")
print("")'''

f = open('ccid', 'r')
cur_change_id = f.readline()
f.close()

sanity = 0

poeapiurl = "http://api.pathofexile.com/public-stash-tabs/?id="
# cur_change_id = "85850361-90171930-84636963-97934537-91279768"

r = requests.get(poeapiurl + cur_change_id)

# print("This code ran, rat least.")
# print("Status code ok?")

itam = raw_input("Hello, Eric. Starting at cur_change_id " + cur_change_id + ".\nType in the name of the item you are looking for:\n\n")
print("Great. Let's check the live data stream for " + itam + "...")

if (r.status_code == requests.codes.ok):
    print("Status code ok!")
else:
    print("Status fail!")


data = r.json()

# print(r.text)
# print(data["next_change_id"])

# for stash in data["stashes"]:
    # print stash["accountName"]

cur_change_id = data["next_change_id"]
print ("###: Pulled first round of data...")

while(True):
    sanity = 0
    chunklogger +=1 
    r = requests.get(poeapiurl + cur_change_id)
    data = r.json()
    for stash in data["stashes"]:
        if (stash["lastCharacterName"] == "SONOFSMASHINGTON" or stash["lastCharacterName"] == "sonofsmashington" or stash["lastCharacterName"] == "SonOfSmashington"):
            with open("bingo", "a") as myfile:
                myfile.write("\nMy stashes at: " + cur_change_id + " \n")
            print("!!!!!!! ----------- ______ found my own stash ______ ------------- !!!!!!!!!!!!!")
        if (sanity > 500000):
            break
        # print (stash["accountName"] + " has added items to their premium stash")
        for item in stash["items"]:
            if (itam in item["name"]):
                if stash["public"] and "note" in item and item["league"] == "Harbinger":
                    print("-------------------")
                    print("@" + stash["lastCharacterName"] + " I'd like to buy your " + itam + " from your " + stash["stash"] + " stash tab, listed at " + item["note"] + " in " + item["league"] + " league.")
                    print("-------------------")
            # print (item["name"])
            sanity += 1
            if (sanity > 500000):
                print ("500,000 items searched and no tabula rosa found")
                break        
    cur_change_id = data["next_change_id"]
    print("###: Next " + cur_change_id)
    saveloc = open('ccid', 'w')
    saveloc.write(cur_change_id)
    saveloc.close()
    time.sleep(3)
