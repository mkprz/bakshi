from django.db import models
import clips
from datetime import datetime

def startinterview():
	i = Interview()
	i.save()
	return clips.Integer(i.id)

# utility function to be called from within CLIPS
def setdecisionnode(interview_id, question, choices):
	i = Interview.objects.get(interview_id)
	i.set_next_node(question, choices)
	i.save()
	return clips.String("ok")

# utility function to be called from within CLIPS
def netcfg(interview_id, cfg_name):
	i = Interview.objects.get(interview_id)
	# call function with name cfg_name from module erc_kb
	i.add_cfg( getattr(erc_kb, cfg_name) )
	i.save()
	return clips.String("ok")

class Interview(models.Model):
	default_filename = "erc_config.sh"

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	config_text = models.TextField()

	def __unicode__(self):
		ustr = u''
		for decision in self.decision_set.all():
			ustr += u'%s\n' % (decision.decision_text)
		return ustr

	def open(self, kbfile):
		try:
			clips.ClearPythonFunctions()
			clips.RegisterPythonFunction(setprompt)
			clips.RegisterPythonFunction(addcmd)
			self.env = clips.Environment()
			self.env.Clear()
			self.env.Reset()
			self.env.DebugConfig.WatchAll()
			self.env.DebugConfig.DribbleOn("erc_app.pyclips.log")
			self.env.Load(kbfile)
			self.created_at = datetime.now()
			self.save()
		except clips.ClipsError:
			print clips.ErrorStream.Read()
		return self

	def next(self):
		try:
			rules_left = self.env.Run(1)
		except clips.ClipsError:
				print clips.ErrorStream.Read()

		if( rules_left > 0 ):
			if( self.choices.Count() > 0 ):
				# CLIPS has added some choices
				while( self.prompt == None and rules_left > 0 ):
					rules_left = next()
			elif( tmp_cmds.Count() > 0  ):
				while( self.cmds.Count() == 0 and rules_left > 0 ):
					rules_left = next()
		return rules_left


	def close(self):
		try:
			self.env.ClearPythonFunctions()
			self.env.Clear()
			self.env.Reset()
		except clips.ClipsError:
				print clips.ErrorStream.Read()

	def build_config(self, request):
		with open(default_filename, 'a') as myfile:
			myfile.writelines(config_text)

	def append_configuration(self, config_lines):
		config_text += config_lines

class Decision(models.Model):
	CHOICES = (
		("1", "A"),
		("2", "B"),
		("3", "Skip")
	)
	interview = models.ForeignKey(Interview)
	decision_text = models.CharField(max_length=255)
	user_response = models.CharField(max_length=255, choices=CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s:%s' % (self.query_text, self.response)
