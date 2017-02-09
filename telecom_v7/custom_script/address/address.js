frappe.ui.form.on("Address", "refresh", function(cur_frm) {
	is_customer(cur_frm.doc)
});

cur_frm.cscript.customer = function(doc){
	is_customer(doc);
}

cur_frm.cscript.validate = function(doc){
	is_customer(doc);
}

is_customer = function(doc){
	// If customer the hide fields
	if(doc.customer){
		doc.address_title = "";
		cur_frm.set_df_property("location_name", "reqd", 1);
		cur_frm.set_df_property("address_title", "read_only", 1);
	}
	else{
		// unhide fields and set customer and customer name to null
		doc.customer = "";
		doc.customer_name = "";
		doc.location_id = "";
		cur_frm.set_df_property("location_name", "reqd", 0);
	}
	cur_frm.refresh_fields();
}
