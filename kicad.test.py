import kicad
import svg 
import sys

p = svg.Path(sys.argv[1])
p.parse()

l = kicad.LibModule("/tmp/1.mod")
m = kicad.Module("MyTest")
m.position()
m.reference('T*')
m.value('testing')

for s in p.simplify(0.5):
    pts = [(0.01 * x).coord() for x in s]
    pts.reverse()
    p1 = pts.pop()
    while pts:
        p2 = pts.pop()
        m.draw(kicad.Segment(p1, p2, 0.20))
        p1 = p2

l.add_module(m)
l.write()

