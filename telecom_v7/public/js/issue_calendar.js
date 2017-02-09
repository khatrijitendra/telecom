frappe.views.calendar["Issue"] = {
	field_map: {
		"start": "due_date",
		"end": "due_date",
		"id": "name",
		"title": "subject",
		"status": "status",
	},
	style_map: {
		"Open": "info",
		"Closed": "success",
		"Replied": "info",
		"Hold": "warning"
	},
	//get_events_method: "erpnext.support.doctype.issue.issue.get_events"
	get_events_method: "telecom_v7.custom_script.issue.issue.get_events"
}