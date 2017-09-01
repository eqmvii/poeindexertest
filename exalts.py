# exalts.py
# A simple proof of concept for running live searches of the path of exile trade api 
# exalts.py
# a python script to monitor the Path of Exile public stash API 
# only looks for specific item names
# must get a cur_change_id from somewhere to start the process 

import requests 
import time
import sys
import datetime
chunklogger = 0

# configuration variables
mycharname = "dummyplaceholdernamegoeshere"
ping_rate = 1 # number of seconds to sleep between API requests
cur_league = "Harbinger"
# end configuration variables

print("POE TRADE MONITOR BOOTING UP")

# read from file the most recent cur_change_id written by the program
river_log = open('ccid', 'r')
cur_change_id = river_log.readline()
river_log.close()

# Do one data request and test results
poeapiurl = "http://api.pathofexile.com/public-stash-tabs/?id="
try:
    new_stash_data = requests.get(poeapiurl + cur_change_id, timeout = 5)
    target_item = raw_input("Hello. Starting at cur_change_id " + cur_change_id + ".\nType in the name of the item you are looking for:\n\n")
    print("Great. Let's check the live data stream for " + target_item + "...")
    if (new_stash_data.status_code == requests.codes.ok):
        print("Data retrieved from PoE API; status code ok!")
    else:
        print("ERROR: http request status code fai! The API request didn't work for some reason (the API might be down?)")
        sys.exit()
    current_data = new_stash_data.json()
    # cur_change_id = current_data["next_change_id"]
    print ("###: Pulled first round of data at cur_change_id: " + cur_change_id)
except:
    print("Unexpected error on API request:", sys.exc_info()[0])


# continuously monitor the stream of new stash data looking for the item
while(True):
    stashcount = 0    
    chunklogger +=1 
    # sanity tries to break if something causes an infinite loop
    sanity = 0

    try:
        new_stash_data = requests.get(poeapiurl + cur_change_id, timeout = 5)
    except:
        with open("bingo", "a") as myfile:
            myfile.write("\nData retrieval error on data chunk " + str(chunklogger))
        print("Data retrieval error, probably an API timeout...")
        continue
       
    data = new_stash_data.json()
    icount = 0
    for stash in data["stashes"]:
        stashcount += 1
        if (stash["lastCharacterName"] == mycharname or stash["lastCharacterName"] == "sonofsmashington" or stash["lastCharacterName"] == "SonOfSmashington"):
            with open("bingo", "a") as myfile:
                myfile.write("\nMy stashes at: " + cur_change_id + " \n")
            print("!!!!!!! ----------- ______ found my own stash ______ ------------- !!!!!!!!!!!!!")
        if (sanity > 50000):
            break        
        for item in stash["items"]:
            if (target_item in item["name"]):
                # if stash["public"] and "note" in item and item["league"] == cur_league:
                if stash["public"] and "note" in item:
                    print("-------------------")
                    print("@" + stash["lastCharacterName"] + " I'd like to buy your " + target_item + " from your " + stash["stash"] + " stash tab, listed at " + item["note"] + " in " + item["league"] + " league.")
                    print("-------------------")
            # print (item["name"])
            sanity += 1
            icount += 1
            if (sanity > 50000):
                print ("50,000 items searched in this chunk but no match was found")
                break        
    cur_change_id = data["next_change_id"]
    print("###: Checked " + str(icount) + " items in " + str(stashcount) + " stashes from this pull. Checked " + str(chunklogger) + " data chunk(s). Next cur_change_id is: " + cur_change_id)
    saveloc = open('ccid', 'w')
    saveloc.write(cur_change_id)
    saveloc.close()
    time.sleep(ping_rate)
