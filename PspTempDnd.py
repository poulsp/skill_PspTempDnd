from datetime import timedelta
import threading
import json
from core.commons import constants
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
from core.util.Decorators import MqttHandler


class PspTempDnd(AliceSkill):
	"""
	Author: poulsp
	Description: My own temporary dnd psptempdnd.
	"""

	_PUBLISH_WAIT_TIME = 1
	_ACTIVATE_WAKEWORD = 'psp/activateWakeWord'
	_DND 				= 'psp/dnd'
	_CANCEL_DND = 'psp/cancelDnd'


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


	def _doLater(self, onOff):
		self.ThreadManager.doLater(
			interval=PspTempDnd._PUBLISH_WAIT_TIME,
			func=self._publishDnd,
			args=[onOff]
		)


	#-----------------------------------------------
	@IntentHandler('startMyDnd')
	def startMyDnd(self, session: DialogSession, **_kwargs):
		self._doLater(True)
		#self.endDialog(session.sessionId, self.randomTalk('startMyDnd'))
		self.endDialog(session.sessionId, '')


	#-----------------------------------------------
	@IntentHandler('stopMyDnd')
	def stopMyDnd(self, session: DialogSession, **_kwargs):
		self._doLater(False)
		#self.endDialog(session.sessionId, self.randomTalk('stopMyDnd'))
		self.endDialog(session.sessionId, '')


	#-----------------------------------------------
	@MqttHandler(_DND)
	def _activateDnd(self, session: DialogSession, **_kwargs):
		self._doLater(True)


	#-----------------------------------------------
	@MqttHandler(_CANCEL_DND)
	def _cancelDnd(self, session: DialogSession, **_kwargs):
		self._doLater(False)


	#-----------------------------------------------
	@MqttHandler(_ACTIVATE_WAKEWORD)
	def _activateWakeWord(self, session: DialogSession, **_kwargs):
		siteId = session.payload['siteId']

		wakeWord = {"siteId":siteId,"modelId":"hey_snips","modelVersion":"workflow-hey_snips_subww_feedback_10seeds-2018_12_04T12_13_05_evaluated_model_0002","modelType":"universal","currentSensitivity":0.5,"detectionSignalMs":1594070704748,"endSignalMs":1594070704748}

		self.publish(constants.TOPIC_HOTWORD_DETECTED, payload=json.dumps(wakeWord))




