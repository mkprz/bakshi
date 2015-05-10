<%inherit file="base.mako"/>

<%doc>
	include blocks/defs from other files
</%doc>
<%namespace name="tabpanes" file="tabpanes/partials.mako"/>

<%def name="head_includes()">
</%def>

<%def name="javascript_includes()">
	<script>
		jQuery("#navbar .nav li").removeClass("active");
		jQuery("#navbar .nav li:last").addClass("active");
	</script>
</%def>

<!-- body -->
<div class="row" role="tab-panel">

	<div class="col-sm-2">
		<!-- Nav tabs -->
		<ol class="nav nav-pills nav-stacked" role="tablist">
			<li role="presentation" class="active"><a href="#interview_start" aria-controls="interview_start" role="tab" data-toggle="tab">Start</a></li>
			<li role="presentation"><a href="#security" aria-controls="security" role="tab" data-toggle="tab">Security</a></li>
			<li role="presentation"><a href="#networking" aria-controls="networking" role="tab" data-toggle="tab">Networking</a></li>
			<li role="presentation"><a href="#performance" aria-controls="performance" role="tab" data-toggle="tab">Performance</a></li>
			<li role="presentation"><a href="#everdayuse" aria-controls="everdayuse" role="tab" data-toggle="tab">Everyday Use</a></li>
		</ol>
	</div>

	<div class="col-sm-10">

		<!-- Tab panes -->
		<div class="tab-content">

			<div role="tabpanel" class="tab-pane active" id="interview_start">
				<%block name="home">
					${tabpanes.home()}
				</%block>
			</div>

			<div role="tabpanel" class="tab-pane" id="security">
				<%block name="security">
					${tabpanes.security()}
				</%block>
			</div>

			<div role="tabpanel" class="tab-pane" id="networking">
				<%block name="networking">
					${tabpanes.networking()}
				</%block>
			</div>

			<div role="tabpanel" class="tab-pane" id="performance">
				<%block name="performance">
					${tabpanes.performance()}
				</%block>
			</div>

			<div role="tabpanel" class="tab-pane" id="everdayuse">
				<%block name="everdayuse">
					${tabpanes.everdayuse()}
				</%block>
			</div>

		</div>

	</div>
</div>
