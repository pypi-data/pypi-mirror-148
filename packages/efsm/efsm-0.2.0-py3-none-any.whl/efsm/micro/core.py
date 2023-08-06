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
    # example:
    add(s_idle)
    add('idle', 'move', fn = my_fn)


    :param state: [keynames, fn, data] or *names, fn=None
    :param fn: only available when len(state) > 1 which mean you want to instance a State in this add function.
    :param data: only available when len(state) > 1 which mean you want to instance a State in this add function.
    :return:
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
            list(_groups).remove(s)
            temp = _groups.pop(_s)
            if _s:
                _groups[_s] = temp
        elif error:
            raise TypeError("'x':" + str(s) + " not in statemachine")

def find(state):
    """
    寻找一个state
    :param state: keyname
    :return: (fn, data) or None
    """
    s = _find(state)

    if s is not None:
        return s[1], s[2]
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
    return state == end

def step():
    """
    步进
    :return: bool about statemachine is running-needy or not.
    """
    # step for itself
    global state, _prepare

    if state is None:
        state = start

    if _prepare:
        _prepare = False

    ''''''
    if state == end:
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

    add('idle', 'move', 'stop', fn=update)

    while not is_finish():
        step()

    print("finish.\n")
