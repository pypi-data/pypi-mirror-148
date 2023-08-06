# -*- coding: utf-8 -*-
import re

from efsm.standard.core import StateMachineBase, StateMachine

# region const
_scpl = re.compile("@[(s)(sta)(state)]\s*.*")
_splt = re.compile('[(\s*)(\s*,\s*)]')
_assn = re.compile('[:(\->)]')
_lsta = lambda *a: ...
_step = lambda self: self._efsm.step()
_bool = lambda self: bool(self._efsm)


# endregion

# region api-shell
class Local():
    def __call__(self, fn):
        fn._lc_ = self
        return fn


class SingleMetaClass(type):
    def __call__(self, *args, **kwargs):
        """
        efsm : class Singleton
        """
        if not hasattr(self, "_ins_"):
            insObject = super(__class__, self).__call__(*args, **kwargs)
            insObject._ins_ = insObject
        return self._ins_


_function = type(lambda: ...)


class EfsmBase(StateMachine):

    def __init__(self, start=None, end=None, on_step=None, on_end=None, name=None):
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
        super(EfsmBase, self).__init__(start, end, on_step, on_end, name if name is not None else ("Efsm" + str(self._id)))
        self.ss = StateSet(_efsm=self)
        self._tfns = {}  # {fn: True}

    def _try_update(self):
        if self._tfns:  #
            # print(self._tfns)
            for tfn in self._tfns:
                self(tfn)
            self._tfns = {}

        if self.state is None and self.start is not None:
            self.state = self.start

    def tolist(self):
        """
        change statemachine._groups to list
        :param self:
        :return: [[(names), fn, data], ...]
        """
        self._try_update()
        return [[k] + v for k, v in self._groups.items()]

    @staticmethod
    def _parse(doc):
        """
        特指解析带doc的函数, 只会解析出带有的state
        :return:
        """
        # region find all @s/ @sta /@state ...
        if doc is None: return []
        lines = re.findall(_scpl, doc)
        _stas = []

        # find -> or :
        for line in lines:
            temp = re.search("#.*", line)
            if temp:
                line = line[:temp.span()[0]]

            temp = re.search(_assn, line)
            if temp:
                line = line[:temp.span()[0]]

            for e in re.split(_splt, line):
                if e and e[0] != "@":
                    _stas += [e]


        return _stas
        # endregion

    def __iter__(self):
        self._try_update()
        return iter(self._groups)

    def __getitem__(self, item):
        self._try_update()
        return EfsmBase._find(self._groups, item)

    def __bool__(self):
        self._try_update()
        if self.state is None and self.start != None:
            self.state = self.start
        return self.state != self.end if self._target is None else bool(self._target)

    def __str__(self):
        self._try_update()
        txt = self.name
        if self._target is not None:
            txt += " -> " + str(self._target)
        else:
            txt += ":" + str(self.state) + " - " + ("running" if self else "finish")

        return txt


class Efsm(EfsmBase):
    """
    Better HighAPI StateMachine
    """

    def add(self, *state, fn=None, data=None):
        # print(state, fn, data)
        if fn is None:
            state, _state = [], state
            for item in _state:
                if isinstance(item, StateWrapper):
                    raise Exception(f"Can not pass a Static and Empty StateSet.")
                elif isinstance(item, StateSet):
                    __state = item.tolist()
                    self._groups[__state[0]] = __state[1:]
                    state += __state
                elif hasattr(item, '_ss_'):
                    self._tfns[item] = True
                    self._try_update()
                    state += item._ss_
                elif callable(item):  # type(state[0]) == _function:
                    get = Efsm._parse(item.__doc__)
                    if get:
                        state += super(Efsm, self).add(*get, fn=item, data=data)
                    else:
                        raise Exception(f"fn:{item.__name__} does not have doc for state.")
                else:
                    raise Exception("Unexpected get{fn:None, state:{" + str(item) + "}}. Only could recv StateSet/doced-function when fn is None.")
        else:
            state = super(Efsm, self).add(*state, fn=fn, data=data)
            # print(state)

        if self.start is None:
            self.start = state[0][0]

        if self.end is None:
            self.end = state[0][-1]

        return state

    def remove(self, *state, error=True):
        for s in state:
            if isinstance(s, StateSet):
                self.remove(*s.states, error)
            else:
                _s = EfsmBase._find(self._groups, s)

                if _s is not None:
                    list(_s).remove(s)
                    temp = self._groups.pop(_s)
                    if _s:
                        self._groups[_s] = temp
                elif error:
                    raise TypeError("'x':" + str(s) + " not in statemachine")

    def step(self):
        """
        步进
        :return: bool about statemachine is running-needy or not.
        """

        if self._prepare:
            self._prepare = False

        if self._tfns:  # 动态加载
            for tfn in self._tfns:
                self(tfn)
            self._tfns = {}

        if self.state is None:
            self.state = self.start
            if self.start is None:
                raise Exception("Efsm does not have a start state.")

        # try to retarget
        if self._target:
            return self._target.step()

        # step for itself
        ''''''
        if self.end is not None and self.state == self.end:
            return False

        state = EfsmBase._find(self._groups, self.state)
        assert state is not None, "can not find state:" + str(self.state) + ". Please check whether you add this state before."

        state = state[1](self.state, state[2])
        # assert state is not None, "fn of state:" + str(efsm.state) + " need return a state name but get None."

        self.state = state
        ''''''

        # update target
        self._target = self._redirect(self, self.state)

        # try on_step
        if self.on_step:
            self.on_step(self)

        # check if end
        if self.end is not None and state == self.end:
            if self.on_end: self.on_end(self)
            return False

        return True

    def __call__(self, fn):
        _states = getattr(fn, '_ss_', [])
        assert _states, "function:{} have not bind any states.".format(fn.__name__)
        _data = getattr(fn, '_lc_', None)
        self.add(*_states, fn=fn, data=_data)
        return fn


class StateWrapper:
    """
    [二段式]
    状态函数打包器
    """

    def __init__(self, *states, _efsm=None):
        self.__states = list(states)
        self.__efsm = _efsm
        #self.__class__ = StateSet

    def __getattr__(self, item):
        return StateWrapper(*self.__states, item, _efsm=self.__efsm)

    def __getitem__(self, item):
        if not isinstance(item, (list, tuple)):
            item = (item,)
        return StateWrapper(*self.__states, *item)

    def __str__(self):
        return "StateSet:Static|Empty"

    def __repr__(self):
        return str(self)

    def __call__(self, fn):
        fn._ss_ = self.__states + getattr(fn, "_ss_", [])
        if self.__efsm is not None:
            self.__efsm._tfns[fn] = True
        return fn


def CombineCE(cond, exec):
    def _ce_(state, o):
        if cond(state, o):
            return exec(state, o)

    _ce_._c_ = cond
    _ce_._e_ = exec
    return _ce_


class StateSet:
    """
    定义了一组state，共用一个二段式fn或三段式的(cond, exec)
    """

    def __new__(cls, *args, _efsm=None, **kwargs):
        # print(len(args))
        if len(args) == 0 or _efsm is not None:
            # print(1)
            return StateWrapper(_efsm=_efsm)
        else:
            # print(2)
            return super().__new__(cls)

    def __init__(self, *states, fn=None, data=None, cond=None, exec=None):
        self.states = list(states)
        self._fn = None
        self._cond, self._exec = None, None
        if exec is not None:
            self.assign(cond, exec)
        self.data = data

    def __str__(self):
        return f"StateSet:{self.states} -> {self.fn} with {self.data}"

    def __repr__(self):
        return str(self)

    @property
    def fn(self):
        return self._fn

    @property
    def cond(self):
        return self._cond

    @property
    def exec(self):
        return self._exec

    def assign(self, arg1, arg2=None):
        """
        [二段式]
        分配一个函数给这几个state
        [三段式]
        分配一个(cond, exec)给这几个state
        :param arg1: [二段式]fn / [三段式]cond
        :param arg2: [三段式]exec
        :return:
        """
        if arg2 is None:
            self._fn = arg1
            self._fn._c_ = None
            self._fn._e_ = None
            self._cond, self._exec = None, None
        else:
            self._cond, self._exec = arg1, arg2
            self._fn = CombineCE(arg1, arg2)

    def tolist(self):
        return [tuple(self.states), self._fn, self.data if self.data is not None else Local()]


# ss = StateSet()

# print(fsm, ss)

fsm = Efsm()  # default fsm designed for you.

ss = StateSet()  # default StateSet designed for you. There is no need to create a other empty stateset.

# endregion

# region state for class

class EfsmMeta(type):

    def __init__(cls, *args, **kwgs):
        cls.__states = {}
        setattr(cls, getattr(cls, "__step__", 'step'), _step)
        setattr(cls, '__bool__', getattr(cls, "__bool__", _bool))

        # region find all @s/ @sta /@state ...
        if cls.__doc__ is None: return
        lines = re.findall(_scpl, cls.__doc__)

        # find -> or :
        for line in lines:
            temp = re.search("#.*", line)
            if temp:
                line = line[:temp.span()[0]]
            # print(line)
            temp = re.search(_assn, line)
            if temp is None: raise Exception(f"{line} does not assign a state-function to handle them.")
            sep = temp.span()
            part1, part2 = line[:sep[0]], line[sep[1] + 1:]

            # region part1
            _stas = []
            for e in re.split(_splt, part1):
                if e and e[0] != "@":
                    _stas += [e]
            _stas = tuple(_stas)
            # endregion

            # print(part2)
            cls.__states[_stas] = re.sub('\s', '', part2)
        # endregion

    def __call__(cls, *args, **kwgs):
        ins = cls.__new__(cls, *args, **kwgs)

        # region init efsm for ins
        ins._efsm = getattr(ins, '_efsm', Efsm())
        for k, v in cls.__states.items():
            fn = getattr(ins, v, None)
            assert fn, f"{cls} does not have method '{v}', which you want to assgin to the states {k}."
            ins._efsm.add(*k, fn=fn)
        # endregion

        cls.__init__(ins, *args, **kwgs)
        return ins


# endregion

def update(state, o):
    """
    @state idle, move, stop
    :param state:
    :param o:
    :return:
    """
    ...


if __name__ == '__main__':
    print("example 1: ")


    # fsm = Efsm()  # 内部默认了一个fsm

    @fsm.ss.idle.move.stop  # careful: It's not proper to use for class method. Because it will record it immediately.| Use basic way to add a method, or try Example2
    def update(state, data):
        match state:
            case 'idle':
                print("i'm idle, next to move")
                return "move"
            case 'move':
                print("i'm moving, next to stop")
                return "stop"
        return 'stop'


    # fsm.end = 'stop'
    # 当fsm没有start时，会尝试将第一次添加的状态的第一个作为start
    # 当fsm没有end时，会尝试将第一次添加的状态的最后一个作为end

    while fsm:
        print(fsm, '\n\t', end="")
        fsm.step()
        print()

    print("finish.\n")

    # -----------------------------------------
    print("example 2: ")

    fsm.restart()  # clear for example1

    def update(state, data):
        """
        @state idle move stop   # ',' is not a matter
        :param state:
        :param data:
        :return:
        """
        match state:
            case 'idle':
                print("i'm idle, next to move")
                return "move"
            case 'move':
                print("i'm moving, next to stop")
                return "stop"
        return 'stop'

    fsm.add(update)

    while fsm:
        print(fsm, '\n\t', end="")
        fsm.step()
        print()

    print("finish.\n")

    # -----------------------------------------
    print("example 3: ")

    fsm.restart()  # clear for example1

    class Test:
        def update(self, state, data):
            """
            @state idle move stop  # ',' is not a matter
            :param state:
            :param data:
            :return:
            """
            match state:
                case 'idle':
                    print("i'm idle, next to move")
                    return "move"
                case 'move':
                    print("i'm moving, next to stop")
                    return "stop"
            return 'stop'

    test = Test()

    fsm.add(test.update)

    while fsm:
        print(fsm, '\n\t', end="")
        fsm.step()
        print()

    print("finish.\n")

    # -----------------------------------------
    print("example 4: ")


    class PhyNote(metaclass=EfsmMeta):  # use EfsmMeta to auto add PhyNote._efsm = Efsm()
        """
        the proper using in class
        @state idle, anim, death -> switch  # like efsm.add(idle, anim, death, fn=switch)
        """

        # __step__ = 'step'  # Auto create a method in this class, used for efsm.step(). Default is 'step', you can overwrite it.
        # def __bool__(self): ...  # Auto create a __bool__ method if you donot define it, Default is efsm.__bool__, you can overwrite it.

        def switch(self, state, data):
            match state:
                case 'idle':
                    print("i'm idle, next to anim")
                    return "anim"
                case 'anim':
                    print("i'm moving, next to death")
                    return "death"
            return 'death'

    pn = PhyNote()

    while pn:
        pn.step()
