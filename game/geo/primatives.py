from libpanda import GeomNode, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom

__author__ = 'greg'

class TileSet(object):
	tileTypes = {}
	textureFilename = None

	def __init__(self, textureFilename):
		self.textureFilename = textureFilename

class TileType(object):

	tileSet = None
	name = ''
	width = 32
	height = 32
	posX = 0
	posY = 0

class TileSquare(GeomNode):

	def __init__(self, x, y, z = -1):
		self.x = x
		self.y = y
		self.z = z
		GeomNode.__init__(self)
		self._createGeometry()

	def _createGeometry(self):
		self.vdata = GeomVertexData('tile', GeomVertexFormat.getV3n3cpt2(), Geom.UHStatic)

		vertexW   = GeomVertexWriter(self.vdata, 'vertex')
		normalW   = GeomVertexWriter(self.vdata, 'normal')
		colorW    = GeomVertexWriter(self.vdata, 'color')
		texcoordW = GeomVertexWriter(self.vdata, 'texcoord')

		#Add vertices to the primative
		vertexW.addData3f(self.x, self.y, self.z)
		normalW.addData3f(0.0,0.0,1.0)
		colorW.addData4f(1.0,1.0,0.0,0.0)
		texcoordW.addData2f(0.0, 0.0)

		vertexW.addData3f(self.x, self.y + 0.128, self.z)
		normalW.addData3f(0,0,1)
		colorW.addData4f(1.0,1.0,0.0,0.0)
		texcoordW.addData2f(0.0, 1.0)

		vertexW.addData3f(self.x + 0.128, self.y + 0.128, self.z)
		normalW.addData3f(0,0,1)
		colorW.addData4f(1.0,1.0,0.0,0.0)
		texcoordW.addData2f(1.0, 1.0)

		vertexW.addData3f(self.x + 0.128, self.y, self.z)
		normalW.addData3f(0,0,1)
		colorW.addData4f(1.0,1.0,0.0,0.0)
		texcoordW.addData2f(1.0, 0.0)

		self.geom = Geom(self.vdata)

		tri1 = GeomTriangles(Geom.UHStatic)
		tri1.addVertices(2,1,0)
		tri1.closePrimitive()
		self.geom.addPrimitive(tri1)

		tri2 = GeomTriangles(Geom.UHStatic)
		tri2.addVertices(0,3,2)
		tri2.closePrimitive()
		self.geom.addPrimitive(tri2)

		self.addGeom(self.geom)

class Tile(TileSquare):
	pass