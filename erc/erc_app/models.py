from django.db import models
from django.forms import ModelForm
import clips

# Create your models here.

class ConfigFile:
	filename = "erc_config.sh"

	@staticmethod
	def set_filename(fn):
		filename = fn

	@staticmethod
	def write(string_list, myfilename=None):
		if( myfilename == None):
			myfilename = filename
		with open(myfilename, 'a') as myfile:
			myfile.writelines(string_list)

class InterviewStream:
	env = clips.Environment()

	prompt = None
	choices = []
	cmds = []

	# utility function to be called from within CLIPS
	@staticmethod
	def setprompt(n,p,c):
		prompt = UserQueryForm(pk=n, query_text=p)
		prompt_name = n
		prompt = p
		choices = c
		return clips.String("ok")

	# utility function to be called from within CLIPS
	@staticmethod
	def addcmd(cmd):
		cmds.append(cmd)
		return clips.String("ok")

	@staticmethod
	def open(kbfile):
		env.ClearPythonFunctions()
		env.Clear()
		env.Load(kbfile)
		env.Reset()
		clips.DebugConfig.WatchAll()
		clips.DebugConfig.DribbleOn("pyclips.log")

		env.RegisterPythonFunction(setprompt)
		env.RegisterPythonFunction(addcmd)
		# env.RegisterPythonFunction(setcmd)

		return env, Interview.objects.create(created_at=DateTime.now)

	@staticmethod
	def next():
		rules_left = env.Run(1)
		if( rules_left > 0 ):
			if( choices.Count() > 0 ):
				# CLIPS has added some choices
				while( prompt == None and r > 0 ):
					rules_left = InterviewStream.next()
			elif( tmp_cmds.Count() > 0  ):
				while( cmds.Count() == 0 and r > 0 ):
					rules_left = InterviewStream.next()
		return rules_left


	@staticmethod
	def close():
		env.ClearPythonFunctions()
		env.Clear()
		env.Reset()

	@staticmethod
	def build_config(request):
		ConfigFile.write( cmds )

class Interview(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "Interview"

class InterviewQuestion(models.Model):
	interview = models.ForeignKey(Interview)
	query_text = models.CharField(max_length=255)

	def __unicode__(self):
		return self.query_text

class UserResponse(models.Model):
	POSSIBLE_ANSWERS = (
		("y", "YES"),
		("n", "NO"),
		("idk", "SKIP"))
	question = models.ForeignKey(InterviewQuestion)
	response = models.CharField(max_length=255, choices=POSSIBLE_ANSWERS)

class UserQueryForm(ModelForm):
	class Meta:
		model = UserResponse
