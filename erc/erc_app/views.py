# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView

from erc_app.forms import KnowledgeBaseForm, DecisionForm, ConfigForm

# based on django tutorial
# https://docs.djangoproject.com/en/1.6/ref/contrib/formtools/form-wizard/
FORMS = [
	("kb", KnowledgeBaseForm),
	("decision_node", DecisionForm),
	("config", ConfigForm)]
TEMPLATES = {
	"kb": "kb_form.html",
	"decision_node": "formtools/wizard/wizard_form.html",
	"config": "config_form.html"}

def is_interview_done(wizard):
	# return true if interview is done (all rules exhausted in CLIPS)
	cleaned_data = wizard.get_cleaned_data_for_step('decision_node') or {'is_interview_done': '0'}
	return cleaned_data['is_interview_done'] == '0'

class BakshiWizard(SessionWizardView):
	# use different templates depending on step of wizard form
	# self.steps.current will be one of 'kb', 'decision_node', or 'config'

	# passed to as_view() in urls.py
	# if rules_active() returns true, then step will be 'decision_node'
	condition_dict = {'decision_node': is_interview_done}

	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

	def done(self, form_list, **kwargs):
		r = save_facts(form_list)
		if( r > 0 ):
			return HttpResponseRedirect('/next/')
		else:
			return HttpResponseRedirect('/review/')

def next(form_list):
	if( interview_session == None ):
		i = Interview()
	else:
		i = interview_session.reload()
	return i.next()


# standard pattern for processing a form
# https://docs.djangoproject.com/en/1.5/topics/forms/#using-a-form-in-a-view
def decide(request):
	if request.method == "POST":
		form = DecisionForm(request.POST)
		if form.is_valid():
			d_id = form.cleaned_data['d_id']
			c_id = form.cleaned_data['c_id']
			d = get_object_or_404(Decision, pk=d_id)
			d.selected_choice = d.choice_set.get(pk=c_id)
			d.save()
			return HttpResponseRedirect( reverse('erc_app:next') )
	else:
		form = DecisionForm( d.choice_set.all() )

	context = {'form': form}
	return render(request, 'erc_app/decision', context)

def build_config(request):
	ConfigFile.write( cmds )
	return HttpResponseRedirect( reverse('erc_app:next') )
