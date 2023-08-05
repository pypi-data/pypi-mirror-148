"""
pydiceroller init
"""

from random import random
from pydiceroller.args import compute_args
import os
import random
import subprocess
from shutil import which
import re

DICE_EMOJI = "\U0001f3b2"

def pydiceroller():
    """
    pydiceroller entry point
    """
    #fix potential windows bug
    #colorama.init()
    os.sys.stdin.reconfigure(encoding='utf-8')
    os.sys.stdout.reconfigure(encoding='utf-8')
    if compute_args().update:
        update()
        exit()
    if not compute_args().dices:
        print("no dice given")    
        exit(1)

    for dice in compute_args().dices:
        if not re.match("^[1-9][0-9]*d[1-9][0-9]*$",dice.lower() ) and not re.match("^d?[1-9][0-9]*$",dice.lower() ) and not re.match("^s[1-9][0-9]*d[1-9][0-9]*$",dice.lower()) and not re.match("^[1-9][0-9]*s[1-9][0-9]*d[1-9][0-9]*$",dice.lower()):
            print("bad param, use --help to see correct syntax") 
            exit(1)

    while True:
        for dice in compute_args().dices:
            if re.match("^[1-9][0-9]*d[1-9][0-9]*$",dice.lower() ):
                number=dice.lower().split('d')[0]
                diceone=dice.lower().split('d')[1]
                for r in range(int(number)):
                    print(((DICE_EMOJI + diceone + " : ") if not compute_args().silent else "") + str(random.randint(1, int(diceone))))
            elif re.match("^d[1-9][0-9]*$",dice.lower() ):
                number=1
                diceone=dice[1:]
                for r in range(int(number)):
                    print(((DICE_EMOJI + diceone + " : ") if not compute_args().silent else "") + str(random.randint(1, int(diceone))))              
            elif re.match("^[1-9][0-9]*$",dice.lower() ):
                number=1
                diceone=dice
                for r in range(int(number)):
                    print(((DICE_EMOJI + diceone + " : ") if not compute_args().silent else "") + str(random.randint(1, int(diceone))))              

            elif re.match("^s[1-9][0-9]*d[1-9][0-9]*$",dice.lower() ):
                number=dice[1:].lower().split('d')[0]
                diceone=dice[1:].lower().split('d')[1]
                result=0
                for r in range(int(number)):
                    result=result+random.randint(1, int(diceone))
                print(((number + DICE_EMOJI + diceone + " : ") if not compute_args().silent else "")  + str(result)) 
            elif re.match("^[1-9][0-9]*s[1-9][0-9]*d[1-9][0-9]*$",dice.lower() ):
                numberdice=dice.lower().split('s')[0]
                dicee=dice.lower().split('s')[1]
                for r in range(int(numberdice)):
                    number=dicee.lower().split('d')[0]
                    diceone=dicee.lower().split('d')[1]
                    result=0
                    for r in range(int(number)):
                        result=result+random.randint(1, int(diceone))
                    print(((number + DICE_EMOJI + diceone + " : ") if not compute_args().silent else "")  + str(result))                    
        if compute_args().infinite:
            try:
                input("press any key to relaunch dices, ctrl-c to exit")
            except KeyboardInterrupt:
                break    
        else:
            break
def update():
    """
    entry point for --update
    """
    prog = "pip3"
    if (which("pip3")) is None:
        prog = "pip"
    params = [
        prog,
        "install",
        "--upgrade",
        "pydiceroller",
    ]
    subprocess.check_call(params)
   