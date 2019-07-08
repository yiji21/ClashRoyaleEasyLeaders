
"""Input: the location of where you are invoking the script. 
Current options: [home, office].
Depending on the location, a different token is passed to the CR server."""

import urllib.request
import json
import datetime
import xlsxwriter
import sys, os


output_dir_root = os.getcwd()
clan_tag = ""
n_args = len(sys.argv)
token = sys.argv[1]
i = 2 
while i < n_args:
    if sys.argv[i] == "-o":
        if i + 1 == len(sys.argv):
            print("Error! Please provide the root for output directory after -o.\nExiting.")
            sys.exit()
        output_dir_root = sys.argv[i+1]
        if not is_path_exists_or_creatable(output_dir_root):
            print("Error! The directory root provided is not a valid path.\nExiting.")
            sys.exit()
        i = i + 2
    elif sys.argv[i] == "-c":
        if i + 1 == len(sys.argv):
            print("Error! Please provide the clan tag after -c.\nExiting.")
            sys.exit()
        if "#" in sys.argv[i+1]:
            print("Error! Please do NOT type the # at the start of the tag.\nExiting.")
            sys.exit()
        clan_tag = "%23"+sys.argv[i+1]+"/"
        i = i + 2

    else:
        i = i + 1   # Future: leave space for extension to support more args

if not clan_tag.strip():
    print("Error! Clan tag is not provided. Please pass in the tag by -c TAG command args.\nExiting.")
    sys.exit()


### DO NOT CHANGE ###
base_url = "https://api.clashroyale.com/v1"
clan_endpoint = "/clans/" + clan_tag
clan_members_endpoint = clan_endpoint + "members"
output_dir=output_dir_root + "/data/player"
### DO NOT CHANGE ###
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


### Step 1: Create the workbook, file nanme is the crreunt timestamp
now = datetime.datetime.now()
"Timestamp format: 20190708115026"
timestamp = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2) \
        +str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
workbook_path = output_dir + "/" + timestamp + ".xlsx"
workbook = xlsxwriter.Workbook(workbook_path)
worksheet = workbook.add_worksheet()

# Write the spreadsheet header
headers = ["Name", 
    "Donations", 
    "Donations Received", 
    "Trophies", 
    "Clan Rank", 
    "Role",
    "Clan Chest Points"]

row = 0
col = 0
for header in headers:
    worksheet.write_string(row,col,header)
    col = col + 1


### Step 2: Fetch player info
with open(token) as f:
    key = f.read().rstrip("\n")

    # Clan warlog data
    clan_members_request = urllib.request.Request(
              base_url + clan_members_endpoint,
              None,
              {
                    "Authorization": "Bearer %s" % key
              }
            )

    clan_members_response = urllib.request.urlopen(clan_members_request).read().decode("utf-8")
    clan_members_data = json.loads(clan_members_response)

    for member in clan_members_data['items']:
        tag = member['tag']
        name = member['name']
        expLevel = str(member['expLevel'])
        trophies = str(member['trophies'])
        arena = member['arena']
        role = member['role']
        clanRank = str(member['clanRank'])
        previousClanRank = str(member['previousClanRank'])
        donations = str(member['donations'])
        donationsReceived = str(member['donationsReceived'])
        clanChestPoints = str(member['clanChestPoints'])

        contents = [name, donations, donationsReceived, trophies, clanRank, role, clanChestPoints]
        row = row + 1
        col = 0
        for content in contents:
            worksheet.write_string(row,col,str(content))
            col = col + 1

workbook.close()