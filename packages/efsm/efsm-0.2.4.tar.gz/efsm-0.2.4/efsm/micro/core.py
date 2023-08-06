# -*- coding: utf-8 -*-
import sys
_statemachine = sys.modules[__name__]

class Local:
    ...

start = None
state = None
end = None

#  fn(this_module)->None Evey this statemachine step finish, python will auto call it.
on_step = None
#  fn(this_module)->None Once state is run to end, python will auto call it.
on_end = None

_prepare = True
_groups = {}


def _find(groups, name):
    """
    获取对应的state
    :param groups:
    :param name:
    :return:
    """
    for k in groups:
        if name in k:
            return [k] + groups[k]
    return None

def tolist():
    """
    change _groups to list
    :return: [[(*state), fn, data], ...]
    """
    return [[k] + v for k, v in _groups.items()]

def restart():
    global start, state, end, on_step, on_end, _prepare, _groups
    start = None
    state = None
    end = None

    on_step = None
    on_end = None

    _prepare = True
    _groups = {}


def add(*states, fn=None, data=None):
    """
    add a smallest unit to your statemachine

    # example:
    .add('idle', 'move', fn = my_fn)

    :param *state: include some states as a group.
    :param fn: then assign a proccessing function to only handle this group of states
            _: None  Note that this is a must param. If you do not pass fn
    :param data: the 'o' offer to your proccessing function
            _: None  Mean it will create a empty object instance for this smallest unit.
    :return: list[tuple[*state], fn, data]
    """

    states = [states, fn, Local() if data is None else data]

    _groups[states[0]] = states[1:]


def remove(*state, error=True):
    """
    移除某种状态
    # example
    .remove('idle')
    .remove('idle', 'move')

    :param state: [state:keyname, ...]
    :param error: bool If not find, will raise error
    :return:
    """
    for s in state:
        _s = _find(_groups, s)

        if _s is not None:
            _s = _s[0]
            temp = _groups.pop(_s)
            _s = list(_s)
            _s.remove(s)
            _s = tuple(_s)
            if _s:
                _groups[_s] = temp
        elif error:
            raise TypeError("'x':" + str(s) + " not in statemachine")

def find(state):
    """
    find the smallest unit corresponding to a state
    :param state: fsm find the state, and return the smallest unit
    :return: [states, fn, data] or None
    """
    s = _find(state)

    if s is not None:
        return s
    else:
        return None

def list_():
    """
    展示所有的state
    :return: {state: (fn, data)}
    """
    states = {}
    for k in _groups:
        for name in k:
            states[name] = _groups[k]
    return states

def is_finish():
    """
    get whether the fsm is finish.
    :return: bool
    """
    return state == end

def step():
    """
    step, mean update once
    :return: bool about statemachine is running-needy or not.
    """
    # step for itself
    global state, _prepare

    if state is None:
        state = start

    if _prepare:
        _prepare = False

    ''''''
    if end is not None and state == end:
        return False

    _state = _find(_groups, state)
    assert _state is not None, "can not find state:" + str(state) + ". Please check whether you add this state before."

    _state = _state[1](state, _state[2])
    # assert _state is not None, "fn of state:" + str(state) + " need return a state name but get None."

    state = _state
    ''''''

    # try on_step
    if on_step:
        on_step(_statemachine)

    # check if end
    if end is not None and _state == end:
        if on_end: on_end(_statemachine)
        return False

    return True

def is_prepare():
    """
    get whether the fsm is steped.
    :return: bool
    """
    return _prepare


if __name__ == '__main__':
    restart()
    print("example for micro: ")


    def update(state, data):
        match state:
            case 'idle':
                print("i'm idle, next to move")
                return "move"
            case 'move':
                print("i'm moving, next to stop")
                return "stop"
        return 'stop'

    start, end = 'idle', 'stop'

    add('idle', 'move', 'stop', 'a', fn=update)
    print(list_())
    remove("a")
    print(list_())

    while not is_finish():
        step()

    print("finish.\n")
