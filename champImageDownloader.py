# Ryan Outtrim
# 3/24/19
# Function to get all of the champs as pictures and updates whenever it is run
import json
import urllib.request

# Getting the current version number of data dragon
naDDragonVersion = 'https://ddragon.leagueoflegends.com/realms/na.json'
with urllib.request.urlopen(naDDragonVersion) as version:
    information = json.loads(version.read().decode())
    champVersion = information['n']['champion']

# All of the champion names
naDDragonChampion = 'http://ddragon.leagueoflegends.com/cdn/' + champVersion + '/data/en_US/champion.json'
with urllib.request.urlopen(naDDragonChampion) as champions:
    information = json.loads(champions.read().decode())
    champions = information['data'].keys()

# Downloading all of the new champ squares
for champion in champions:
    naDDragonSquare = 'http://ddragon.leagueoflegends.com/cdn/' + champVersion + '/img/champion/' + champion + '.png'
    nnDDragonSplash = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + champion + '_0.jpg'
    urllib.request.urlretrieve(naDDragonSquare, 'ChampSquare/' + champion + '.png')
    urllib.request.urlretrieve(nnDDragonSplash, 'ChampSplash/' + champion + '.jpg')
    print('Saved image for ' + champion)

