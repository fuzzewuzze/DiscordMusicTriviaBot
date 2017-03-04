from __future__ import unicode_literals
import discord
import asyncio
import youtube_dl
from random import randint
import operator
import csv
import urllib
import urllib3
from bs4 import BeautifulSoup

discord.opus.load_opus('libopus-0.x64.dll')

client = discord.Client()
playerList = {'Test': 5}
currentRound = 1
currentSongArtist = ""
currentSongName = ""
currentSongList = []
voice = None


def GetSongUrl(song):
    print("Finding: {}".format(song))
    query = urllib.parse.quote(song)

    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    vid = soup.find(attrs={'class':'yt-uix-tile-link'})
    return ("https://www.youtube.com{}".format(vid['href']))

def SetSongArtist(songArtist):
    global currentSongArtist
    currentSongArtist = songArtist

def GetCurrentSongArtist():
    global currentSongArtist
    return currentSongArtist

def SetSongName(songName):
    global currentSongName
    currentSongName = songName

def GetSongName():
    global currentSongName
    return currentSongName

def PrintScores():
    sorted_players = sorted(playerList.items(), key=operator.itemgetter(1))
    scoreMessage = 'Current Game Scores\r\n'
    scoreMessage += '---------------------------\r\n'
    for player, score in sorted_players:
        scoreMessage += str(player) + ": " + str(score) + "\r\n"
    return scoreMessage

def RegisterPlayer(playerName):
    playerList[playerName] = 1

def IncrementRound(self):
    self.currentRound += 1

def GetAudioDuration(url):
    opts = {
        'format': 'webm[abr>0]/bestaudio/best',
        'prefer_ffmpeg': True,
        'simulate': True,
    }
    ydl = youtube_dl.YoutubeDL(opts)
    info = ydl.extract_info('https://www.youtube.com/watch?v=wPBbMbKSZrQ',download=False)
    return info.get('duration')

def LoadSongList():
    global currentSongList
    with open("rock.txt") as f:
        reader = csv.reader(f, delimiter="\t")
        currentSongList = list(reader)
    return currentSongList.__len__()

@client.event
async def on_ready():
    global voice
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    channel = client.get_channel('193910742322249728')
    if client.is_voice_connected(client.get_server('96063816692940800')) == False:
        voice = await client.join_voice_channel(channel)
    else:
        voice = client.voice_client_in(client.get_server('96063816692940800'))

@client.event
async def on_message(message):
    global currentSongList
    global voice
    if message.content.startswith("!startgame"):
        playerList = {}
        currentRound = 1
        await client.send_message(message.channel, 'Starting Game In 15 Seconds')

    if message.content.startswith('!register'):
        RegisterPlayer(message.author)
        await client.send_message(message.channel, 'User: {} Registered'.format(message.author))

    if message.content.startswith('!scores'):
        await client.send_message(message.channel, '{}'.format(PrintScores()))

    if message.content.startswith('!load'):
         numOfSongs = LoadSongList();
         randSongNum = randint(0,numOfSongs)
         SetSongArtist(currentSongList[randSongNum][0])
         SetSongName(currentSongList[randSongNum][1])
         song = "{} {}".format(GetCurrentSongArtist(), GetSongName())
         print("Song: {}".format(song))
         url = GetSongUrl(song)
         print("URL: {}".format(url))
         duration = GetAudioDuration(url)
         randStart = randint(0,duration/2)
         print('Random Start is {}'.format(randStart))
         kwargs = {"options":'-ss {}'.format(randStart)}
         player = await voice.create_ytdl_player(url, **kwargs)

         player.start()
         await asyncio.sleep(5)
         player.pause()


    if message.content.startswith('!find'):
        textToSearch = 'Michael Bolton How Am i supposed to live without you'
        query = urllib.parse.quote(textToSearch)

        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            print("https://www.youtube.com{}".format(vid['href']))


client.run('MjgzNDc5MDg1ODYxMTc1MzAw.C41tlQ.ceJFKwl4cGnTBohS2J4MZ3szKhw')