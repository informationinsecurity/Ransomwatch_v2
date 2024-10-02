from scrapers import *
import requests
import json
import re
from datetime import date
from slack_webhook import Slack
from slack_sdk import WebClient
import mysql.connector
import urllib
from getpass import getpass
from mysql.connector import connect, Error
import json
from datetime import datetime
from argparse import ArgumentParser
from os.path import join, dirname, realpath
import time
import shutil
import base64
import os
import sys
import ast
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import time

global proxy
proxy = "socks5h://127.0.0.1:9050"

global headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

global proxies
proxies = {
    'http': proxy,
    'https': proxy
}
#Dev = 1 puts in a different channel for troubleshooting
DEV = 0
PRINT_JSON = 0
POST_SLACK = 1
PULL_VICTIM_LIST = 1
PULL_GROUP_LIST = 1
ENABLE_SCREENSHOTS = 1
PARSE_SCRAPERS = 1
ransomwatch_url = "https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json"
ransomwatch_groups = "https://raw.githubusercontent.com/joshhighet/ransomwatch/main/groups.json"


#rwatch app
slack_bot_token = '<xoxb-token-here'
slack_signing_secret = '<slack_signing_secret-here>'

client = WebClient(token=slack_bot_token)

if DEV == 0:

    slack_webhook = "<slack-webhook-prod>"
    slack_channel_id = "<prod channel id>"

if DEV == 1:
    slack_webhook = "<slack-dev-webhook>"
    slack_channel_id = "<dev channel id>"

slack_message = ""

###MYSQL SETTINGS
mydb = mysql.connector.connect(
  host="<host>",
  user="<user>",
  password="<password>",
  database="<database>"
)
writedb = True

chromedriver_path = "/usr/bin/chromedriver"  # Adjust this path to your chromedriver location
# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
socks5_proxy = "socks5://127.0.0.1:9050"  # Update with your proxy details
chrome_options.add_argument(f"--proxy-server={socks5_proxy}")

# Initialize the Chrome driver
driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

screenshot_directory = "./screenshots/"


def post_screenshot_slack(victim_name, threat_group):
    if threat_group == "blacksuit":
        victim_name = victim_name.replace('https://', '')
        victim_name = victim_name.replace('http://', '')
        print(f"trying to screenshot {victim_name}")

    # Find if message has psoted to channel
    result = client.conversations_history(channel=slack_channel_id)
    conversation_history = result["messages"]
    message_found = 0
    matching_message_ts = ''

    for individual_message in conversation_history:
        single_message = individual_message["text"]
        single_message_ts = individual_message["ts"]

        if victim_name in single_message:
            print("Victim has been posted to Slack")
            screenshot_filename = f'{victim_name}.png'

            screenshot_path = os.path.join(screenshot_directory, screenshot_filename)
            print(f"SHould save to {screenshot_filename}")
            print(f"Should save to {screenshot_path}")
            screenshot_size = os.path.getsize(screenshot_path)

            print("TESTING UPLOAD - SHOULD GET A URL")
            ##GET URL FOR UPLOAD
            upload_text_file = client.files_getUploadURLExternal(
                filename=screenshot_filename,
                length=screenshot_size,
                pretty=1
            )
            print(upload_text_file)
            file_upload_url = re.search(r"(upload_url.*?,)", str(upload_text_file))
            file_upload_url = file_upload_url.group(1)
            file_upload_url = file_upload_url.replace('upload_url\': \'','')
            file_upload_url = file_upload_url.replace('\',','')
            file_upload_id = re.search(r"(file_id.*?})", str(upload_text_file))
            file_upload_id = file_upload_id.group(1)
            file_upload_id = file_upload_id.replace('file_id\': \'','')
            file_upload_id = file_upload_id.replace('\'}','')

            print(file_upload_url)
            print(file_upload_id)
            ##POST FILE TO URL
            with open(screenshot_path, 'rb') as file:
                response = requests.post(file_upload_url, files={'file': file})

            print(response.text)
            files_array = [{"id": file_upload_id, "title": screenshot_filename}]

            ##REFERENCE FILE FOR CHANNEL
            complete_upload = client.files_completeUploadExternal(
                files=files_array,
                channel_id=slack_channel_id,
                thread_ts=single_message_ts
            )

            # response = requests.request("POST", file_upload_url, files=)

            # time.sleep(30)


            # upload_text_file = client.files_upload(
            #     channels=slack_channel_id,
            #     title=screenshot_filename,
            #     file=screenshot_path,
            #     initial_comment=screenshot_filename,
            #     thread_ts=single_message_ts
            # )
def get_locations_by_name(name):
    locations = []
    if name in data_by_name_and_location:
        locations = list(data_by_name_and_location[name].keys())
    return locations

def extract_url(url_input):
    if isinstance(url_input, list):
        # If it's already a list, return the first element
        return url_input[0] if url_input else None
    elif isinstance(url_input, str):
        # If it's a string, try to eval it as a list
        try:
            url_list = ast.literal_eval(url_input)
            return url_list[0] if isinstance(url_list, list) and url_list else url_input
        except:
            # If eval fails, just return the string as is
            return url_input.strip("[]'")
    else:
        # If it's neither a list nor a string, return it as is
        return url_input

if PULL_GROUP_LIST == 1:
    print("Updating Threat Group Lists")
    response = requests.request("GET", ransomwatch_groups)
    # response = requests.request("GET", ransomwatch_url, headers=cases_headers, data=closed_case_details_payload)
    ransomwatch_groups_result = response.text
    data = json.loads(ransomwatch_groups_result)
    data_by_name_and_location = {}
    # Storing the data for quick reference by Name and Location
    for data_point in data:
        name = data_point["name"]
        locations = data_point["locations"]
        if name not in data_by_name_and_location:
            data_by_name_and_location[name] = {}
        for location in locations:
            fqdn = location["fqdn"]
            data_by_name_and_location[name][fqdn] = location



if PULL_VICTIM_LIST == 1:
    victim_count = 0
    print("Pulling Current Victim List")
    response = requests.request("GET", ransomwatch_url)
    # response = requests.request("GET", ransomwatch_url, headers=cases_headers, data=closed_case_details_payload)
    ransomwatch_result = response.text
    # print(ransomwatch_result)
    today = date.today()
    # print("Today's date:", today)
    ### Load List of victims to avoid Duplicates
    historic_victims = ''
    f = open("victims", "r", encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        historic_victims += line
    f.close()
    for line in str(ransomwatch_result).split('},'):
        slack_message = ''
        mycursor = mydb.cursor()
        if PRINT_JSON == 1:
            print(line)
        victim_name = re.search(r"(\"post_title\":.*?,)", line)
        victim_name = victim_name.group(1)
        victim_name = victim_name.replace('\"post_title\": \"','')
        victim_name = victim_name.replace('\",','')

        threat_group = re.search(r"(\"group_name\":.*?,)", line)
        threat_group = threat_group.group(1)
        threat_group = threat_group.replace('\"group_name\": \"', '')
        threat_group = threat_group.replace('\",','')

        published_date = re.search(r"(\"discovered\":.*)", line)
        published_date = published_date.group(1)
        published_date = published_date.replace('\"discovered\": \"','')
        published_date = published_date.replace('\"','')
        #limit to current date
        # if published_date[:10] in str(today) and victim_name not in historic_victims:
        #limit to current year
        # if published_date[:4] in str(today) and victim_name not in historic_victims:
        if victim_name not in historic_victims:

            # Example usage:
            name_to_search = threat_group
            locations = get_locations_by_name(name_to_search)
            if locations:
                # print(locations)
                # print("Locations for", name_to_search, ":", ", ".join(locations))
                # print(str(locations))
                str_locations = str(locations)
                try:
                    short_location = re.search(r"(.*\', \')", str_locations).group(0)
                    short_location = short_location.replace('\', \'','')
                    short_location = str(short_location).replace('[\'','')
                    parts = short_location.split('.onion')

                    # If '.onion' is found in the URL
                    if len(parts) > 1:
                        # Take everything before '.onion' and add '.onion' back
                        onion_part = parts[0].split('/')[-1] + '.onion'
                        short_location = onion_part.strip()
                        # print("Shortened the URL")


                except:
                    short_location = locations

                short_location = str(short_location)
                short_location = short_location.replace('[\'', '')
                short_location = short_location.replace('\']', '')

                try:
                    print("Count " + str(victim_count))
                    print("Victim Name: " + str(victim_name))
                    print("Threat Group: " + str(threat_group))
                    print("Published On: " + str(published_date))
                    print("URL: " + str(short_location))
                except:
                    print("Cannot print name - likely unicode issue")

                # print("Location for " + str(threat_group) + ": " + extract_url(short_location))

            else:
                print("No locations found for", name_to_search)
            #Add to database
            dupecheck = "SELECT EXISTS(SELECT * from rw_victims where victim like %s)"
            mycursor.execute(dupecheck, (victim_name,))
            duperesult = mycursor.fetchall()
            print(duperesult)
            if str(duperesult) != "[(1,)]":
                print("New Victim Found! - Adding to database")
                # time.sleep(10)

                sql = "INSERT IGNORE INTO rw_victims (id, actor, url, victim, date) VALUES (NULL, %s, %s, %s, %s)"
                val = (str(threat_group), extract_url(short_location), str(victim_name), str(published_date))
                if writedb == True:
                    # try:
                    mycursor.execute(sql, val)
                    mydb.commit()
                    # except:
                    #     print(f"Error adding {victim_name} by {threat_group} to database!")
                    # Add to database

                    ##Compare to Partners and Tenants
                    print("Checking if existing Todyl Customer")
                    dupecheck2 = "SELECT EXISTS(SELECT * from Tenants where Tenants.tenant_name like %s)"
                    mycursor.execute(dupecheck2, (victim_name,))
                    duperesult2 = ''
                    duperesult2 = mycursor.fetchall()
                    print(str(duperesult2))
                    if "1" in str(duperesult2):
                        slack_warning = ''
                        print("Victim matches Todyl Tenant Name! Alerting!")
                        slack_warning = "<!channel> - " +str(victim_name)+ " appears to match one of our tenants - please investigate!"
                        post_to_slack = Slack(url=slack_webhook)
                        post_to_slack.post(text=slack_warning)
                        slack_warning = ''
                        # time.sleep(10)

                if POST_SLACK == 1:
                    locations = str(locations).replace('[','')
                    locations = str(locations).replace(']','')

                    slack_message += "Ransomware Victim Identified:\nCompany Name: `" + str(victim_name) + "`\nThreat Group: `" + threat_group + "`\nPublished On: `" + str(published_date) + "`\nLeak Site: `" + str(short_location) + "`"
                    try:
                        if slack_message:
                            post_to_slack = Slack(url=slack_webhook)
                            post_to_slack.post(text=slack_message)
                            print("Sent Slack Notification")
                    except:
                        print("Failed to send to slack!")
                if ENABLE_SCREENSHOTS == 1:
                    screenshot_needed = 0
                    print("Running applicable Parsers")
                    try:
                        ###Clean up names
                        if "http://" in victim_name:
                            victim_name = victim_name.replace('http://','')
                        if "https://" in victim_name:
                            victim_name = victim_name.replace('https://','')
                        if "/" in victim_name:
                            victim_name = victim_name.replace('/','')
                        if threat_group == "ransomhub":
                            scrape_ransomhub(victim_name, short_location)
                            screenshot_needed = 1

                        # if threat_group == "cactus":
                        #     scrape_cactus(victim_name, short_location)

                        if threat_group == "play":
                            scrape_play(victim_name, short_location)
                            screenshot_needed = 1

                        if threat_group == "dAn0n":
                            scrape_danon(victim_name, extract_url(short_location))
                            screenshot_needed = 1

                        if threat_group == "darkvault":
                            scrape_darkvault(victim_name, extract_url(short_location))
                            screenshot_needed = 1

                        if threat_group == "bianlian":
                            scrape_bianlian(victim_name, extract_url(short_location))
                            screenshot_needed = 1

                        if threat_group == "blacksuit":
                            scrape_blacksuit(victim_name, extract_url(short_location))
                            screenshot_needed = 1

                        if threat_group == "handala":
                            scrape_handala(victim_name, extract_url(short_location))
                            screenshot_needed = 1

                        if threat_group == "eldorado":
                            scrape_eldorado(victim_name, extract_url(short_location))
                            screenshot_needed = 1

                        if threat_group == "spacebears":
                            scrape_spacebears(victim_name, extract_url(short_location))
                            screenshot_needed = 1

                        if threat_group == "cicada3301":
                            scrape_cicada3301(victim_name, extract_url(short_location))
                            screenshot_needed = 1

                        if threat_group == "qilin":
                            scrape_qlin(victim_name, extract_url(short_location))
                            screenshot_needed = 1

                    except:
                        print(f"Scraping victim {victim_name} failed!")

                    if screenshot_needed == 1 and ENABLE_SCREENSHOTS == 1:
                        try:
                            print("Attempting to gather screenshots")
                            post_screenshot_slack(victim_name, threat_group)
                        except:
                            print(f"Failed to send screenshot {victim_name} to slack!")

                historic_victims += victim_name + "\n"
                # add victims to the victim list
                f = open("victims", "a", encoding='utf-8')
                f.write(victim_name)
                f.write("\n")
                f.close()
                victim_count += 1
                print("--------")

            elif str(duperesult) == "[(0,)]":
                print("DUPLICATE ENTRY --Found in database")
                # time.sleep(30)



