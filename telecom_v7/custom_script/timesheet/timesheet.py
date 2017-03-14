from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
import json


def on_update(self, method=None):			
	if self.name:
		print "\nonupdate",self.name
		if self.time_logs:
			pass
			update_issues(self.time_logs,self.name)
			update_issues_detail(self.time_logs,self.name)

def update_issues(time_logs,timesheet_name):	
	# Updating referenced_issue field from issue
	for row in time_logs:
		issue_doc = frappe.get_doc("Issue",row.issue)
		if not issue_doc.referenced_timesheet:
			frappe.db.set_value("Issue",row.issue,"referenced_timesheet",timesheet_name)
			
def update_issues_detail(time_logs,timesheet_name):
	for row in time_logs:
		issue_doc = frappe.get_doc("Issue",row.issue)
		if issue_doc.status != row.issue_status and issue_doc.referenced_timesheet == timesheet_name:
			if row.issue_status == "Replied" :
				frappe.db.set_value("Issue",row.issue,"status",row.issue_status)
			else:
					print "\nelse"
					if row.issue_status == "Hold":
						frappe.db.set_value("Issue",row.issue,"status",row.issue_status)
						frappe.db.set_value("Issue",row.issue,"comment_for_hold",row.comment_for_hold)
						assign_back_to_manager(row.issue,row.issue_status,row.comment_for_hold)
						print "\n\nON HOLD\n"
					if row.issue_status =="Closed":
						frappe.db.set_value("Issue",row.issue,"status",row.issue_status)
						frappe.db.set_value("Issue",row.issue,"resolution_details",row.resolution_details)

def assign_back_to_manager(name,status,comment_for_hold):
	issue_doc = frappe.get_doc("Issue",name)
	todo_doc = frappe.new_doc("ToDo")
	todo_doc.owner = issue_doc.raised_by
	todo_doc.reference_type = "Issue"
	todo_doc.reference_name = name
	todo_doc.assigned_by = frappe.session.user
	todo_doc.description = comment_for_hold
	todo_doc.save(ignore_permissions = True)
	print "assigne--",todo_doc.description

@frappe.whitelist()
def get_permission_query_conditions(user):
	roles = frappe.get_roles(user)
	employee=frappe.db.get_value("Employee",{"user_id": user},"name")
	if "Technician" in roles:
		return "`tabTimesheet`.employee = '{0}'".format(employee);
	if "Telecom Manager" in roles:
		reference_names=frappe.get_all("ToDo",fields='reference_name', filters={'owner':user})
		names=[]
		for i in range(0,len(reference_names)):
			names.insert(i,reference_names[i]["reference_name"])
		print names
		list2 = tuple([x.encode('UTF8') for x in list(names) if x])
		cond="";
		if len(list2)>1:
			cond = "in {0}".format(list2)
		if len(list2)==1:
			cond = "= '{0}'".format(list(list2)[0]) 
		return "`tabTimesheet`.name {0}".format(cond);


				
