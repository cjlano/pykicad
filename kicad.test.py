import kicad
import svg 
import sys

p = svg.Path(sys.argv[1])
p.parse()

l = kicad.LibModule("/tmp/1.mod")
m = kicad.Module("MyTest")
m.reference('T*')
m.value('testing')

a,b = p.bbox()
# We want a 10.0mm width logo
width = 10.0
ratio = width/(b-a).x
# Centering offset
offset = (a-b)*0.5*ratio

#for s in p.scale(ratio).translate(offset).simplify(0.01):
#    pts = [x.coord() for x in s]
#    pts.reverse()
#    p1 = pts.pop()
#    while pts:
#        p2 = pts.pop()
#        m.draw(kicad.Segment(p1, p2, 0.20))
#        p1 = p2

for s in p.scale(ratio).translate(offset).simplify(0.01):
    m.draw(kicad.Polygon([x.coord() for x in s]))

l.add_module(m)
l.write()

