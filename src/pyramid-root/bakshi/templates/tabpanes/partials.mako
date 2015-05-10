<%doc>
		partials for the tab-pane
		each block/def below is for each tab in a tab-pane
</%doc>

<%block name="home">
	<ol>
		<li>Open config file = jump to review tab-pane w/ option to apply, edit, or re-take wizconfig
		<li>New config file = start new wizconfig
		<li>View current config = jump to review tab-pane
	</ol>

	<div class="row">
		<a href="/wizconfig/start" data-remote="true" data-target="#interview_start" class="btn btn-primary pull-right">Ok, Let's Start!</a>
		<h2>${test_path}</h2>
	</div>
</%block>

<%block name="wizard_prompt">
		% if not interview is None:
			<form class="form-horizontal" action="/wizconfig/next/${interview.id}">
				<div class="form-label">
					<h2>${interview.prompt_text}</h2>
					% for choice in interview.csv_choices.split(","):
						<label class="control-label">
							<input type="radio" class="form-control" name="selected_choice" value="${choice}">${choice}<br/>
						</label>
					% endfor
				</div>
				<input type=submit />
			</form>
			<p><pre>${interview.watchtext}</pre></p>
		% else:
			No interview created!
		% endif
</%block>

<%block name="config_review">
		% if not interview is None:
			<p><pre>${interview.config_text}</pre></p>
		% else:
			No interview created!
		% endif
</%block>

<%block name="security">
		setup security, e.g., SSID, authentication, wifi security protocol, etc.
</%block>

<%block name="networking">
		dhcp, subnets, etc
</%block>

<%block name="performance">
		QoS, wifi channel, etc
</%block>

<%block name="everdayuse">
	backups, parental controls, guest wifi, sharing printers, NAS access, portforwarding
</%block>
