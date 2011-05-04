"""
Kirby Urner
4D Solutions
First published: May 10 2007

May 13:  added finer grain control of textures (now per shape),
turned gl_settings into a Template to provide more control, new tests.

Simple framework for studying POV-Ray's Scene Description Language,
use of Template class in the Standard Library string module.

Dependencies (outside of Standard Library):

http://www.4dsolutions.net/ocn/python/stickworks.py
http://www.4dsolutions.net/ocn/python/polyhedra.py

"""

from string import Template
from time import asctime, localtime, time
from random import randint
from stickworks import Vector, Edge
from polyhedra import Tetrahedron, Cube, Icosahedron, Octahedron, Coupler, Mite
from math import sqrt
              
gl_theheader = Template(
"""
// Persistence of Vision Ray Tracer Scene Description File
// File: $filename
// Vers: 3.6
// Desc: $thedescript
// Date: $thedate
// Auth: $theauthor
// ==== Standard POV-Ray Includes ====
#include "colors.inc"     // Standard Color definitions
#include "textures.inc"   // Standard Texture definitions
#include "functions.inc"  // internal functions usable in user defined functions

// ==== Additional Includes ====
// Don't have all of the following included at once, it'll cost memory and time
// to parse!
// --- general include files ---
#include "chars.inc"      // A complete library of character objects, by Ken Maeno
#include "skies.inc"      // Ready defined sky spheres
#include "stars.inc"      // Some star fields
#include "strings.inc"    // macros for generating and manipulating text strings

// --- textures ---
#include "finish.inc"     // Some basic finishes
#include "glass.inc"      // Glass textures/interiors
#include "golds.inc"      // Gold textures
#include "metals.inc"     // Metallic pigments, finishes, and textures
#include "stones.inc"     // Binding include-file for STONES1 and STONES2
#include "stones1.inc"    // Great stone-textures created by Mike Miller
#include "stones2.inc"    // More, done by Dan Farmer and Paul Novak
#include "woodmaps.inc"   // Basic wooden colormaps
#include "woods.inc"      // Great wooden textures created by Dan Farmer and Paul Novak
"""
)

gl_thesettings = Template("""
// perspective (default) camera
camera {
  location  <$camx, $camy, $camz>
  look_at   <0.0, 0.0,  0.0>
  right     x*image_width/image_height
}

// create a regular point light source
light_source {
  0*x                  // light's position (translated below)
  color rgb <1,1,1>    // light's color
  translate <-20, 40, -20>
}

background { color rgb <0.0, 0.0, 0.0> }

"""
)

gl_theedge = Template(
"""
  cylinder {
    <$x0, $y0, $z0>,     // Center of one end
    <$x1, $y1, $z1>,     // Center of other end
    $radius              // Radius
    open                 // Remove end caps
    texture { $edge_texture }
  }
"""
)

gl_thevertex = Template(
"""
  sphere { <$x0, $y0, $z0>, $radius
    texture { $vertex_texture }
  }
"""
)

gl_theface = Template (
"""
  polygon {
    $numcorners,
    $eachcorner
    texture { $face_texture }
  }
"""
)
          
class Scene (object) :

    thepath = 'c:/python25/Lib/site-packages/'
        
    def __init__(self, thefile='test.pov', desc = 'test file', author = 'me'):
        self.header = dict(
              filename = thefile,
              thedescript = desc,
              thedate = asctime(localtime(time())),
              theauthor = author)
        self.settings = dict(
              camx =  0.0,
              camy =  2.0,
              camz = -3.0)
        self.objects = []

    def _edges(self, someobj):        
        # cylinders
        for edge in someobj.edges:
            edict = dict(x0 = edge.v0.xyz[0],
                         y0 = edge.v0.xyz[1],
                         z0 = edge.v0.xyz[2],
                         
                         x1 = edge.v1.xyz[0],
                         y1 = edge.v1.xyz[1],
                         z1 = edge.v1.xyz[2],
                         
                         radius = edge.radius,
                         edge_texture = someobj.edge_texture)

            self.fileobject.write(gl_theedge.substitute(edict))

    def _vertexes(self, someobj):
        # spheres
        thevertices = someobj.vertices
        for vertex in someobj.vertices:
            vdict = dict(x0 = thevertices[vertex].xyz[0],
                         y0 = thevertices[vertex].xyz[1],
                         z0 = thevertices[vertex].xyz[2],
                         
                         radius = thevertices[vertex].radius,
                         vertex_texture = someobj.vertex_texture
                         )

            self.fileobject.write(gl_thevertex.substitute(vdict))

    def _faces(self, someobj):
        # polygons
        thevertices = someobj.vertices
        for face in someobj.faces:                
            # first corner
            v  = face[0]
            x0 = thevertices[v].xyz[0]
            y0 = thevertices[v].xyz[1]
            z0 = thevertices[v].xyz[2]
            firstcorner = "<%s, %s, %s>" % (x0, y0, z0)
            eachcorner = firstcorner

            for v in face[1:]: # the rest of 'em
                x0 = thevertices[v].xyz[0]
                y0 = thevertices[v].xyz[1]
                z0 = thevertices[v].xyz[2]
                eachcorner = eachcorner + ", <%s, %s, %s> " % (x0, y0, z0)
                
            eachcorner = eachcorner + ", " + firstcorner
            
            # POV-Ray closes polygon by repeating first corner
            fdict = dict(numcorners = len(face)+1,
                         eachcorner = eachcorner,
                         face_texture = someobj.face_texture)
            
            self.fileobject.write(gl_theface.substitute(fdict))
        
    def write(self):
        # set the stage
        self.fileobject = open(Scene.thepath + self.header['filename'], 'w')
        self.fileobject.write(gl_theheader.substitute(self.header))
        self.fileobject.write(gl_thesettings.substitute(self.settings))

        # write each object
        for obj in self.objects:
            if obj.showvertices:
                self._vertexes(obj)
            if obj.showedges:
                self._edges(obj)
            if obj.showfaces:
                self._faces(obj)
                
        self.fileobject.close()

def makecoupler():
    thecube = Cube()
    thecube.showfaces = False
    thecube.edge_texture = 'T_Chrome_2A'
    thecoupler = Coupler()
    output = Scene('test0.pov')
    output.objects.append(thecube)
    output.objects.append(thecoupler)
    output.write()
    
def makemite():
    thecube = Cube()
    thecube.showfaces = False
    thecube.edge_texture = 'T_Brass_3A'
    
    thecoupler = Coupler()    
    thecoupler.showfaces = False
    thecoupler.edge_texture = 'T_Chrome_2A'
    
    themite = Mite()
    themite.face_texture = 'T_Stone18'
    themite.edge_texture = 'T_Chrome_2A'
    
    output = Scene('test1.pov')
    output.settings['camy'] = 2.5
    
    output.objects.append(thecube)
    output.objects.append(thecoupler)
    output.objects.append(themite)
    output.write()

def maketent():
    output = Scene('test2.pov')    # naming disk file
    output.objects.append(Tetrahedron()) # appending Polyhedron object
    output.write()

def makeicosa():
    output = Scene('test3.pov')    # naming disk file
    # appending a scaled Polyhedron object
    output.objects.append( Icosahedron()  * sqrt(2) ) 
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
