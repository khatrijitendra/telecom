cur_frm.add_fetch("issue","subject", "issue_subject")
cur_frm.add_fetch("issue","status", "issue_status")


/*cur_frm.cscript.validate = function(frm){
	
} */
cur_frm.cscript.validate = function(frm){
	
} 

cur_frm.cscript.onload = function(frm,cdt,cdn){
	if (cur_frm.doc.__islocal){
	 	frappe.call({
	 		method: "frappe.client.get_value",
			args: {
					doctype: "Employee",
					fieldname: "name",
					filters: { user_id: user },
					},
			callback:function(r)
			{
				cur_frm.set_value("employee",r.message.name); 
				
			}
		});
		
		frappe.call({
	 		method: "frappe.client.get_value",
			args: {
					doctype: "User",
					fieldname: "manager",
					filters: { name: user },
					},
			callback:function(r)
			{
				cur_frm.set_value("manager",r.message.manager);
					 
			}
		});
	}	
	var d  = locals[cdt][cdn]
	for(i=0;i<user_roles.length;i++){
		if(user_roles[i]=="Technician"){
			cur_frm.set_df_property(d.billable,"read_only",1);
			cur_frm.set_df_property(d.activity_type,"read_only",1);

		}
	}

	var d  = locals[cdt][cdn];
	console.log(d)
	cur_frm.set_df_property(d.hours,"read_only",1);
}

cur_frm.fields_dict['time_logs'].grid.get_field('issue').get_query = function(doc, cdt, cdn) {
     var issues=[];
    $.each(doc.time_logs, function(idx, val){
		issues.push(val.issue)
	})
	return { filters: [	
					['Issue','status', '!=',"Closed"],

				] 
			}
}

cur_frm.cscript.issue_status = function(frm,cdt,cdn){
	var d  = locals[cdt][cdn]
	console.log(d.resolution_details,d.issue_status)
	if(d.issue_status == "Open"){
		cur_frm.set_df_property(d.activity_type,"read_only",1);

	}

	
	//frm.fields_dict.time_logs.grid.toggle_reqd(d.resolution_details,d.issue_status =="Closed");
	//cur_frm.toggle_reqd(d.resolution_details,d.issue_status=="Closed")	
}

frappe.ui.form.on("Timesheet Detail", {
	time_logs_add: function(frm) {
		console.log("______")	
		cur_frm.get_field("fields").grid.toggle_reqd("issue", true);
		// var field = frappe.utils.filter_dict(cur_frm.fields_dict["time_logs"].grid.grid_rows_by_docname[cdn].docfields,{"fieldname": "issue"})[0];
		// console.log(field)
		// field.df.reqd = true;
		// field.refresh();
	},
});

