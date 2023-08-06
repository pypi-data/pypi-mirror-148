from colorama import init, Fore
from mcstatus import JavaServer
from geoip import geolite2
from colorama import Style
from colorama import Back       #импортс
from ping3 import ping
from time import sleep
import requests
import json
import urllib.request
import os
import sys



def s(ip):
        txt = 'https://api.mcsrvstat.us/2/server'
        aboba = txt.replace("server", ip)
        resp = requests.get(aboba)
        resp = json.loads(resp.text)
        good = resp['online']

        if good == True:
            server_stats = 1
        else:
            server_stats = 0

                                                                # тут тоже самое что и sn но выдаёт записаные в код сервера
        print(Back.WHITE + Fore.BLACK + '   ' + ip, end='')
        print(Fore.BLACK + '                                                                                                                          ', end='')


        if server_stats == 1:
            print(Fore.BLUE + ' [ UP ]')

        else:
            print(Fore.RED + ' [DOWN]')
