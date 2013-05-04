# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from erc_app.model import Choice, Prompt

choices = []
prompt = None
tmp_cmds = []
cmds = []

""" utility functions to be called from within CLIPS
def addchoice(c):
	choices.append(c)
	return clips.String("ok")
def setprompt(n,q,c):
	prompt_name = n
	prompt = p
	choices = c
	return clips.String("ok")
def addcmd(c)
	cmds.append(cmd)
	return clips.String("ok")
def setcmd():
	cmds = tmp_cmds
	return clips.String("ok)


def index(request):
	return render(request, 'erc_app/index.html')

def start_wizard(request):
	env = InterviewStream.open()
	env.RegisterPythonFunction(addchoice)
	env.RegisterPythonFunction(setprompt)
	env.RegisterPythonFunction(addcmd)
	env.RegisterPythonFunction(setcmd)
	return HttpResponseRedirect( reverse('erc_app:siphon_stream') )

def end_wizard(request):
	InterviewStream.close()
	return HttpResponseRedirect( reverse('erc_app:review') )

def siphon_stream(request):
	r = InterviewStream.next()
	if( r == 0 ):
		return HttpResponseRedirect( reverse('erc_app:end_wizard') )
	elif( choices.Count() > 0 ):
		while( prompt == None and r > 0 ):
			r = InterviewStream.next()
		if( r == 0 ):
			return HttpResponseRedirect( reverse('erc_app:end_wizard') )
		else:
			return HttpResponseRedirect( reverse('erc_app:query') )
	elif( tmp_cmds.Count() > 0  ):
		while( cmds.Count() == 0 and r > 0 ):
			r = InterviewStream.next()
		if( r == 0 ):
			return HttpResponseRedirect( reverse('erc_app:end_wizard') )
		else:
			return HttpResponseRedirect( reverse('erc_app:build_config') )
	else:
		return HttpResponseRedirect( reverse('erc_app:siphon_stream') )
	
def query(request):
	up = UserPrompt.objects.create( userprompt_text=prompt )
	for c in choices:
		Choice.objects.create( userprompt=up, choice_text=c )

	""" reset these variables
	prompt = None
	choices = []

	context = {'userprompt': up}
	return render(request, 'erc_app/query.html', context)

def query_response(request):
	up_id = request.POST['up_id']
	c_id = request.POST['c_id]
	up = get_object_or_404(UserPrompt, pk=up_id)
	c = get_object_or_404(Choice, pk=c_id)
	up.selected_choice = up.choice_set.get(pk=c_id)
	up.save()

	InterviewStream.give_feedback(up)

	return HttpResponseRedirect( reverse('erc_app:siphon_stream') )	

def build_config(request):
	ConfigFile.write( cmds )
	return HttpResponseRedirect( reverse('erc_app:siphon_stream') )	
