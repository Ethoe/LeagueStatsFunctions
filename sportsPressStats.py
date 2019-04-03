# Ryan Outtrim
# 4/3/19
# Functions that return a csv file with stats from given match
import csv
import urllib.request
import json
import requests
from collections import OrderedDict
from dataclasses import dataclass

@dataclass
class Player:
    name: str
    champNumber: int
    ID: int = 0
    kills: int = 0
    assists: int = 0
    deaths: int = 0
    gold: int = 0
    cs: int = 0
    dmgDealt: int = 0
    teamDmg: int = 0
    teamKills: int = 0
    playerScore: float = 0


def getTeam(filename):
    # Getting the current version number of data dragon
    naDDragonVersion = 'https://ddragon.leagueoflegends.com/realms/na.json'
    with urllib.request.urlopen(naDDragonVersion) as version:
        information = json.loads(version.read().decode())
        champVersion = information['n']['champion']

    # All of the champion names
    naDDragonChampion = 'http://ddragon.leagueoflegends.com/cdn/' + champVersion + '/data/en_US/champion.json'
    with urllib.request.urlopen(naDDragonChampion) as champions:
        information = json.loads(champions.read().decode())
        champions = information['data']

    players = OrderedDict()
    with open(filename, mode='r') as csvTeams:
        teams = csv.reader(csvTeams, delimiter=',')
        counter = 0
        for row in teams:
            if counter == 0:
                matchID = row[1]
                counter += 1
            else:
                champNumber = champions[row[1]]['key']
                players[row[0]] = champNumber

    return players, matchID


def statGatherer(players, matchID, apiKey):
    blueTeam = dict()
    redTeam = dict()
    counter = 0
    for player in players:
        if counter < 5:
            gamer = Player(name=player, champNumber=players[player])
            blueTeam[player] = gamer
        else:
            gamer = Player(name=player, champNumber=players[player])
            redTeam[player] = gamer
        counter += 1

    matchUrl = 'https://na1.api.riotgames.com/lol/match/v4/matches/' + matchID + '?api_key=' + apiKey
    request = requests.get(matchUrl)
    jsonData = request.json()
    blueDmg = 0
    redDmg = 0
    blueKills = 0
    redKills = 0
    for participant in range(10):
        champPlayed = int(jsonData['participants'][participant]['championId'])
        jsonPlayer = jsonData['participants'][participant]['stats']
        for user in blueTeam:
            gamer = blueTeam[user]
            if champPlayed is int(gamer.champNumber):
                gamer.ID = participant
                playerMaker(jsonPlayer, gamer)
                blueKills += gamer.kills
                blueDmg += gamer.dmgDealt
        for user in blueTeam:
            gamer = blueTeam[user]
            gamer.teamDmg = blueDmg
            gamer.teamKills = blueKills

        for user in redTeam:
            gamer = redTeam[user]
            if champPlayed == int(gamer.champNumber):
                gamer.ID = participant
                playerMaker(jsonPlayer, gamer)
                redKills += gamer.kills
                redDmg += gamer.dmgDealt
        for user in redTeam:
            gamer = redTeam[user]
            gamer.teamDmg = redDmg
            gamer.teamKills = redKills

    return blueTeam, redTeam


def playerMaker(jsonPlayer, gamer):
    score = 0
    gamer.kills = jsonPlayer['kills']
    gamer.deaths = jsonPlayer['deaths']
    gamer.assists = jsonPlayer['assists']
    gamer.gold = jsonPlayer['goldEarned']
    gamer.cs = jsonPlayer['neutralMinionsKilled'] + jsonPlayer['totalMinionsKilled']
    gamer.dmgDealt = jsonPlayer['totalDamageDealtToChampions']

    score += gamer.kills * 2
    score += gamer.deaths * -0.5
    score += gamer.assists * 1.5
    score += gamer.cs * 0.01
    score += jsonPlayer['tripleKills'] * 2
    score += jsonPlayer['quadraKills'] * 5
    score += jsonPlayer['pentaKills'] * 10
    if gamer.kills >= 10:
        score += 2
    if gamer.assists >= 10:
        score += 2

    gamer.playerScore = score
    return gamer


def csvReturn(blueTeam, redTeam):
    with open('playerStats.csv', mode='w') as csvFile:
        fields = ['Player Name', 'Kills', 'Deaths', 'Assists', 'Gold', 'CS', 'Damage Dealt', 'Player Score',
                  'Team Damage', 'Team Kills']
        writer = csv.DictWriter(csvFile, fieldnames=fields, delimiter=',', lineterminator='\n')
        writer.writeheader()
        for user in blueTeam:
            gamer = blueTeam[user]
            row = dict()
            row[fields[0]] = gamer.name
            row[fields[1]] = gamer.kills
            row[fields[2]] = gamer.deaths
            row[fields[3]] = gamer.assists
            row[fields[4]] = gamer.gold
            row[fields[5]] = gamer.cs
            row[fields[6]] = gamer.dmgDealt
            row[fields[7]] = gamer.playerScore
            row[fields[8]] = gamer.teamDmg
            row[fields[9]] = gamer.teamKills
            writer.writerow(row)
        for user in redTeam:
            gamer = redTeam[user]
            row = dict()
            row[fields[0]] = gamer.name
            row[fields[1]] = gamer.kills
            row[fields[2]] = gamer.deaths
            row[fields[3]] = gamer.assists
            row[fields[4]] = gamer.gold
            row[fields[5]] = gamer.cs
            row[fields[6]] = gamer.dmgDealt
            row[fields[7]] = gamer.playerScore
            row[fields[8]] = gamer.teamDmg
            row[fields[9]] = gamer.teamKills
            writer.writerow(row)
    return


def driver():
    apiKey = 'RGAPI-dd1500ad-117d-476a-9bca-51029a0ec6b8'
    game = getTeam("match.csv")
    stats = statGatherer(game[0], game[1], apiKey)
    csvReturn(stats[0], stats[1])
    print(stats[0])
    print('----------------------')
    print(stats[1])


driver()
