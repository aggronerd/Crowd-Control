from itertools import count

__author__ = 'greg'

from panda3d.core import GeomVertexData, GeomVertexFormat, GeomVertexWriter, Geom
from panda3d.core import GeomLinestrips, GeomNode, GeomTriangles, GeomEnums

class Polygon(object):

    vertices = []

    def addVertex(self, vertex):
        self.vertices[] = vertex

    def createPrimative(self):
        i = 0
        n = count(self.vertices)
        while i < n:
            node = DLLNode

            if(i == 0):
                v1 = self.vertices[n]
            else:
                v1 = self.vertices[i-1]
            v2 = self.vertices[i]
            if(i == (n - 1)):
                v3 = self.vertices[0]
            else:
                v3 = self.vertices[i+1]
            i += 1

    def __addTo

class DLLNode(object):

    next = None
    previous = None
    value = None

    def DLLNode(self, next, value):
        self.next = next
        self.value = value
        next.previous = self

