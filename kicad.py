import time

LIBMODULE_HEADER = 'PCBNEW-LibModule-V1  '
LIBMODULE_HEADER += time.strftime("%c", time.localtime())
LIBMODULE_HEADER += '\n# encoding utf-8\n'
LIBMODULE_HEADER += 'Units mm\n'

class LibModule:
    '''Container (file) for all the Modules'''
    def __init__(self, filename):
        self.filename = filename
        self.modules = []

    def add_module(self, mod):
        self.modules.append(mod)

    def write(self):
        f = open(self.filename, 'w')
        f.write(LIBMODULE_HEADER)
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
        self.position = {
            'Xpos': 0,
            'Ypos': 0,
            'orientation': 0,
            'layer': 15,
            'timestamp': '00000000 00000000',
            'attr1': '~',
            'attr2': '~'}
        self.cd = ''
        self.kw = ''
        self.fields = []
        self.drawings = []
        self.pads = [] # not implemented

        self.reference('M*')
        self.value(name)

    def __str__(self):
        s = '$MODULE ' + self.name + '\n'
        # Position
        s += 'Po {Xpos} {Ypos} {orientation} {layer} {timestamp} {attr1}{attr2}\n'.format(**self.position)
        # Module lib name
        s += 'Li ' + self.name + '\n'
        # Comments & keywords
        s += 'Cd ' + self.cd + '\n'
        s += 'Kw ' + self.kw + '\n'
        # TimeStampOp (?)
        s += 'Sc 00000000\n'
        # AR (?)
        s += 'AR ' + self.name + '\n'
        # Op (?)
        s += 'Op 0 0 0\n'
        # fields
        for f in self.fields:
            s += 'T{nb} {Xpos} {Ypos} {Xsize} {Ysize} {rotation} {penWidth} N {visible} {layer} N "{text}"\n'.format(**f)
        # drawings
        for d in self.drawings:
            s += str(d)
        s += '$EndMODULE ' + self.name + '\n'
        return s

    def position(self, x=None, y=None, orientation=None, layer=None):
        if x is not None:
            self.position['Xpos'] = x
        if y is not None:
            self.position['Ypos'] = y
        if orientation is not None:
            self.position['orientation'] = orientation
        if layer is not None:
            self.position['layer'] = layer

    def comment(self, desc=''):
        self.cd = desc

    def keywords(self, kw=''):
        self.kw = kw

    def field(self, nb, Xpos=0, Ypos=0, Xsize=0.8128, Ysize=0.8128, rotation=0, penWidth=0.1524, visible=True, layer=21, text=''):
        if visible:
            visible = 'V'
        else:
            visible = 'I'

        # Remove posible duplicate
        self.fields = [f for f in self.fields if f.get('nb') != nb]

        f = {
        'nb': nb,
        'Xpos': Xpos,
        'Ypos': Ypos,
        'Xsize': Xsize,
        'Ysize': Ysize,
        'rotation': rotation,
        'penWidth': penWidth,
        'visible': visible,
        'layer': layer,
        'text': text}
        self.fields.append(f)

    def reference(self, ref):
        self.field(0, text=ref)
    def value(self, value):
        self.field(1, text=value)

    def draw(self, d):
        self.drawings.append(d)

class Segment:
    def __init__(self, start, end, width, layer=21):
        self.start = start
        self.end = end
        self.width = width
        self.layer = layer

    def __str__(self):
        s = 'DS '
        s += ' '.join(map(str, self.start)) + ' '
        s += ' '.join(map(str, self.end)) + ' '
        s += str(self.width) + ' '
        s += str(self.layer) + '\n'
        return s

class Polygon:
    def __init__(self, pts, width=0, layer=21):
        self.length = len(pts)
        self.pts = list(pts)
        self.width = width
        self.layer = layer

    def __str__(self):
        s = 'DP 0 0 0 0 '
        s += str(self.length) + ' '
        s += str(self.width) + ' '
        s += str(self.layer) + '\n'
        for pt in self.pts:
            s += 'Dl ' + ' '.join(map(str, pt)) + '\n'
        return s

class Circle:
    def __init__(self, center, radius, width, layer=21):
        self.center = center
        self.pt = (center[0] + radius, center[1])
        self.width = width
        self.layer = layer

    def __str__(self):
        s = 'DC '
        s += ' '.join(map(str, self.center)) + ' '
        s += ' '.join(map(str, self.pt)) + ' '
        s += str(self.width) + ' '
        s += str(self.layer) + '\n'
        return s
