from direct.showbase import ElementTree

__author__ = 'greg'

from panda3d.core import GeomVertexData, GeomVertexFormat, GeomVertexWriter, Geom
from panda3d.core import GeomLinestrips, GeomNode, GeomTriangles, GeomEnums, Triangulator
import elementtree.ElementTree

class Polygon(GeomNode):

	vertices = []

	def __init__(self, name):
		GeomNode.__init__(self, name)

	def addVertex(self, vertex):
		self.vertices.append(vertex)

	def reconstruct(self):
		trianglator = Triangulator()

		#Add vertices to the trianglator
		for vertex in self.vertices:
			trianglator.addPolygonVertex(trianglator.addVertex(vertex))
		
		trianglator.triangulate()

		#Prepare to create the primative
		self.vdata = GeomVertexData('floor', GeomVertexFormat.getV3n3cpt2(), Geom.UHStatic)
		vertexW = GeomVertexWriter(self.vdata, 'vertex')
		normalW = GeomVertexWriter(self.vdata, 'normal')
		colorW = GeomVertexWriter(self.vdata, 'color')
		texcoordW = GeomVertexWriter(self.vdata, 'texcoord')

		#Add vertices to the primative
		i = 0
		while i < trianglator.getNumVertices():
			vertex = trianglator.getVertex(i)
			vertexW.addData3f(vertex.x,vertex.y,0.0)
			normalW.addData3f(0,0,1)
			colorW.addData4f(0.1,0.1,0.1,0.5)
			texcoordW.addData2f(0.0, 1.0)	
			i+=1

		self.geom = Geom(self.vdata)

		#Add triangles to the primative
		i = 0
		print(trianglator.getNumTriangles())
		while i < trianglator.getNumTriangles():
			tri = GeomTriangles(Geom.UHStatic)
			tri.addVertices(trianglator.getTriangleV0(i),trianglator.getTriangleV1(i),trianglator.getTriangleV2(i))
			tri.closePrimitive()
			self.geom.addPrimitive(tri)
			i+=1

		self.addGeom(self.geom)

class Level(object):

	tilesets = []
	layers = []

	def load(self, filename):
		doc = ElementTree.parse(filename)
		assert doc.getroot().get

class WallTile(object):
	pass

class Tile(object):
	pass
