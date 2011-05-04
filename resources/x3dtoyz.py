"""
Kirby Urner
4D Solutions
First published: June 12 2007

Simple framework for studying X3D, an industry standard
inheriting from VRML, plus use of Template class in the
Standard Library string module.

Dependencies (outside of Standard Library):

http://www.4dsolutions.net/ocn/python/stickworks.py
http://www.4dsolutions.net/ocn/python/polyhedra.py

"""

from string import Template
from time import asctime, localtime, time
from random import randint
from stickworks import Vector, Edge
from polyhedra import Tetrahedron, Cube, Icosahedron, Octahedron, Coupler, Mite
from math import sqrt, hypot, acos
              
gl_thetemplate = Template(
"""<?xml version="1.0" encoding="UTF-8"?>
<X3D profile="Immersive" version="3.1"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance"
  xsd:noNamespaceSchemaLocation="http://www.web3d.org/specifications/x3d-3.1.xsd">
  <head>
    <meta content="$filename" name="title"/>
    <meta content="$thedescript" name="description"/>
    <meta content="$theauthor" name="creator"/>
    <meta content="$thedate" name="created"/>
  </head>
  <Scene>$thescene</Scene>
</X3D>
"""
)

gl_shape = Template("""
<Transform>
    $shapes
</Transform>
"""
)

gl_theedge = Template(
"""
    <Transform translation = "$translate">
        <Transform rotation = "$roty">
            <Transform rotation = "$rotx">      
                <Shape>
                    <Cylinder height="$length" radius="$radius"
                    containerField="geometry"
                    side="true" solid="true" top="true" />
                    <Appearance>
                      <Material diffuseColor="$color"/>
                    </Appearance>                    
                </Shape>
            </Transform>
        </Transform>    
    </Transform>
"""
)

gl_thevertex = Template (
"""
    <Transform translation = "$translate">
    <Shape>
        <Sphere containerField="geometry"
         radius="$radius" solid="true"/>
        <Appearance>
          <Material diffuseColor="$color"/>
        </Appearance>         
    </Shape>
    </Transform>
"""
)

gl_theface = Template (
"""
    <Transform>
        <Shape>
            <IndexedFaceSet coordIndex="$corners" solid="false" >
                <Coordinate point="$coords" />
            </IndexedFaceSet>
            <Appearance>
              <Material diffuseColor="$color"/>
            </Appearance>            
        </Shape>
    </Transform>    
"""
)

colordict = dict(
             Red     = "1.0 0.0 0.0",
             Green   = "0.0 1.0 0.0",
             Blue    = "0.0 0.0 1.0",
             Yellow  = "1.0 1.0 0.0",
             Cyan    = "0.0 1.0 1.0",
             Magenta = "1.0 0.0 1.0",
             White   = "1.0 1.0 1.0",
             Black   = "0.0 0.0 0.0",
             Orange  = "1.0 0.5 0.0",
             Violet  = "0.309804 0.184314 0.309804",
             Indigo  = "0.294117 0.0      0.509803",
             Brown   = "0.647059 0.164706 0.164706",
             Wood    = "0.647059 0.164706 0.164706",                
             Grey    = "0.752941 0.752941 0.752941",
             Gray    = "0.752941 0.752941 0.752941",
             Gold    = "0.8 0.498039 0.196078",
             Silver  = "0.90 0.91 0.98")

class Scene (object) :

    thepath = 'c:/python25/Lib/site-packages/'
        
    def __init__(self, thefile='test.x3d', desc = 'test file', author = 'me'):
        self.header = dict(
              filename = thefile,
              thedescript = desc,
              thedate = asctime(localtime(time())),
              theauthor = author)
        self.objects = []

    def _orient(self, etuple):
        """
        recycled code from a much earlier VRML2 application,
        used in proprietary mode for DST to produce
        StrangeAttractors .wrl files.
        """
        data  = [(0,0,0),0,0,0]

        # midpoint of edge between vert0 and vert1
        midpoint = (etuple[0]+etuple[1])*(1/2.0)
              
        # used to translate from origin
        data[0]  = midpoint.xyz

        # tip = translated endpoint (w/ midpoint at 0,0,0)
        tip = etuple[1]-midpoint

        # length of cylinder
        hyp = tip.length
        data[1]=2*hyp

        # height above Y plane             
        xzhyp = hypot(tip.xyz[0],tip.xyz[2])

        # rotate zx plane around north/south (y) axis to
        # have xy plane intersect tip
        if xzhyp!=0:
          mval = tip.xyz[2]/xzhyp           
          data[2] = acos(mval)

        if tip.xyz[0]<=0: data[2] = -data[2]

        # rotate about x axis, tilting y axis to tip
        if hyp!=0: 
           mval = tip.xyz[1]/hyp
           data[3] = acos(mval)
          
        return data #object handle for array w/ new data
    
    def _edges(self, someobj):        
        # cylinders
        thevertices = someobj.vertices        
        for edge in someobj.edges:
            v1 = edge.v0
            v2 = edge.v1
            vrmldata = self._orient((v1,v2))
            length,roty,rotx = (vrmldata[1],vrmldata[2],vrmldata[3])
      
            edict = dict(
                radius    = edge.radius,
                color     = colordict[someobj.ecolor],
                length    = length,              
                translate = "%r %r %r" % vrmldata[0],
                roty      = "0 1 0 %s" % roty,       
                rotx      = "1 0 0 %s" % rotx)
            
            someobj.text = someobj.text + gl_theedge.substitute(edict)

    def _vertexes(self, someobj):
        # spheres
        thevertices = someobj.vertices
        for vertex in someobj.vertices:
            sdict = dict(
                color     = colordict[someobj.vcolor],
                radius    = thevertices[vertex].radius,       
                translate = "%r %r %r" % thevertices[vertex].xyz)
            
            someobj.text = someobj.text + gl_thevertex.substitute(sdict)

    def _faces(self, someobj):
        # polygons
        thevertices = someobj.vertices        
        for face in someobj.faces:
            theverts = " "            
            for v in face: 
               theverts += " %r %r %r, " % thevertices[v].xyz
            fdict = dict(
                color   = colordict[someobj.fcolor],
                coords  = theverts,
                corners = range(len(face)) + [-1])
            
            someobj.text = someobj.text + gl_theface.substitute(fdict)
        
    def write(self):
        # set the stage
        self.fileobject = open(Scene.thepath + self.header['filename'], 'w')
        # write each object
        for obj in self.objects:
            obj.text = ""  # patch of xml for each object
            if obj.showvertices:
                self._vertexes(obj)
            if obj.showedges:
                self._edges(obj)
            if obj.showfaces:
                self._faces(obj)

        shapes = "" # concatenate the xml
        for obj in self.objects:
            shapes = shapes + obj.text

        
        # save the whole scene, telescoping back to gl_thetemplate
        # as outer context
        self.header["thescene"] = shapes
        self.fileobject.write(gl_thetemplate.substitute(self.header))
        self.fileobject.close()

# TESTS

"""
An interesting feature of this code is the used of attributes not
mentioned anywhere in the class definition.  Python allows generic
objects to be assigned new properties at will.  So XML builds up
within objects as obj.text, before going to a file as a final step.
Likewise, color attributes fcolor, vcolor and ecolor are expected
for each polyhedron.
"""

def makecoupler():

    thecube = Cube()
    thecube.ecolor = "Green"
    thecube.vcolor = "Silver"
    thecube.showfaces = False

    thecoupler = Coupler()
    thecoupler.ecolor = "Orange"
    thecoupler.vcolor = "Silver"
    thecoupler.fcolor = "Wood"
    
    output = Scene('test0.x3d')
    output.objects.append(thecube)
    output.objects.append(thecoupler)
    output.write()
    
def makemite():
    thecube = Cube()
    thecube.ecolor = "Green"
    thecube.vcolor = "Silver"
    thecube.showfaces = False
    
    thecoupler = Coupler()    
    thecoupler.showfaces = False
    thecoupler.ecolor = "Orange"
    thecoupler.vcolor = "Silver"

    themite = Mite()
    themite.ecolor = "Orange"
    themite.vcolor = "Silver"
    
    output = Scene('test1.x3d')
    
    output.objects.append(thecube)
    output.objects.append(thecoupler)
    output.objects.append(themite)
    output.write()

def maketent():

    output = Scene('test2.x3d')    # naming disk file
    Vector.radius = 0.07        
    thetet = Tetrahedron()
    thetet.showfaces = False
    thetet.ecolor = "Yellow"
    thetet.vcolor = "Indigo"

    output.objects.append(thetet) # appending Polyhedron object
    output.write()

def makeicosa():
    output = Scene('test3.x3d')    # naming disk file
    icosa = Icosahedron() * sqrt(2)
    icosa.fcolor = "Cyan"
    icosa.vcolor = "Silver"
    icosa.ecolor = "Orange"
    # appending a scaled Polyhedron object
    output.objects.append( icosa ) 
    output.write()

def manymes():
    pass

def test():

    """list the functions"""
    thetests = [
        makecoupler,  # Coupler
        makemite,     # Mighty Mite
        maketent,     # tetra tent
        makeicosa,    # i, icosa
        manymes]      # many mes
    
    while True:
        print """
        Choose:
        0  Coupler
        1  Mighty Mite
        2  Tetra Tent
        3  I, Icosa
        4  Many Mes
        Q  Outta here!
        
        """

        ans = raw_input('Choice? ')
        
        if ans in 'Qq':
            break

        # trap more errors here
        
        thetests[int(ans)]()  # perform user selection (or crash?)

        print "View output, hit Enter to continue..."

        # pause to look in the POV-Ray window
        ok = raw_input()
            
    return # null

if __name__ == '__main__':
    test()
