function my_ajax_error(event_source, xhr, status, error) {
	console.log("my_ajax_error");
	console.log("status: " + status);
	console.log("error: " + error);
}

function my_ajax_success(event_source, data, status, xhr) {
	var e = jQuery(event_source);
	console.log("my_ajax_success");
	console.log("status: " + status);
	console.log("data-target:" + e.data("target"));
	console.log("data-updatemode:" + e.data("updatemode"));
	var update_element = jQuery(e.data("target"));
	if( update_element ) {
		var update_mode = e.data("updatemode");
		switch( update_mode ) {
			case "append":
				update_element.append(data); break;
			case "prepend":
				update_element.prepend(data); break;
			case "before":
				update_element.before(data); break;
			case "after":
				update_element.after(data); break;
			default:
				update_element.html(data); break;
		}
	}
}
jQuery(document).delegate("[data-remote]", "ajax:complete", function(evnt, xhr, status) {
	console.log("caught: ajax:complete");
	console.log("status:" + status);
	console.log("response:" + xhr.responseText);
	if( status == "success" )
		my_ajax_success(this, xhr.responseText, status, xhr);
});

jQuery(document).delegate("[data-remote]", "ajax:beforeSend", function(evnt, xhr, settings) {
	console.log("caught: ajax:beforeSend");
	console.log(xhr);
	console.log(settings);
});
