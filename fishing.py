import minescript as m
from minescript import *
import time
import math
import random

THRESHOLD = 0.12
pulls = 0

def rc():
    m.player_press_use(True)
    time.sleep(random.uniform(0.001, 0.003))
    m.player_press_use(False)

def find_bobber():
    for e in m.entities():
        if "fishing_bobber" in e.type.lower():
            return e
    return None

def speed(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

while True:

    time.sleep(random.uniform(0.04, 0.11))

    rc()

    # wait for bobber to spawn
    start = time.time()
    bobber = None
    while time.time() - start < 8:
        bobber = find_bobber()
        if bobber:
            break
        time.sleep(0.05)

    if not bobber:
        continue

    #   ignore initial velocity
    time.sleep(random.uniform(1.2, 2.2))

    # wait for bobber to settle
    settle_deadline = time.time() + 0.7
    while time.time() < settle_deadline:
        bobber = find_bobber()
        if not bobber:
            break
        try:
            if speed(bobber.velocity) < THRESHOLD:
                break
        except:
            pass
        time.sleep(0.05)

    # wait for bite
    timeout = time.time() + 30
    while time.time() < timeout:
        bobber = find_bobber()
        if not bobber:
            break
        try:
            vy = bobber.velocity[1]

            if vy < -THRESHOLD:
                time.sleep(random.uniform(0.1, 0.16))

                rc()
                pulls += 1
                m.echo(str(pulls))
                
                # wait for bobber to despawn or break
                despawn_wait = time.time() + 0.6
                while time.time() < despawn_wait:
                    if find_bobber() is None:
                        break
                    time.sleep(0.05)

                time.sleep(random.uniform(0.08, 0.12))
                break
        except:
            pass
        time.sleep(random.uniform(0.025, 0.05))