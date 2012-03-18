from libpanda import NodePath, PandaNode, LightRampAttrib, OrthographicLens, GeomNode, GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomTriangles, TextureStage, TransparencyAttrib, PointLight, Spotlight, PerspectiveLens
from direct.filter.CommonFilters import CommonFilters

__author__ = 'greg'

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from actors import Person
from panda3d.core import loadPrcFile, Point2D, Point3, DirectionalLight, Vec3, AmbientLight, Vec4, Material, VBase4
from pandac.PandaModules import AntialiasAttrib, TransparencyAttrib
from direct.gui.OnscreenText import OnscreenText
import sys

class Tile(GeomNode):

	def __init__(self, name, left, bottom, z = -1):
			self.left = left
			self.bottom = bottom
			self.z = z
			GeomNode.__init__(self, name)
			self.reconstruct()

	def reconstruct(self):

		#Prepare to create the primative
		self.vdata = GeomVertexData('tile', GeomVertexFormat.getV3n3cpt2(), Geom.UHStatic)

		vertexW = GeomVertexWriter(self.vdata, 'vertex')
		normalW = GeomVertexWriter(self.vdata, 'normal')
		colorW = GeomVertexWriter(self.vdata, 'color')
		texcoordW = GeomVertexWriter(self.vdata, 'texcoord')

		#Add vertices to the primative
		vertexW.addData3f(self.left, self.bottom, self.z)
		normalW.addData3f(0,0,1)
		colorW.addData4f(1.0,1.0,0.0,0.0)
		texcoordW.addData2f(0.0, 0.0)

		vertexW.addData3f(self.left, self.bottom + 0.064, self.z)
		normalW.addData3f(0,0,1)
		colorW.addData4f(1.0,1.0,0.0,0.0)
		texcoordW.addData2f(0.0, 1.0)

		vertexW.addData3f(self.left + 0.128, self.bottom + 0.064, self.z)
		normalW.addData3f(0,0,1)
		colorW.addData4f(1.0,1.0,0.0,0.0)
		texcoordW.addData2f(1.0, 1.0)

		vertexW.addData3f(self.left + 0.128, self.bottom, self.z)
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

class MyApp(ShowBase):

	mouseWheelTicks = 0

	def __init__(self):

		loadPrcFile("config/Config.prc")

		ShowBase.__init__(self)

		self.camera = self.makeCamera(self.win)

		#self.render.setAntialias(AntialiasAttrib.MMultisample)
		self.setBackgroundColor(0.0,0.0,0.0)

		#Mouse position text
		self.posText = OnscreenText(\
			style=1, fg=(1,1,1,1), pos=(0.8,-0.95), scale = .07)

		#self.toggleWireframe()
		self._setupKeyboardEvents()

		# Load and transform the panda actor.
		self.render.setTransparency(TransparencyAttrib.MAlpha)
		self.tile1 = Tile("tile1",0.0,0.0)
		node1 = self.render.attachNewNode(self.tile1)
		self.tile2 = Tile("tile2",0.064,0.032)
		node2 = self.render.attachNewNode(self.tile2)

		texture = self.loader.loadTexture('artwork/sample.png')
		#node.setTwoSided(True)
		ts = TextureStage('ts')
		#ts.setMode(TextureStage.MNormal)
		node1.setTexture(ts, texture, 1)
		node2.setTexture(ts, texture, 1)

		myMaterial = Material()
		myMaterial.setShininess(0.0) #Make this material shiny
		myMaterial.setAmbient(VBase4(0.0,0.0,0.0,1)) #Make this material blue
		node1.setMaterial(myMaterial)
		node2.setMaterial(myMaterial)

		self.camera.setPos(0, 0, 2)
		self.camera.setHpr(0, -95, 0)

		plight = PointLight('plight')
		plight.setColor(VBase4(0.8, 0.8, 0.2, 1))
		plnp = self.render.attachNewNode(plight)
		plnp.setPos(0.128, 0.064, -0.8)
		plight.setAttenuation(Point3(0.23, 0.23, 0.25))
		self.render.setLight(plnp)

		self.alight = self.render.attachNewNode(AmbientLight("Ambient"))
		self.alight.node().setColor(Vec4(0.1, 0.1, 0.1, 1))
		self.render.setLight(self.alight)

		self.render.setShaderAuto()

	def _setupKeyboardEvents(self):

		self.accept("escape", sys.exit, [0])
		self.accept("wheel_up", self.onMouseWheelUp)
		self.accept("wheel_down", self.onMouseWheelDown)
		self.disableMouse()

		self.taskMgr.add(self.moveCameraTask, "MoveCameraTask", priority=-1)

	def onMouseWheelUp(self):
		self.mouseWheelTicks -= 1

	def onMouseWheelDown(self):
		self.mouseWheelTicks += 1

	#Define a procedure to move the camera
	def moveCameraTask(self, task):

		if self.mouseWatcherNode.hasMouse():

			x=self.mouseWatcherNode.getMouseX()
			y=self.mouseWatcherNode.getMouseY()
			newPos=self.camera.getPos()

			self.posText.setText("Mouse: " + str(x) + "," + str(y))

			#Set rate as 4.0 per second ensuring smooth scrolling
			rate = 3.0*task.time

			#Adjust position
			if(y < -0.9):
				newPos.setY(newPos.getY() - (abs(y+0.9)/0.1) * rate)
			elif(y > 0.9):
				newPos.setY(newPos.getY() + (abs(y-0.9)/0.1) * rate)
			if(x < -0.9):
				newPos.setX(newPos.getX() - (abs(x+0.9)/0.1) * rate)
			elif(x > 0.9):
				newPos.setX(newPos.getX() + (abs(x-0.9)/0.1) * rate)

			#Adjust zoom
			newZ = newPos.getZ() + (float(self.mouseWheelTicks)*0.01)
			if newZ > 1.0 and newZ < 3.0:
				newPos.setZ(newZ)

			self.mouseWheelTicks = 0

			self.camera.setPos(newPos)

		return Task.again


app = MyApp()
app.run()
