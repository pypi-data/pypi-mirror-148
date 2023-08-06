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

while True:
    init(autoreset=True)#без этого не работают цвета на винде

    print("list command  you gay((( uwu \nOptions:\n"
				    "\t(s) stats all servers\n"
                    "\t(s -all) viev all info\n"                  #это инфа 
				    "\t(s -n server) you server info\n"
                    "\texit\n"
				    "\t(s -n -all server) you server all info\n")


    servertest = input('->') # штука для красивого импута реально прикольно да?

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



    
    def sall(ip):
        txt = 'https://api.mcsrvstat.us/2/server'
        aboba = txt.replace("server", ip)




    # это тоже саоме что и s но выдает доп инфу
        resp = requests.get(aboba)
        resp = json.loads(resp.text)
        good = resp['online']


        if good == True:
            server_stats = 1
        else:
            server_stats = 0

        try:
            gay = str(resp['players']['online'])
        except:
            gay = str(('0'))
        skolko_geev = len(gay)
        print(Back.WHITE + Fore.BLACK + '   ', end = '')
        print(Back.WHITE + Fore.BLACK + ip, end = '')
        skolko_geev_up = '         '
        print(Fore.BLACK + '                                                                                                    ', 'players =', gay, end='')
        if skolko_geev == 1:
            print('           ', end = '')
        if skolko_geev == 2:
            print('          ', end = '')
        if skolko_geev == 3:
            print('         ', end = '')
        if skolko_geev == 4:
            print('        ', end = '')
        if skolko_geev == 5:
            print('       ', end = '')

        if server_stats == 1:
            print(Fore.BLUE + '[ UP ]')

        else:
            print(Fore.RED + '[DOWN]')

    def sn(server):
        servername = server.replace("s -n ", "")

        txt = 'https://api.mcsrvstat.us/2/server'
        aboba = txt.replace("server", servername)
        resp = requests.get(aboba)
        resp = json.loads(resp.text)
        good = resp['online']

        if good == True:
            server_stats = 1
        else:
            server_stats = 0

    # тут тоже самое что и snpro но без всех доп функций

        print(Back.WHITE + '   ', end = '')
        print(Back.WHITE + Fore.BLACK + servername, end = '')
        print(Fore.BLACK + '                                                                                                                           ', end = '')

        if server_stats == 1:
            print(Fore.GREEN + '[ UP ]')

        else:
            print(Fore.RED + ' [DOWN]')


    def snpro(server): #ооо это какая то хрень ладно это вся информация о сервере который ты выбрал
        servername = server.replace("s -n -all", "")# тут удаляется тег

        txt = 'https://api.mcsrvstat.us/2/server'
        aboba = txt.replace("server", servername)#тут заменятся в переменной txt  server на названия сервера который выбрали

        resp = requests.get(aboba)
        resp = json.loads(resp.text)# тут узнается онлайн он или нет
        good = resp['online']

        if good == True:
            server_stats = 1 # тут узнается онлайн он или нет
        else:
            server_stats = 0


        try:
            gay = str(resp['players']['online'])# тут узнается сколько игроков на сервере
        except:
            gay = str(('0'))# если ошибка то ноль игроков, логично?


        skolko_geev = len(gay) #моя любимая чась и так тут узнается сколько символов в числе игроков

        skolko_geev_up = '         ' # и так эта часть кода если игроков 123 то текст [ OK ] сдвигается а это преддотвращает это
        print(Back.WHITE + '  ', end ='')
        print(Back.WHITE + Fore.BLACK + servername, end='')
        print(Fore.BLACK + '                                                                                ', 'players =',gay, end='')
        if skolko_geev == 1:
            print('           ', end='')
        if skolko_geev == 2:
            print('          ', end='')
        if skolko_geev == 3:
            print('         ', end='')
        if skolko_geev == 4:
            print('        ', end='')
        if skolko_geev == 5:
            print('       ', end='')


        if server_stats == 1:
            print(Fore.GREEN + ' [ UP ]')

        else:
            print(Fore.RED + ' [DOWN]')





    if 's -n -all' in servertest:
        snpro(servertest)

    elif 's -n' in servertest:
        sn(servertest)

    elif 's -all' in servertest:
        sall('play.vanilla-mc.xyz')
        sall('vanilla.makotomc.ru')
        sall('    seven-lights.ru')
        sall('           2b2t.org')
        sall('    12.pepeland.net')
    elif 's' in servertest:
        s('play.vanilla-mc.xyz')
        s('vanilla.makotomc.ru')
        s('    seven-lights.ru')
        s('           2b2t.org')
        s('    12.pepeland.net')
    elif 'exit' in servertest:
        sys.exit()













