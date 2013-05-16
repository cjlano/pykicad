import time

class LibModule:
    '''Container (file) for all the Modules'''
    def __init__(self, filename):
        self.filename = filename
        self.modules = []

    def add_module(self, mod):
        self.modules.append(mod)

    def _header(self):
        s = 'PCBNEW-LibModule-V1  '
        s += time.strftime("%a %d %b %Y %H:%M:%S %Z", time.localtime())
        s += '\n'
        s += '# encoding utf-8'
        return s

    def write(self):
        f = open(self.filename, 'w')
        f.write(self._header())
        # Index
        f.write("$INDEX\n")
        for m in self.modules:
            f.write(m.name + '\n')
        f.write("$EndINDEX\n")
        for m in self.modules:
            f.write(str(m))
        f.close()


class Module:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        s = '$MODULE ' + self.name + '\n'
        s += '$EndMODULE ' + self.name + '\n'

        return s

