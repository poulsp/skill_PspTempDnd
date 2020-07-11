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
	def _publishDnd(self, onOff: bool):
		if onOff:
			for siteId in self._siteList:
				self.publish(constants.TOPIC_HOTWORD_TOGGLE_OFF, payload=json.dumps({"siteId": siteId, "sessionId": ''}))
		else:
			for siteId in self._siteList:
				self.publish(constants.TOPIC_HOTWORD_TOGGLE_ON, payload=json.dumps({"siteId": siteId, "sessionId": ''}))


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
	@IntentHandler('activateWakeWord')
	def activateWakeWord(self, session: DialogSession, **_kwargs):
		room 	= 'kitchen' if 'Room' not in session.slots else session.slots['Room']

		wakeWord = {"siteId":room,"modelId":"hey_snips","modelVersion":"workflow-hey_snips_subww_feedback_10seeds-2018_12_04T12_13_05_evaluated_model_0002","modelType":"universal","currentSensitivity":0.5,"detectionSignalMs":1594070704748,"endSignalMs":1594070704748}

		self.publish(constants.TOPIC_HOTWORD_DETECTED, payload=json.dumps(wakeWord))

		self.endDialog(session.sessionId, '')
