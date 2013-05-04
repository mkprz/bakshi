from django.db import models
import clips

# Create your models here.

class ConfigFile:
	filename = "erc_config.sh"

	@staticmethod
	def set_filename(fn):
		filename = fn

	@staticmethod
	def write(string_list, myfilename=None)
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
		return env

	@staticmethod
	def next:
		return env.Run(1)

	@staticmethod
	def close:
		env.ClearPythonFunctions()
		env.Clear()
		env.Reset()

	@staticmethod
	def set_feedback(selected_choice):
		fact_template = env.FindTemplate("response")
		f = fact_template.BuildFact()
		f.AssignSlotDefaults()
		for k in selected_choice.keys():
			f.Slots[k] = selected_choice[k]
		f.Assert()

class UserPrompt(models.Model):
	interview = models.ForeignKey(Interview)
	userprompt_text = models.CharField(max_length=1024)
	response = models.OneToOneField(Choice)

	def __unicode__(self):
		return self.userprompt_text

class Choice(models.Model):
	interview = models.ForeignKey(Interview)
	prompt = models.ForeignKey(Prompt)
	choice_text = models.CharField(max_length=1024)
	
	def __unicode__(self):
		return self.choice_text
