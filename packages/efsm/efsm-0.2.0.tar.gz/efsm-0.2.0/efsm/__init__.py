# -*- coding: utf-8 -*-
from efsm.standard.core import *
import efsm.micro.core as micro


"""
# to use this. you need to create a StateMachine and add some State to it.
# this could use in micropython and very efficient

use this to create self:
self = StateMachine(start, end=None, on_end=None)

use this to create State
State(*keynames, fn=None, data=None)

# example 1:    # single statemachine
def update(state, data):
    match state:
        case 'idle':
            print("i'm idle, next to move")
            return "move"
        case 'move':
            print("i'm moving, next to stop")
            return "stop"
    return 'stop'


sm1 = StateMachine('idle', 'stop')

sm1.add('idle', 'move', 'stop', fn=update)

while sm1:
    print(sm1, '\n\t', end="")
    sm1.step()
    print()

print("finish.")


# you could link them to a sm net, by using:
sm.link(state, target, target_state)

# example 2:    # link as net
    def update(state, *a):
        match state:
            case 'idle':
                print("i'm idle, next to move")
                return "move"
            case 'move':
                print("i'm moving, next to stop")
                return "stop"
        return 'stop'


    sm1 = StateMachine('idle', 'stop')
    sm2 = StateMachine('idle', 'stop')  # all same with sm1

    sm1.add('idle', 'move', 'stop', fn=update)
    sm2.add('idle', 'move', 'stop', fn=update)

    sm1.link('stop', sm2, 'idle')

    while sm1:
        print(sm1, '\n\t', end="")
        sm1.step()
        print()


    print("finish.")


"""