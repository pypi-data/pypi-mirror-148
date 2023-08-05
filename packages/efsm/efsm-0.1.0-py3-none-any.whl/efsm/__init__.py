# -*- coding: utf-8 -*-
from efsm.core import StateMachine, State
"""
# to use this. you need to create a StateMachine and add some State to it.
# this could use in micropython and very efficient

use this to create sm:
sm = StateMachine(start, end=None, on_end=None)

use this to create State
State(*keynames, fn=None, data=None)

# example:
def update(state, data):
    match state:
        case 'idle':
            print("i'm idle, next to move")
            return "move"
        case 'move':
            print("i'm moving, next to stop")
            return "stop"
    return 'stop'


sm = StateMachine('idle', 'stop')

sm.add('idle', 'move', 'stop', fn=update)

while sm:
    sm.step()

print("finish.")


"""