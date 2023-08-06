# -*- coding: utf-8 -*-

class Local:
    ...


class StateSet:
    """
    定义了一组state，这些state共用一个二段式的函数
    """

    def __new__(cls, *names, fn=None, data=None):
        assert fn is not None, "param 'fn' need a function like fn(state, d)->state but get None."

        return [names, fn, Local() if data is None else data]


class StateMachineBase:
    _raw_id = 0

    @property
    def _id(self):
        StateMachineBase._raw_id += 1
        return StateMachineBase._raw_id - 1

    def __init__(self, start, end=None, on_step=None, on_end=None, name=None):
        """
        new a statemachine
        :param start: start state name
        :param end: end state name
                _ = None
        :param on_step: fn(statemachine)->None Evey this statemachine step finish, python will auto call it.
                _ = None
        :param on_end: fn(statemachine)->None Once state is run to end, python will auto call it.
                _ = None
        :param name: does not important. only for showcase.
                _ = None   mean use auto name
        Attribute start without '_' is explosure to outer:
            .start
            .state
            .end
            .on_step
            .on_end
            .links      # {state: [statemachine, to_state]}
            .add(...)
            .remove(...)
            .find(...)
            .list(...)
            .link(...)
            .broke(...)
            .step(...)
            .tolist(...)

        """
        # inner attr
        self.name = name if name is not None else ("StateMachine" + str(self._id))
        self._prepare = True

        # 指示部分
        self.start = start  # 指示状态机入口， 是一个keyname
        self.state = self.start  # 指示状态机当前状态， 是一个keyname
        self.end = end  # 指示状态机出口， 是一个keyname
        self.on_step = on_step
        self.on_end = on_end

        # 数据部分
        self._groups = {}  # {(names, ...): [fn, data]}

        # net部分
        self._target = None
        self.links = {}  # {name: [statemachine, to_state]}

    def tolist(self):
        """
        change statemachine._groups to list
        :param self:
        :return: [[(names), fn, data], ...]
        """
        return [[k] + v for k, v in self._groups.items()]

    @staticmethod
    def _redirect(self, state):
        """
        get the target to other efsm
        :return:
        """
        if state is not None: self.state = state  # redirect efsm.state to state
        get, to = self.links.get(state, (None, None))
        if get is not None:
            get_ = StateMachineBase._redirect(get, to)
            if get_ is None:
                return get
            else:
                return get_
        else:
            return None

    @staticmethod
    def _standard(*state, fn=None, data=None):
        """
        标准化
        :param state: [names, fn, data] or *names, fn=None
        :param fn: only available when len(state) > 1 which mean you want to instance a StateSet in this add function.
        :param data: only available when len(state) > 1 which mean you want to instance a StateSet in this add function.
        :return:
        """
        assert state, "get empty state."
        # print("std_std", state, fn, data)
        if fn is None:
            assert len(state) == 1, "you can pass in only a state at once, but get " + str(state)
            state = state[0]
            assert len(state) == 3, "unexpected state to get " + str(state)
        else:
            state = StateSet(*state, fn=fn, data=data)
        return state

    @staticmethod
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

    def __iter__(self):
        return iter(self._groups)

    def __getitem__(self, item):
        return StateMachineBase._find(self._groups, item)

    def __bool__(self):
        if self.state is None and self.start != None:
            self.state = self.start
        return self.state != self.end if self._target is None else bool(self._target)

    def __str__(self):
        txt = self.name
        if self._target is not None:
            txt += " -> " + str(self._target)
        else:
            txt += ":" + str(self.state) + " - " + ("running" if self else "finish")

        return txt


class StateMachine(StateMachineBase):
    def add(self, *state, fn=None, data=None) -> list:
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

        state = StateMachine._standard(*state, fn=fn, data=data)

        self._groups[state[0]] = state[1:]
        return state

    def remove(self, *state, error=True) -> None:
        """
        remove a state.
        It won't remove the hole group states but only remove the state from the group states
        The smallest unit will be remove only after all of it's group states all being removed.
        # example
        .remove('idle')
        .remove('idle', 'move')

        :param *state: fsm will remove them one by one.
        :param error: bool If not find, will raise error
        :return: None
        """
        for s in state:
            _s = StateMachine._find(self._groups, s)

            if _s is not None:
                _s = _s[0]
                temp = self._groups.pop(_s)
                _s = list(_s)
                _s.remove(s)
                _s = tuple(_s)
                if _s:
                    self._groups[_s] = temp
            elif error:
                raise TypeError("'x':" + str(s) + " not in statemachine")

    def find(self, state):
        """
        find the smallest unit corresponding to a state
        :param state: fsm find the state, and return the smallest unit
        :return: [states, fn, data] or None
        """
        s = StateMachine._find(self._groups, state)

        if s is not None:
            return s
        else:
            return None

    def list(self):
        """
        showcase state
        Note: it do not return list but dict
        :return: {state: (fn, data)}
        """
        states = {}
        for k in self._groups:
            for name in k:
                states[name] = self._groups[k]
        return states

    def link(self, state, target: StateMachineBase, target_state=None):
        """
        redirect statemachine when statemachine step with this spec state

        linked state will check before itself step.
        :param state: state in this state machine which you want to redirect
        :param target: target state machine
        :param target_state: target's state.
                _ = None    mean only redirect to target without change target.state
        :return:
        """
        self.links[state] = [target, target_state]

    def broke(self, state) -> bool:
        """
        break the state link. return true if successful(if link exist) or False
        :param state:
        :return: bool
        """
        if self.links.pop(state, None) is not None:
            return True
        else:
            return False

    def step(self):
        """
        步进
        :return: bool about statemachine is running-needy or not.
        """

        if self._prepare:
            self._prepare = False

        if self.state is None:
            self.state = self.start

        # try to retarget
        if self._target:
            return self._target.step()

        # step for itself
        ''''''
        if self.end is not None and self.state == self.end:
            return False

        state = StateMachine._find(self._groups, self.state)
        assert state is not None, "can not find state:" + str(self.state) + ". Please check whether you add this state before."

        state = state[1](self.state, state[2])
        # assert state is not None, "fn of state:" + str(efsm.state) + " need return a state name but get None."

        self.state = state
        ''''''

        # update target
        self._target = StateMachine._redirect(self, self.state)

        # try on_step
        if self.on_step:
            self.on_step(self)

        # check if end
        if state == self.end and self.end is not None:
            if self.on_end: self.on_end(self)
            return bool(self)

        return True

    def is_finish(self):
        """
        check whether it on end.
        If this statemachine has target, will check whether the target is finish.
        :return:
        """
        return not self

    def is_prepare(self):
        return self._prepare

    def restart(self):
        self._prepare = True
        self.state = self.start


if __name__ == '__main__':
    """ --------  example 1 -------- """
    print("example 1: ")


    def update(state, data):
        if state == 'idle':
            print("i'm idle, next to move")
            return "move"
        elif state == 'move':
            print("i'm moving, next to stop")
            return "stop"
        else:
            return 'stop'


    sm1 = StateMachine('idle', 'stop')

    sm1.add('idle', 'move', 'stop', "useless", fn=update)
    print(sm1.list())
    sm1.remove('useless')
    print(sm1.list())
    while sm1:
        print(sm1, '\n\t', end="")
        sm1.step()
        print()

    print("finish.\n")

    """ -------- example 2 -------- """
    print("example 2: ")


    def update(state, *a):
        if state == 'idle':
            print("i'm idle, next to move")
            return "move"
        elif state == 'move':
            print("i'm moving, next to stop")
            return "stop"
        else:
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


    def update(state, o):
        if state == 'idle':
            print("i'm idle, next to move")
            return "move"
        elif state == 'move':
            print("i'm moving, next to stop")
            return "stop"
        else:
            return 'stop'


    sm1, sm2 = StateMachine('idle', 'stop'), StateMachine('idle', 'stop')
    sm1.add('idle', 'move', 'stop', fn=update)
    sm2.add('idle', 'move', 'stop', fn=update)

    sm1.link('stop', sm2,'idle')  # link sm1.stop -> sm2.idle &emsp;&emsp; # when sm1.state come to 'stop', it will start at sm2.idle in next sm1.step

    while sm1.step():
        ...  # note that you only call sm1.step() here
    print("finish.")

