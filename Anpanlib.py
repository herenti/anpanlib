import time
import urllib.request
import urllib.parse
import random
import re
import select
import socket
import threading

"""
ANPANLIB
SPARKING THE ANPAN
BY HERENTI
"""


def regex(pattern, x, default): return re.search(pattern, x).group(1) if re.search(pattern, x) else default


def Auth(user, password):
    data = urllib.parse.urlencode({"user_id": user, "password": password, "storecookie": "on", "checkerrors": "yes"}).encode()
    return regex('auth.chatango.com=(.*?);', urllib.request.urlopen("http://chatango.com/login", data).getheader('Set-Cookie'), None)



manager = dict()


#CHAT STUFF


def chat_login(chat, username, password):
        chat_port = 443
        chat_server = server(chat)
        chat_id = str(random.randrange(10**15, 10**16))
        cumsock = socket.socket()
        cumsock.connect((chat_server, chat_port))
        manager["chat_sockets"][chat] = cumsock
        manager["chat_ready"] = "T"
        manager["chats_wbyte"][chat]= b''
        timer(30, chat_ping, chat)
        chat_send(chat, 'bauth', chat, chat_id, username, password)
        manager["chat_ready"] = "F"
        print("logged into "+chat)


def chat_send(chat, *x):
        data = ':'.join(x).encode()
        byte = b'\x00' if manager["chat_ready"] == "T" else b'\r\n\x00'
        manager["chats_wbyte"][chat] += data+byte

def chat_ping(chat):
        chat_send(chat, "")



#PM STUFF


pm_server = 'c1.chatango.com'
pm_port = 5222

def pm_login(username, password):
        manager["pm_ready"] = "T"
        cumsock = socket.socket()
        cumsock.connect((pm_server, pm_port))
        manager["pm_socket"] = cumsock
        manager["pm_wbyte"] = b''
        auth = Auth(username, password)
        timer(30, pm_ping)
        pm_send('tlogin', auth, '2')
        manager["pm_ready"] = "F"


def pm_send(*x):
        data = ':'.join(x).encode()
        byte = b'\x00' if manager["pm_ready"] == "T" else b'\r\n\x00'
        manager["pm_wbyte"] += data+byte


def pm_ping():
        pm_send("")


#UNIVERSAL

def timer(seconds, function, *var):
        event = threading.Event()
        def decorator(*var):
            while not event.wait(seconds): function(*var)
        threading.Thread(target = decorator, args = (var), daemon = True).start()
        manager["tasks"].append(event)
        return event

def bootup(username, password, chats):
  manager["tasks"] = []
  manager["chat_sockets"] = {}
  manager["chats_wbyte"] = {}
  pm_login(username, password)
  for i in chats:
    chat_login(i, username, password)
  lemonize()

def lemonize():
  manager["cake"] = "T"
  read_byte = b''
  while manager["cake"] == "T":
        manager["sendoff"] = {}
        connections = list(manager["chat_sockets"].values())
        connections.append(manager["pm_socket"])

        for i in manager["chats_wbyte"]:
                if manager["chats_wbyte"][i] != b'':
                        manager["sendoff"][manager["chat_sockets"][i]] = [i, manager["chats_wbyte"][i]]

        write_sock = list(manager["sendoff"].keys())


        if manager["pm_wbyte"] != b'':
                write_sock.append(manager["pm_socket"])
                manager["sendoff"][manager["pm_socket"]] = ["pm", manager["pm_wbyte"]]

        r, w, e = select.select(connections, write_sock, [], 0.05)

        for i in r:
                while not read_byte.endswith(b'\x00'):
                        read_byte += i.recv(1024)
                print(read_byte)
                read_byte = b''
        for i in w:
                content = manager["sendoff"][i][1]
                _type = manager["sendoff"][i][0]
                i.send(content)
                if _type == "pm":
                        manager["pm_wbyte"] = b''
                else:
                        manager["chats_wbyte"][_type] = b''



def server(group):
    try:  s_number = str(specials[group])
    except KeyError:
        group = re.sub('[-_]', 'q', group)
        lcv8 = max(int(group[6:9], 36), 1000) if len(group) > 6  else 1000
        num = (int(group[:5], 36) % lcv8) / lcv8
        cake, s_number = 0, 0
        for x in tagserver_weights:
          cake += float(x[1]) / sum(a[1] for a in tagserver_weights)
          if(num <= cake) and s_number == 0:
            s_number += int(x[0])
    return "s{}.chatango.com".format(s_number)

#def pm_ping():

#WEIGHTS

w12 = 75
sv2 = 95
sv4 = 110
sv6 = 104
sv8 = 101
sv10 = 110
sv12 = 116

tagserver_weights = [["5", w12], ["6", w12], ["7", w12], ["8", w12], ["16", w12], ["17", w12], ["18", w12], ["9", sv2], ["11", sv2], ["12", sv2], ["13", sv2], ["14", sv2], ["15", sv2], ["19", sv4], ["23", sv4], ["24", sv4], ["25", sv4], ["26", sv4], ["28", sv6], ["29", sv6], ["30", sv6], ["31", sv6], ["32", sv6], ["33", sv6], ["35", sv8], ["36", sv8], ["37", sv8], ["38", sv8], ["39", sv8], ["40", sv8], ["41", sv8], ["42", sv8], ["43", sv8], ["44", sv8], ["45", sv8], ["46", sv8], ["47", sv8], ["48", sv8], ["49", sv8], ["50", sv8], ["52", sv10], ["53", sv10], ["55", sv10], ["57", sv10], ["58", sv10], ["59", sv10], ["60", sv10], ["61", sv10], ["62", sv10], ["63", sv10], ["64", sv10], ["65", sv10], ["66", sv10], ["68", sv2], ["71", sv12], ["72", sv12], ["73", sv12], ["74", sv12], ["75", sv12], ["76", sv12], ["77", sv12], ["78", sv12], ["79", sv12], ["80", sv12], ["81", sv12], ["82", sv12], ["83", sv12], ["84", sv12]]

specials = {'mitvcanal': 56, 'magicc666': 22, 'livenfree': 18, 'eplsiite': 56, 'soccerjumbo2': 21, 'bguk': 22, 'animachat20': 34, 'pokemonepisodeorg': 55, 'sport24lt': 56, 'mywowpinoy': 5, 'phnoytalk': 21, 'flowhot-chat-online': 12, 'watchanimeonn': 26, 'cricvid-hitcric-': 51, 'fullsportshd2': 18, 'chia-anime': 12, 'narutochatt': 52, 'ttvsports': 56, 'futboldirectochat': 22, 'portalsports': 18, 'stream2watch3': 56, 'proudlypinoychat': 51, 'ver-anime': 34, 'iluvpinas': 53, 'vipstand': 21, 'eafangames': 56, 'worldfootballusch2': 18, 'soccerjumbo': 21, 'myfoxdfw': 22, 'animelinkz': 20, 'rgsmotrisport': 51, 'bateriafina-8': 8, 'as-chatroom': 10, 'dbzepisodeorg': 12, 'tvanimefreak': 54, 'watch-dragonball': 19, 'narutowire': 10, 'leeplarp': 27}





bootup("", "", [""])
