import discord
import os
import aiocron
import json
import requests
import re
from bs4 import BeautifulSoup, Comment
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
CHANNEL_ID=905950888521261168

client = discord.Client()

## pull event data from my json file
#e7_events = json.loads('events.json')

# use this to add events from user input
#x = {
#  "name": "John",
#  "age": 30,
#  "city": "New York"
#}

# convert into JSON:
#y = json.dumps(x)

## from https://www.geeksforgeeks.org/remove-all-style-scripts-and-html-tags-using-beautifulsoup/
def remove_tags(html): 
    soup = html
    for data in soup(['style', 'script']):
        data.decompose()
  
    return ' '.join(soup.stripped_strings)

# adapted from https://webautomation.io/blog/how-to-clean-web-scraping-data-using-python-beautifulsoup/
def clean(text):
    cleaner = re.compile('<.*?>')
    clean_text = re.sub(cleaner, '', text) 
    return str(clean_text)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello {}! It\'s me, Queen Chloe! :star_struck:'.format(message.author))

    if message.content.startswith('$help'):
        await message.channel.send('An Epic 7 helper bot made by AndATomato#9444.\nTadada! Queen Chloe is here to help!\n> To search for a character, enter \'$c\' followed by the character\'s name.\n> To search for an artifact, enter \'$a\' followed by the artifact\'s name.\n> To get a greeting from Chloe, enter \'$hello\'')

    ## character search
    if message.content.startswith('$c'):
        char_name = message.content.split("$c ",1)[1].replace(" ", "-") # gets whatever is searched for
        url = 'https://epic7x.com/character/' + char_name + '/'
        response = requests.get(url)
        await message.channel.send('{}'.format(url))

    ## character search
    if message.content.startswith('$a'):
        art_name = message.content.split("$a ",1)[1].replace(" ", "-") # gets whatever is searched for
        url = 'https://epic7x.com/artifact/' + art_name + '/'
        response = requests.get(url)
        await message.channel.send('{}'.format(url))
        #found = True
        #if found:
            #soup = BeautifulSoup(response.text, 'html.parser')
            #tier_info = soup.find(id='TierList')
            
            #description = clean(str(tier_info.find_all("p")))
            #artifacts = clean(str(tier_info.find_all(class_="f-12")))
            #sets = clean(str(tier_info.find_all(class_="pure-u-1 pure-u-md-1-2 text-center mt-20")))

            #stat_data = soup.find(id='SubstatPriority')
            # adapated from https://stackoverflow.com/questions/23299557/beautifulsoup-4-remove-comment-tag-and-its-content
            #for element in stat_data(text=lambda text: isinstance(text, Comment)):
            #    element.extract()

            #substats = clean(str(stat_data))
            #await message.channel.send('__**{}**__\n**Description**: {}\n**Artifacts**: {}\n**Sets**: {}\n**Substats**: {}'.format(char_name, description, artifacts, sets, substats))
        #else:
        #    await message.channel.send('Uh oh! I couldn\'t find that character, please try again!')

@aiocron.crontab('0 8 * * mon,wed,fri')
async def cornjob1():
    gw_channel = client.get_channel(906307886781718559) ##this needs to go into the guild war tab.
    await gw_channel.send('Tadada! Good morning! Today is {}, and that means today is guild war! Make sure to do your battles! Bang, bang! :star_struck:'.format(datetime.today().strftime('%A')))

@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(937783630732861492)
    await welcome_channel.send('Hi {member.name}, welcome to our Discord server! :star_struck:')

client.run(os.getenv('TOKEN'))

