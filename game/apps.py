from libpanda import TextureStage
from direct.gui.DirectOptionMenu import DirectOptionMenu
from direct.gui.DirectSlider import DirectSlider
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile, Point2D, Point3, DirectionalLight, Vec3, AmbientLight, Vec4, Material, VBase4
from game.tasks.interface import CameraControlsTaskHandler, DebugInfoUpdateTaskHandler
from game.geo.primatives import TileSet, TileSquare
import direct.gui.DirectGuiGlobals as DGG
import sys

__author__ = 'greg'

##
# An abstract class representing an app used to contain the
# world and defining common HCI interactions for both.
class CrowdControlWorldApp(ShowBase):
	mouseWheelTicks = 0
	cameraControlsTaskHandler = None
	tilesets = []
	tiles = []

	def __init__(self):
		loadPrcFile("config/Config.prc")
		ShowBase.__init__(self)
		self.debugOnscreenText = OnscreenText(style=1, fg=(1,1,1,1), align=0 ,pos=(-1,-0.95), scale = .05, text="Test")
		self.setBackgroundColor(0.0,0.0,0.0)
		self._setupBasicCamera()
		self._setupKeyboardEvents()
		self._setupMouseEvents()
		self._setupCoreTasks()

	def _setupCoreTasks(self):
		self.debugInfoUpdateTaskHandler = DebugInfoUpdateTaskHandler(self)
		self.taskMgr.add(self.debugInfoUpdateTaskHandler.updateDebugOnscreenTextTask, "UpdateDebugOnscreenTextTask", priority=-1)

	def _setupBasicCamera(self):
		self.camera = self.makeCamera(self.win)
		self.camera.setPos(0, 0, 2)
		self.camera.setHpr(0, -95, 0)

	def _setupKeyboardEvents(self):
		self.accept("escape", sys.exit, [0])
		self.accept("wheel_up", self.onMouseWheelUp)
		self.accept("wheel_down", self.onMouseWheelDown)
		self.disableMouse()

	def _setupMouseEvents(self):
		self.cameraControlsTaskHandler = CameraControlsTaskHandler(self)
		self.taskMgr.add(self.cameraControlsTaskHandler.moveCameraTask, "MoveCameraTask", priority=-1)

	def onMouseWheelUp(self):
		self.mouseWheelTicks -= 1

	def onMouseWheelDown(self):
		self.mouseWheelTicks += 1

##
# The level editor
class CrowdControlLevelEditorApp(CrowdControlWorldApp):

	cursorZ = 0.0

	def __init__(self):

		CrowdControlWorldApp.__init__(self)

		self.modeTextObject = OnscreenText(style=1, fg=(1,1,1,1), pos=(0.8,-0.95), scale = .07, text="Test")
		self.modeMenuObject = DirectOptionMenu(text="options", pos=(-1.2,0.0,0.91), scale=0.1,items=["Select","Delete","Add"],initialitem=2,
			highlightColor=(0.65,0.65,0.65,1),command=self.onChangeEditorMode)
		self.floorLevelSlider = DirectSlider(range=(-100,100), pos=(-1.2,0.0,0.0), value=self.cursorZ, pageSize=0.5, \
			scale=0.6, command=self.onChangeFloorSliderValue, orientation=DGG.VERTICAL)

	# Callback function to set  text
	def onChangeEditorMode(self, arg):
		output = "Item Selected is: " + arg
		self.modeTextObject.setText(output)

	def onChangeFloorSliderValue(self):
		pass

	def createNewLevel(self):
		self.tilesets.append(TileSet('artwork/floor-tileset.png'))

	def updateCursorPosition(self):
		if self.mouseWatcherNode.hasMouse():
			x=self.mouseWatcherNode.getMouseX()
			y=self.mouseWatcherNode.getMouseY()

	def _createCursor(self):
		cursorObject = TileSquare(0,0,self.cursorZ)
		self.cursorNodePath = self.render.attachNewNode(cursorObject)
		self.cursorNodePath.hide()

		texture = self.loader.loadTexture('artwork/cursor.png')
		ts = TextureStage('ts')
		self.cursorNodePath.setTexture(ts, texture, 1)

app = CrowdControlLevelEditorApp()
app.run()
