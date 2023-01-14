import base64
from os import system
from colorama import Fore, Style
from psutil import process_iter
from requests import get
from urllib3 import disable_warnings, exceptions

def logo():
    eye = '''
░░░░░░░░░░░░░░░░░░░░░░ True sight ░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░▄▀░░▄▀░░▄▀░░▄▀░░░▄░▀▄█▀░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░█▄▄▄█▄▄█▄▄▄▀░░░░░▄▄██▀░▀░░░░░░░░░░
░░░░░░░░░░░░░░░░░░▄████▀██▀███████████▀░▄░▀░░░░░░░░░░░
░░░░░░░░░░░░░░░░▄█▀█░█████░█░▄████▀░░░▄░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░▄▀░░▀█▄▄▄▄▄▀░████▀▀▀▀█▄░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░▄▀░░░░▄▄▄▄▄▄▄██▀░░▀▀▄▄▄░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░▀▀▀▀▀▀░▀▀▀▀▀░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░▄██████▄▄▄░░░▄░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░▀░░░░░░░░░▀▀░▄▀░░░░░░░░░░░░░░░░░░░░░░░░░░
                                          -Ionian path
'''
    print(Fore.LIGHTRED_EX + eye + Style.RESET_ALL)

class Sight:
    region = None
    riot_auth_token = None
    riot_app_port = None
    riot_client_headers = None
    riot_client_api = None
    team = []

    def __init__(self):
        self.get_lcu_args()
        self.riot_client_api = 'https://127.0.0.1:' + self.riot_app_port
        self.session = base64.b64encode(('riot:' + self.riot_auth_token).encode('ascii')).decode('ascii')
        self.riot_client_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'LeagueOfLegendsClient',
            'Authorization': 'Basic ' + self.session
        }
        self.get_current_noobs()
        self.reveal_team()
    
    def get_lcu_args(self):
        for p in process_iter():
            if p.name() == 'LeagueClientUx.exe':
                args = p.cmdline()

                for a in args:
                    if '--region=' in a:
                        self.region = a.split('--region=', 1)[1].lower()
                    if '--riotclient-auth-token=' in a:
                        self.riot_auth_token = a.split('--riotclient-auth-token=', 1)[1]
                    if '--riotclient-app-port=' in a:
                        self.riot_app_port = a.split('--riotclient-app-port=', 1)[1]
    
    def opgg_url(self, team: list):
        str_team = '%2C'.join(team)
        return f'https://www.op.gg/multisearch/{self.region}?summoners={str_team}'

    def porofessor_url(self, team: list):
        str_team = ','.join(team)
        return f'https://porofessor.gg/pregame/{self.region}/{str_team}'

    def get_current_noobs(self):
        get_lobby = self.riot_client_api + '/chat/v5/participants/champ-select'
        lobby = get(get_lobby, headers=self.riot_client_headers, verify=False).json()
        for noob in lobby['participants']:
            self.team.append(noob['game_name'])
    
    def reveal_team(self):
        logo()
        print(Fore.LIGHTBLUE_EX)
        print(*self.team, sep=', ')
        print(Style.RESET_ALL + Fore.LIGHTCYAN_EX + self.opgg_url(self.team))
        print(self.porofessor_url(self.team), Style.RESET_ALL)


if __name__ == '__main__':
    system('cls')
    disable_warnings(exceptions.InsecureRequestWarning)
    client = Sight()
