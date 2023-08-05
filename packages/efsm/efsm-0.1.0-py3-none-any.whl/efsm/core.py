# -*- coding: utf-8 -*-

class Local:
    ...


class State:
    def __new__(cls, *names, fn=None, data=None):
        assert fn is not None, "param 'fn' need a function like fn(state, d)->state but get None."

        return [names, fn, Local() if data is not None else data]


class StateMachineBase:
    def __init__(self, start, end=None, on_end=None):
        """
        new a statemachine
        :param start: start state name
        :param end: end state name
                _ = None
        :param on_end: fn(statemachine)->None Once state is run to end, python will auto call it.
                _ = None
        """
        self._prepare = True

        self.start = start  # 指示状态机入口， 是一个keyname
        self.end = end  # 指示状态机出口， 是一个keyname
        self.on_end = on_end

        self.state = self.start
        self.groups = {}

        # self.add(state)

    @staticmethod
    def _standard(*state, fn=None, data=None):
        """
        标准化
        :param state: [names, fn, data] or *names, fn=None
        :param fn: only available when len(state) > 1 which mean you want to instance a State in this add function.
        :param data: only available when len(state) > 1 which mean you want to instance a State in this add function.
        :return:
        """
        assert state, "get empty state."
        if fn is None:
            assert len(state) == 1, "you can pass in only a state at once, but get " + str(state)
            state = state[0]
            assert len(state) == 3, "unexpected state to get " + str(state)
        else:
            state = State(*state, fn=fn, data=data)
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

    def __getitem__(self, item):
        get = self.groups.get(item)
        if get is not None:
            return get
        else:
            return self._find(self.groups, item)

    def __bool__(self):
        return self.state != self.end

    def __call__(self):
        return self.step()

    def __str__(self):
        txt = "StateMachine<" + str(self.state) + "> " + ("running" if self else "finish")
        return txt


class StateMachine(StateMachineBase):
    def add(self, *state, fn=None, data=None):
        """
        # example:
        .add(s_idle)
        .add('idle', 'move', fn = my_fn)


        :param state: [keynames, fn, data] or *names, fn=None
        :param fn: only available when len(state) > 1 which mean you want to instance a State in this add function.
        :param data: only available when len(state) > 1 which mean you want to instance a State in this add function.
        :return:
        """

        state = self._standard(*state, fn=fn, data=data)

        self.groups[state[0]] = state[1:]

    def remove(self, *state, error=True):
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
            _s = self._find(self.groups, s)

            if _s is not None:
                list(_s).remove(s)
                temp = self.groups.pop(_s)
                if _s:
                    self.groups[_s] = temp
            elif error:
                raise TypeError("'x':" + str(s) + " not in statemachine")

    def find(self, state):
        """
        寻找一个state
        :param state: keyname
        :return: (fn, data) or None
        """
        s = self._find(state)

        if s is not None:
            return s[1], s[2]
        else:
            return None

    def list(self):
        """
        展示所有的state
        :return: {state: (fn, data)}
        """
        states = {}
        for k in self.groups:
            for name in k:
                states[name] = self.groups[k]
        return states

    def step(self):
        """
        步进
        :return: bool about statemachine is running-needy or not.
        """

        if self._prepare:
            self._prepare = False

        if self.state == self.end:
            return False

        state = self._find(self.groups, self.state)
        assert state is not None, "can not find state:" + str(self.state) + ". Please check whether you add this state before."

        state = state[1](self.state, state[2])
        assert state is not None, "fn of state:" + str(self.state) + " need return a state name but get None."

        self.state = state

        # check if end
        if self.end is not None and state == self.end:
            if self.on_end: self.on_end(self)
            return False

        return True

    def is_finish(self):
        return not self

    def is_prepare(self):
        return self._prepare

    def restart(self):
        self._prepare = True
        self.state = self.start


if __name__ == '__main__':
    def update(state, *a):
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
