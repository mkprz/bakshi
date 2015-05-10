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
	<h1>Configuration Review</h1>
	${tabpanes.config_review()}
</%block>
