"""
Compilation
"""


class LevelError(Exception):
    def __init__(self):
        print('level has some problem')


class Tree:
    def __init__(self, code):
        code = code.split('\n')
        self.level = []
        for i in code:
            if i == '':
                continue
            self.level.append(i.count(' ') // 4)
        self.code = [i.replace(' ', '') for i in code if i != '']

    def __call__(self, base=0, code=None, level=None):
        if (code and level) is None:
            code = self.code
            level = self.level
        wait = False  # wait or not
        pre_c = []  # making code
        pre_l = []  # making level
        out = {}  # final
        last = ''  # the key before
        for code_, level_ in zip(code, level):  # iter code, level
            if level_ == base:  # a smaller tree
                if wait:  # build last tree
                    out[last] = self.__call__(base + 1, pre_c, pre_l)
                    pre_c = []
                    pre_l = []
                if code_[-1] == ':':  # A tree block is going to start
                    last = code_.split(':')[0]
                    wait = True
                elif code_[-1] != ':':  # Oneline tree
                    split = code_.split(':')
                    out[split[0]] = split[1]
            elif level_ > base:  # son level
                pre_c.append(code_)
                pre_l.append(level_)
        if wait:  # build last tree
            out[last] = self.__call__(base + 1, pre_c, pre_l)
        return out
