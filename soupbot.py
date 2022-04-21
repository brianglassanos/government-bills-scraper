"""
Scrapes Data based on provided URL parameters
"""
import os
from bs4 import BeautifulSoup
from collections import Counter
import requests

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

""" 
Uncomment for verbose logging purposes 
"""
# import logging
# logging.basicConfig(level=logging.INFO)

from urllib.parse import urljoin, unquote
import re
import os 

""" 
URL will be turned into a BeautifulSoup Object.
"""
url = "https://www.espn.com"
base_site = requests.get(url)
soup = BeautifulSoup(base_site.content, 'html.parser')

""" 
Processes | Possibly turn into Functions
List comprehension loops through soup.find_all, returning specified tags, attributes. link_paths then accesses the href attribute of those tags. 
"""
links = [item for item in soup.find_all("a")]
link_paths = [l.get('href') for l in links]

""" 
Uncomment the following List comprehensions to see how certain keywords can be searched.
"""
# members = [url for url in link_paths if 'members' in url]
# congress = [url for url in link_paths if 'congress' in url]

""" 
Chatbot Helper Resource: 
Helps user out with website data discovery + exploration
"""

a_links = [item.text for item in soup.find_all("a")]

conversation = [
    "Hi there! I am Soupbot. Feed me any decoded URL and I will scrape data from that website for you.",
    f"Here are all of the <a> tags I could find: \n{a_links}"
]

bot = ChatBot(
    "Souperman",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.sqlite3'
)
trainer = ListTrainer(bot)
trainer.train(conversation)

""" 
Easy recursion with While Loop for user_input 
ctrl+c to break out of loop.
"""
while True:
    try:
        # os.system('clear')
        user_input = input("Command: ")
        bot_input = bot.get_response(user_input)
        print(bot_input)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break

