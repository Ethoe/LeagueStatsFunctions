import requests

page = requests.get("https://127.0.0.1:63688/lol-champ-select/v1/session",
                    auth=('riot', 'O_8TXT-F0dAR28veAsSvRQ'),
                    verify=False)
print(str(page.content.decode()))
