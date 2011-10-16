__author__ = 'greg'

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from actors import Person
from panda3d.core import loadPrcFile, Point2D, Point3, DirectionalLight, Vec3, AmbientLight, Vec4, Material, VBase4
from pandac.PandaModules import AntialiasAttrib
from direct.gui.OnscreenText import OnscreenText
import environment
import sys

class MyApp(ShowBase):

	mouseWheelTicks = 0

	def __init__(self):

		loadPrcFile("config/Config.prc")

		ShowBase.__init__(self)

		self.render.setAntialias(AntialiasAttrib.MMultisample)
		self.setBackgroundColor(0,0,0)

		#Mouse position text
		self.posText = OnscreenText(
				text="",
				style=1, fg=(1,1,1,1), pos=(0.8,-0.95), scale = .07)

		#Environment
		self.floor = environment.Polygon("floor1")
		self.floor.addVertex(Point2D(40,-40))
		self.floor.addVertex(Point2D(40,40))
		self.floor.addVertex(Point2D(-60,40))
		self.floor.addVertex(Point2D(-60,10))
		self.floor.addVertex(Point2D(-40,10))
		self.floor.addVertex(Point2D(-40,-40))
		self.floor.reconstruct()
		node = self.render.attachNewNode(self.floor)

		myMaterial = Material()
		myMaterial.setShininess(5.0) #Make this material shiny
		myMaterial.setEmission(VBase4(0.6,0.6,0.6,1))
		myMaterial.setAmbient(VBase4(0.2,0.2,0.2,1)) #Make this material blue1

		node.setMaterial(myMaterial)

		# Capture keyboard events
		self.accept("escape", sys.exit, [0])
		self.accept("wheel_up", self.onMouseWheelUp)
		self.accept("wheel_down", self.onMouseWheelDown)
		self.disableMouse()
		#self.toggleWireframe();

		# Add the sinCamberTask procedure to the task manager
		self.taskMgr.add(self.moveCameraTask, "MoveCameraTask", priority=-1)

		# Load and transform the panda actor.
		self.pandaActor = Person()
		self.pandaActor.reparentTo(self.render)

		self.camera.setPos(0, -30, 50)
		self.camera.setHpr(0, -60, 0)

		self.alight = self.render.attachNewNode(AmbientLight("Ambient"))
		self.alight.node().setColor(Vec4(0.3, 0.3, 0.3, 1))
		self.render.setLight(self.alight)

		self.render.setShaderAuto()

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
			rate = 12.0*task.time

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
			newPos.setZ(newPos.getZ() + (float(self.mouseWheelTicks)*2.0))
			self.mouseWheelTicks = 0

			self.camera.setPos(newPos)

		return Task.again


app = MyApp()
app.run()
