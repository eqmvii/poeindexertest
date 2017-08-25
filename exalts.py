# exalts.py
# A proof of concept for running live searches of the path of exile trade api 
# 
import requests 
import time
import sys

print("POE TRADE SNIPER 2000 BOOTING UP")
time.sleep(1)
print(".")
time.sleep(1)
print("..")
time.sleep(1)
print("...")
time.sleep(1)
print("")
print("")
print("")
itam = raw_input("Hello, Eric. Type in the name of the item you are looking for.")
print("Great. Let's check the live data stream for " + itam + "...")

sanity = 0

poeapiurl = "http://api.pathofexile.com/public-stash-tabs/?id="
cur_change_id = "85467415-89772001-84257940-97507737-90871074"

r = requests.get(poeapiurl + cur_change_id)

print("This code ran, rat least.")
print("Status code ok?")

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
print ("Pulled first round of data...")

while(True):
    print("######################################## next search...")
    sanity = 0
    r = requests.get(poeapiurl + cur_change_id)
    data = r.json()
    for stash in data["stashes"]:
        if (sanity > 50000):
            break
        # print (stash["accountName"] + " has added items to their premium stash")
        for item in stash["items"]:
            if (itam in item["name"]):
                if stash["public"] and "note" in item and item["league"] == "Harbinger":
                    print("-------------------")
                    print("@" + stash["lastCharacterName"] + " I would like to buy your " + itam + " listed for " + item["note"] + " in " + item["league"])
                    print("-------------------")
            # print (item["name"])
            sanity += 1
            if (sanity > 50000):
                print ("50,000 items searched and no tabula rosa found")
                break        
    cur_change_id = data["next_change_id"]
    print("########################################")
    time.sleep(6)
