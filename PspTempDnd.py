from datetime import timedelta
import threading
import json
from core.commons import constants
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class PspTempDnd(AliceSkill):
	"""
	Author: poulsp
	Description: My own temporary dnd psptempdnd.
	"""

	_PUBLISH_WAIT_TIME = 1

	#-----------------------------------------------
	def __init__(self):
		super().__init__()
		self._timer = None
		self._siteList = list()


	#-----------------------------------------------
	def onStart(self):
		super().onStart()
		self._siteList = self.getConfig('siteList').split(',')


	#-----------------------------------------------
	@IntentHandler('startMyDnd')
	def startMyDnd(self, session: DialogSession, **_kwargs):
		self.ThreadManager.doLater(
			interval=PspTempDnd._PUBLISH_WAIT_TIME,
			func=self._publishDnd,
			args=[True]
		)
		#self.endDialog(session.sessionId, self.randomTalk('startMyDnd'))
		self.endDialog(session.sessionId, '')


	#-----------------------------------------------
	@IntentHandler('stopMyDnd')
	def stopMyDnd(self, session: DialogSession, **_kwargs):
		self.ThreadManager.doLater(
			interval=PspTempDnd._PUBLISH_WAIT_TIME,
			func=self._publishDnd,
			args=[False]
		)
		#self.endDialog(session.sessionId, self.randomTalk('stopMyDnd'))
		self.endDialog(session.sessionId, '')


	#-----------------------------------------------
	def _publishDnd(self, onOff: bool):
		if onOff:
			for siteId in self._siteList:
				self.publish(constants.TOPIC_HOTWORD_TOGGLE_OFF, payload=json.dumps({"siteId": siteId, "sessionId": ''}))
		else:
			for siteId in self._siteList:
				self.publish(constants.TOPIC_HOTWORD_TOGGLE_ON, payload=json.dumps({"siteId": siteId, "sessionId": ''}))

