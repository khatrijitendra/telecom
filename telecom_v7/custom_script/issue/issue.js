cur_frm.add_fetch('customer','customer_name','customer_name');
cur_frm.add_fetch('contact','mobile_no','phone');
cur_frm.add_fetch('contact','email_id','raised_by');
cur_frm.add_fetch("location_id","location_name", "location_name")



cur_frm.cscript.refresh = function(doc, cdt, cdn){
	set_notification_mode(doc.contact)
	for(i=0;i<user_roles.length;i++){
		if(user_roles[i]=="Technician"){
			$(".strong add-assignment").css("display", "none");
			$(".list-unstyled sidebar-menu form-assignments").hide();
		}
	}

}

cur_frm.cscript.onload = function(doc, cdt, cdn){
	/*
		Read Only Status
		Read Only Due Date for Technician
	*/
	set_notification_mode(doc.contact)
	
	for(i=0;i<user_roles.length;i++){
		if(user_roles[i]=="Technician"){
			$(".strong add-assignment").css("display", "none");
			$(".list-unstyled sidebar-menu form-assignments").hide();
			cur_frm.set_df_property("due_date","read_only",1);
			if(cur_frm.doc.status=="Closed" || cur_frm.doc.status=="Hold" ){
				cur_frm.set_read_only()	
			}

		}
	}
}

cur_frm.cscript.customer = function(doc, cdt, cdn){
	/*
		clear fields
		set the customer name
	*/

	doc.contact = "";
	doc.location_id = "";
	doc.raised_by = "";
	doc.phone = "";
	doc.contact_name = "";

	cur_frm.refresh_fields();
}

cur_frm.cscript.contact = function(doc, cdt, cdn){
	// get notification mode and set the checkbox
	set_notification_mode(doc.contact);
}

cur_frm.cscript.status = function(doc, cdt, cdn){
	if(doc.status == "Closed"){
		frappe.msgprint("You Cannot Close Issue Here,Close Issue From Timesheet");
		cur_frm.set_df_property("resolution_details","reqd",1)
		cur_frm.set_value("status",cur_frm.doc.old_status); 
		cur_frm.set_df_property("resolution_details","reqd",0)
	}
	else{
		cur_frm.set_df_property("resolution_details","reqd",0)
	}
	cur_frm.toggle_reqd("comment_for_hold", cur_frm.doc.status=="Hold");
}

// cur_frm.cscript.customer_address =function(doc, cdt, cdn) {
// 		erpnext.utils.get_address_display(this.frm, "customer_address");
// }

cur_frm.cscript.validate = function(frm){
	
}


cur_frm.fields_dict['location_id'].get_query = function(doc, cdt, cdn) {
	return {
		filters:{ 'customer': doc.customer }
	}
}

cur_frm.cscript.location_id =function(doc, cdt, cdn) {
				
	frappe.call({
			method:"frappe.client.get_list",
			args:{
				doctype:"Address",
				filters: [
							["name","=",cur_frm.doc.location_id],
						],
				fields: ["address_line1","address_line2","city","state","country"]
			},
			callback: function(r) {
				if (r.message) {
					console.log("add",r.message[0])
					var add = "<p>"+r.message[0]['address_line1']+"</p>"
							  +"<p>"+r.message[0]['address_line2']+"</p>"
							  +"<p>"+r.message[0]['city']+"</p>"
							  +"<p>"+r.message[0]['state']+"</p>"
							  +"<p>"+ r.message[0]['country']+"</p>"

					cur_frm.set_value("customer_address",add);		
				}
			}
	});		
		
}

cur_frm.fields_dict['contact'].get_query = function(doc, cdt, cdn) {
	return {
		filters:{
			// 'location_id': doc.location_id,
			'customer': doc.customer
		}
	}
}


set_notification_mode = function(contact){
	/*
		check the notification mode from Contact and checked the respective checkbox
	*/
	var mode = "";
	if(contact){
		// Get Contact doc 
		frappe.model.with_doc('Contact', contact, function() {
	  		d = frappe.model.get_doc('Contact', contact);
	  		mode = d.notification_mode;
	  		// Set the checkbox to checked state
	  		$('.is-email').prop('checked', mode == 'Via Email'? true: false);
			$('.is-sms').prop('checked', mode == 'Via SMS'? true: false);
			$('.is-both').prop('checked', mode == 'Both'? true: false);
			$('.is-comment').prop('checked',mode != 'Via Email' && mode != 'Via SMS' && mode != 'Both'?true:false);
		})

		cur_frm.refresh_fields();
	}
	else
		$('.is-comment').prop('checked',true);
}