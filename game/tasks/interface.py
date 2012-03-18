__author__ = 'greg'

from direct.task import Task
from game.tasks.core import TaskHandler

class DebugInfoUpdateTaskHandler(TaskHandler):

	def updateDebugOnscreenTextTask(self, task):
		if self.app.mouseWatcherNode.hasMouse():
			x=self.app.mouseWatcherNode.getMouseX()
			y=self.app.mouseWatcherNode.getMouseY()
		else:
			x='NULL'
			y='NULL'

		self.app.debugOnscreenText.setText("Mouse position is " + str(x) + "," + str(y))
		return Task.again

class CameraControlsTaskHandler(TaskHandler):

	##
	# Updates the camera position based on input from the user
	def moveCameraTask(self, task):

		if self.app.mouseWatcherNode.hasMouse():
			x=self.app.mouseWatcherNode.getMouseX()
			y=self.app.mouseWatcherNode.getMouseY()
			newPos=self.app.camera.getPos()

			#Set rate as 4.0 per second ensuring smooth scrolling
			rate = 3.0 * task.time

			#Adjust position
			if y < -0.9:
				newPos.setY(newPos.getY() - (abs(y+0.9)/0.1) * rate)
			elif y > 0.9:
				newPos.setY(newPos.getY() + (abs(y-0.9)/0.1) * rate)
			if x < -0.9:
				newPos.setX(newPos.getX() - (abs(x+0.9)/0.1) * rate)
			elif x > 0.9:
				newPos.setX(newPos.getX() + (abs(x-0.9)/0.1) * rate)

			#Adjust zoom
			newZ = newPos.getZ() + (float(self.app.mouseWheelTicks)*0.01)
			if 1.0 < newZ < 3.0:
				newPos.setZ(newZ)

			self.app.mouseWheelTicks = 0
			self.app.camera.setPos(newPos)

		return Task.again