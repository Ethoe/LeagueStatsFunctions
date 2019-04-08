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
            elif counter == 1:
                date = row[1]
                counter += 1
            elif counter == 2:
                time = row[1]
                counter += 1
            elif counter == 3:
                blueTeamName = row[1]
                if row[0] == str('Home'):
                    home = True
                counter += 1
            elif counter == 4:
                redTeamName = row[1]
                if row[0] == str('Home'):
                    home = False
                counter += 1
            else:
                champNumber = champions[row[1]]['key']
                players[row[0]] = champNumber

    return players, matchID, date, time, blueTeamName, redTeamName, home


def statGatherer(players, matchID, apiKey):
    blueTeam = dict()
    redTeam = dict()
    blueStat = [0, 0, 0, 0, 0]
    redStat = [0, 0, 0, 0, 0]
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

    for participant in range(10):
        champPlayed = int(jsonData['participants'][participant]['championId'])
        jsonPlayer = jsonData['participants'][participant]['stats']
        for user in blueTeam:
            gamer = blueTeam[user]
            if champPlayed is int(gamer.champNumber):
                gamer.ID = participant
                playerMaker(jsonPlayer, gamer)
                blueStat[0] += gamer.dmgDealt
                blueStat[1] += gamer.kills
                blueStat[2] += gamer.deaths
                blueStat[3] += gamer.assists
                blueStat[4] += gamer.gold

        for user in redTeam:
            gamer = redTeam[user]
            if champPlayed == int(gamer.champNumber):
                gamer.ID = participant
                playerMaker(jsonPlayer, gamer)
                redStat[0] += gamer.dmgDealt
                redStat[1] += gamer.kills
                redStat[2] += gamer.deaths
                redStat[3] += gamer.assists
                redStat[4] += gamer.gold

    blueWin = jsonData['teams'][0]['win']
    return blueTeam, redTeam, blueWin, blueStat, redStat


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


def resultMaker(totalDmg, totalKills, totalDeaths, totalAssists, totalGold, winLoss):
    if winLoss == 'Win':
        string = "W"
    else:
        string = "L"
    return ' | '.join([string, str(totalDmg), str(totalKills), str(totalDeaths), str(totalAssists), str(totalGold)])


def csvReturn(blueTeam, redTeam, date, time, blueTeamName, redTeamName, firstWin, blueStat, redStat):
    with open('match.csv', mode='w') as csvFile:
        fields = ['Date', 'Time', 'Venue', 'Teams', 'Results', 'Outcome',
                  'Players', 'CS', 'Damage Dealt', 'Kills', 'Deaths', 'Assists', 'Gold']

        writer = csv.DictWriter(csvFile, fieldnames=fields, delimiter=',', lineterminator='\n')
        writer.writeheader()

        if firstWin:
            teamOne = 'Win'
            teamTwo = 'Loss'
        else:
            teamOne = 'Loss'
            teamTwo = 'Win'

        counter = 0
        for user in blueTeam:
            gamer = blueTeam[user]
            if counter == 0:
                result = resultMaker(blueStat[0], blueStat[1], blueStat[2], blueStat[3], blueStat[4], teamOne)
                writer.writerow({fields[0]: date, fields[1]: time, fields[2]: 'Online', fields[3]: blueTeamName,
                                 fields[4]: result, fields[5]: teamOne, fields[6]: gamer.name,
                                 fields[7]: gamer.cs, fields[8]: gamer.dmgDealt, fields[9]: gamer.kills,
                                 fields[10]: gamer.deaths, fields[11]: gamer.assists, fields[12]: gamer.gold})
                counter += 1
            else:
                writer.writerow({fields[6]: gamer.name, fields[7]: gamer.cs, fields[8]: gamer.dmgDealt,
                                 fields[9]: gamer.kills, fields[10]: gamer.deaths, fields[11]: gamer.assists,
                                 fields[12]: gamer.gold})

        counter = 0
        for user in redTeam:
            gamer = redTeam[user]
            if counter == 0:
                result = resultMaker(redStat[0], redStat[1], redStat[2], redStat[3], redStat[4], teamTwo)
                writer.writerow({fields[3]: redTeamName, fields[4]: result, fields[5]: teamTwo,
                                 fields[6]: gamer.name, fields[7]: gamer.cs, fields[8]: gamer.dmgDealt,
                                 fields[9]: gamer.kills, fields[10]: gamer.deaths, fields[11]: gamer.assists,
                                 fields[12]: gamer.gold})
                counter += 1
            else:
                writer.writerow({fields[6]: gamer.name, fields[7]: gamer.cs, fields[8]: gamer.dmgDealt,
                                 fields[9]: gamer.kills, fields[10]: gamer.deaths, fields[11]: gamer.assists,
                                 fields[12]: gamer.gold})

    return


def driver():
    apiKey = 'RGAPI-dd1500ad-117d-476a-9bca-51029a0ec6b8'
    game = getTeam("inputMatch.csv")
    stats = statGatherer(game[0], game[1], apiKey)
    if game[6]:
        if stats[2] == 'Win':
            csvReturn(stats[0], stats[1], game[2], game[3], game[4], game[5], True, stats[3], stats[4])
        else:
            csvReturn(stats[0], stats[1], game[2], game[3], game[4], game[5], False, stats[3], stats[4])
    else:
        if stats[2] == 'Win':
            csvReturn(stats[1], stats[0], game[2], game[3], game[5], game[4], False, stats[4], stats[3])
        else:
            csvReturn(stats[1], stats[0], game[2], game[3], game[5], game[4], True, stats[4], stats[3])


driver()
