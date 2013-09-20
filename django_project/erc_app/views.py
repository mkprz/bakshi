# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from erc_app.models import Choice, Prompt

prompt = None
choices = []
cmds = []
interview_session = None


# utility functions to be called from within CLIPS
def setprompt(n,p,c):
	prompt = UserQueryForm(pk=n, query_text=p)
	prompt_name = n
	prompt = p
	choices = c
	return clips.String("ok")

def addcmd(cmd):
	cmds.append(cmd)
	return clips.String("ok")

# def setcmd():
# 	cmds = tmp_cmds
# 	return clips.String("ok")

# view actions
def index(request):
	return render(request, 'erc_app/index.html')

def start_wizard(request):
	env = InterviewStream.open()
	env.RegisterPythonFunction(setprompt)
	env.RegisterPythonFunction(addcmd)
	# env.RegisterPythonFunction(setcmd)
	return HttpResponseRedirect( reverse('erc_app:sip_from_stream') )

def end_wizard(request):
	InterviewStream.close()
	return HttpResponseRedirect( reverse('erc_app:review') )

def sip_from_stream(request):
	r = InterviewStream.next()
	if( r == 0 ):
		# no rules left to activate; end wizard
		return HttpResponseRedirect( reverse('erc_app:end_wizard') )
	elif( choices.Count() > 0 ):
		# CLIPS has added some choices
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
	
# standard pattern for processing a form
# https://docs.djangoproject.com/en/1.5/topics/forms/#using-a-form-in-a-view
def query(request):
	if request.method == "POST":
		form = UserPromptForm(request.POST)
		if form.is_valid():
			up_id = form.cleaned_data['up_id']
			c_id = form.cleaned_data['c_id']
			up = get_object_or_404(UserPrompt, pk=up_id)
			up.selected_choice = up.choice_set.get(pk=c_id)
			up.save()
			return HttpResponseRedirect( reverse('erc_app:sip_from_stream') )	
	else:
		form = UserPromptForm( prompt. choices )

		#reset these variables
		prompt = None
		choices = []

	context = {'form': form}
	return render(request, 'erc_app/query.html', context)

def build_config(request):
	ConfigFile.write( cmds )
	return HttpResponseRedirect( reverse('erc_app:siphon_stream') )	
