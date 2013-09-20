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

	@staticmethod
	def open(kbfile):
		env.ClearPythonFunctions()
		env.Clear()
		env.Load(kbfile)
		env.Reset()
		clips.DebugConfig.WatchAll()
		clips.DebugConfig.DribbleOn("pyclips.log")
		return env, Interview.objects.create(created_at=DateTime.now)

	@staticmethod
	def next():
		return env.Run(1)

	@staticmethod
	def close():
		env.ClearPythonFunctions()
		env.Clear()
		env.Reset()

class Interview(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "Interview"

class UserQuery(models.Model):
	POSSIBLE_ANSWERS = (
		("y", "YES"),
		("n", "NO"),
		("idk", "SKIP"))
	interview = models.ForeignKey(Interview)
	query_name = models.CharField(max_length=1024, primary_key=True)
	query_text = models.CharField(max_length=1024)
	response = models.CharField(choices=POSSIBLE_ANSWERS)

	def __unicode__(self):
		return self.query_text

class UserQueryForm(ModelForm):
	class Meta:
		model = UserQuery