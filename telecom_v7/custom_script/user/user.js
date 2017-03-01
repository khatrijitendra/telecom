cur_frm.fields_dict['manager'].set_query = function(doc) {
	return {
		filters: [
			["name","not", "in",[cur_frm.doc.name]]
		]
	}
}