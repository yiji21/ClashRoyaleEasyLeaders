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
    print("Clan tag is not provided. Please pass in the tag by -c TAG command args.\nExiting.")
    sys.exit()


### DO NOT CHANGE ###
base_url = "https://api.clashroyale.com/v1"
clan_endpoint = "/clans/" + clan_tag
clan_warlog_endpoint = clan_endpoint + "warlog"
output_dir=output_dir_root + "/data/war"
### DO NOT CHANGE ###
if not os.path.exists(output_dir):
    os.makedirs(output_dir)




### Step 1: Create the workbook (if Tuesday) 
# or a worksheet (Thursday or Saturday) in the workbook 
# that stores data for the same week
now = datetime.datetime.now()
# today = datetime.date.today()
"Timestamp format: 20190708115026"
timestamp = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2) \
        +str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
# workbook_path = output_dir + "/" + timestamp + ".xlsx"
# workbook = xlsxwriter.Workbook(workbook_path)
# worksheet = workbook.add_worksheet()

headers = ["Name", "# Collection Day Battles Played", "# Cards Collected", 
"# Total Battles Given", "# Total Battles Done", "# Wins"]

# row = 0
# col = 0
# for header in headers:
#     worksheet.write_string(row,col,header)
#     col = col + 1


### Step 2: Fetch nodations and war data for each player

with open(token) as f:
    key = f.read().rstrip("\n")

    # Clan warlog data
    clan_warlog_request = urllib.request.Request(
              base_url + clan_warlog_endpoint,
              None,
              {
                    "Authorization": "Bearer %s" % key
              }
            )

    clan_warlog_response = urllib.request.urlopen(clan_warlog_request).read().decode("utf-8")
    clan_warlog_data = json.loads(clan_warlog_response)


    wars_processed = []
    ### Extracting war stats and donation stats
    for warlog in clan_warlog_data["items"]:

        war_season_id = str(warlog["seasonId"])
        war_created_date = str(warlog["createdDate"])[0:8]

        print("Processing war: %s_%s" % (war_season_id, war_created_date))

        workbook_path = output_dir + "/" + war_season_id + "_" + war_created_date + ".xlsx"
        workbook = xlsxwriter.Workbook(workbook_path)
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0
        for header in headers:
            worksheet.write_string(row,col,header)
            col = col + 1


        for player in warlog["participants"]: # 'tag',name','cardsEarned','battlesPlayed','wins','collectionDayBattlesPlayed','numberOfBattles'
            ### War stats
            tag = player['tag']
            name = player['name']
            cardsEarned = player['cardsEarned']
            battlesPlayed = player['battlesPlayed']
            wins = player['wins']
            collectionDayBattlesPlayed = player['collectionDayBattlesPlayed']
            numberOfBattles = player['numberOfBattles']

            print("\tProcessing player %s..." % name)

            contents = [name, collectionDayBattlesPlayed, cardsEarned, numberOfBattles, battlesPlayed, wins]
            row = row + 1
            col = 0
            for content in contents:
                worksheet.write_string(row,col,str(content))
                col = col + 1

        wars_processed.append(war_created_date)
        workbook.close()
    
    print("Done. %d wars processed." % len(wars_processed))
    # end for warlog in clan_warlog_data["items"]:
    