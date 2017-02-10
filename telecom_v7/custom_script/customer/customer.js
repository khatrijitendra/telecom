cur_frm.cscript.refresh = function(doc, dt, dn) {
	if(doc.__islocal != 1){
		cur_frm.set_df_property("abbr", "read_only", 1);
	}
}