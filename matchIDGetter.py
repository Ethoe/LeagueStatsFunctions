import requests
import subprocess

def playerNameToID(player, api):
    playerUrl = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + player + '?api_key=' + api
    request = requests.get(playerUrl)
    jsonData = request.json()
    playerID = jsonData['id']

    matchUrl = 'https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/' + playerID + '?api_key=' + api
    request = requests.get(matchUrl)
    jsonData = request.json()
    return jsonData['gameId']

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def driver():
    apiKey = 'RGAPI-dd1500ad-117d-476a-9bca-51029a0ec6b8'
    while True:
        player = input("Enter players IGN: ")
        id = playerNameToID(player, apiKey)
        copy2clip(str(id))
        print(player + "'s current match ID was copied to clipboard")
        print("Match ID: " + str(id))


driver()
