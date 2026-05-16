#run and pray
import random
import threading
from unittest.result import failfast
import winsound
from minescript import (echo, player, player_press_left, player_press_right, player_press_attack, execute)
import sys
import time
import http.client, urllib

                        #defining most var
a = 0
Running = True
sneak = False
x, y, z = (0, 0, 0,)
yaw, pitch = (0, 0,)
Right = True
Left = not Right
player_data = {}
dx = 0
dy = 0
dz = 0
dp = 0
dyw = 0
p = player()

def getpos():       # Get Position
    global x, y, z, p
    p = player()
    x, y, z = [round(pos) for pos in p.position]

def send_noti(message):                                         #fucking AI bs (sends the message to ur phone)
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": "araouvqe3xtw8nofba59j2h9mpx99r",
        "user": "ureg3s59ketjgd5w97w3oa785e29dx",
        "message": message,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()


def getori():                      # Get Orientation
    global yaw, pitch
    try:
        yaw = round(p.yaw)
        pitch = round(p.pitch)
    except AttributeError:
        yaw, pitch = round(p.look)

def dictionary(n):
    global x, y, z, yaw, pitch
    player_data[n] = {             #dictionary type shit (stores info about our current state)
        "pos": (x, y, z),
        "rot": (yaw, pitch)
    }

def ring_bell():
    winsound.Beep(300, 400)  # frequency, duration
    winsound.Beep(800, 400)

def alert():                    #you aren't retarded this is self explanitory
    send_noti("Macro detected ⚠️")
    echo(f"{dy,dz}")
    ring_bell()
    ring_bell()
    ring_bell()

def calc():             #calc change in axis (calc is short for calculate)
    global dx, dy, dz
    dx = player_data[1]["pos"][0] - player_data[0]["pos"][0]
    dy = player_data[1]["pos"][1] - player_data[0]["pos"][1]
    dz = player_data[1]["pos"][2] - player_data[0]["pos"][2]

def calc2():            #calc change in pitch/yaw
    global dyw, dp
    dyw = player_data[1]["rot"][0] - player_data[0]["rot"][0]
    dp = player_data[1]["rot"][1] - player_data[0]["rot"][1]

# actuall macro functions

def leftclick(Bool):
    player_press_attack(Bool)

def MovementR(Bool, Time): #Left/Right

    time.sleep(0.1)
    end_time = time.time() + Time + random.random()
    player_press_right(Bool)
    while time.time() < end_time:
        time.sleep(0.01)
    player_press_right(not Bool)
    time.sleep(0.1)



def MovementL(Bool, Time):
    end_time = time.time() + Time + random.random()
    player_press_left(Bool)
    while time.time() < end_time:
        time.sleep(0.01)
    player_press_left(not Bool)
    time.sleep(0.1)

def FarmMove():
    MovementL(True, 119.5)
    MovementR(True, 119.5)
    MovementL(True, 119.5)
    MovementR(True, 119.5)
    MovementL(True, 119.5)

def Failsafe():

    getpos()
    getori()        #initialize the first position before loop
    dictionary(0)

    while True:
        time.sleep(1.7)
        getpos()
        getori()
        dictionary(1)
        calc()
        calc2()
        if ((((dx >= 0 and dx < 1) and (abs(dz) >= 3 and abs(dz) <= 5) and (0 <= dy <= 3)) or ((dx >= 0 and dx < 1) and (abs(dz) >= 6 and abs(dz) <= 8) and (0 <= abs(dy) <= 3))) and (dyw ==0 and dp == 0) or (abs(dz) <= 478 and abs(dz) >= 473)):
            player_data[0] = player_data[1]

        elif (1 <= abs(dy) and abs(dy) <= 3):            # for part where we go down in farm
            player_data[0] = player_data[1]
            continue

        else:
            alert()
            player_data[0] = player_data[1]

            break
    sys.exit()


def macro():        #puts all movement and clicking together and loops for an hour ish (until I figure out how to extract scoreboard information for pests)
    global a, running
    while a < 2:
        a += 1
        leftclick(True)
        FarmMove()
        time.sleep(0.001)
        execute("/warp garden")
        time.sleep(0.001)
    leftclick(False)
    execute("/warp garden")

thread_a = threading.Thread(target=macro, daemon=True)
thread_b = threading.Thread(target=Failsafe, daemon=True)
thread_a.start()
thread_b.start()
thread_b.join()