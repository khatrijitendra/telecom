cur_frm.fields_dict['location_id'].get_query = function(doc,cdt,cdn) {
	return {
		query: "telecom_v7.custom_script.address.address.get_customer_addresses",
		filters:{
			'customer': doc.customer
		}
	}
}