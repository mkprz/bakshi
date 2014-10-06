from django import forms
from erc_app.models import Decision

class DecisionForm(forms.ModelForm):
	decision_text = forms.CharField(max_length=255)
	# user_response = forms.
	class Meta:
		model = Decision

class KnowledgeBaseForm(forms.Form):
	kb_file_name = forms.CharField(max_length=255)

class ConfigForm(forms.Form):
	cfg_file_name = forms.CharField(max_length=255)
