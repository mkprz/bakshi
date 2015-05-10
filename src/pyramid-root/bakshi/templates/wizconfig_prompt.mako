<%inherit file="wizconfig.mako"/>

<%doc>
	include blocks/defs from other files
</%doc>
<%namespace name="tabpanes" file="tabpanes/partials.mako"/>

<%def name="head_includes()">
</%def>

<%def name="javascript_includes()">
</%def>

<%block name="home">
	<h1>ERC Wizard</h1>
	% if rules_fired > 0:
		${tabpanes.wizard_prompt()}
	% else:
		${tabpanes.config_review()}
	% endif
</%block>
