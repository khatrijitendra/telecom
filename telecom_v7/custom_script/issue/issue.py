from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from datetime import date,datetime
import datetime
from datetime import date
from datetime import timedelta

# from frappe.boot import get_bootinfo

# def boot_session(bootinfo):
# 	frappe.errprint(bootinfo)

def validate(self, method=None):
	#finalize_timesheet_on_thursday()
	if self.due_date:
		if self.due_date < self.opening_date:
			frappe.throw("Due Date can not be date in past")
	if self.old_status != self.status:
		self.old_status = self.status
	if self.name:
		if self.status =="Hold":
			assign_back_to_manager(self.name,self.raised_by,self.status,self.comment_for_hold)
	if self.referenced_timesheet:
		update_timesheet_issue(self.referenced_timesheet,self.name,self.status,self.old_status)
	
def on_update(self, method=None):
	issue = frappe.get_doc("Issue",self.name)
	if issue and self.status != issue.status:
		# roles = frappe.get_roles(frappe.session.user)
		if "Technician" in roles:
			send_status_notification_to_manager(self.owner,self.customer,self.name,self.location_id,self.status)
 			send_status_notification(self.customer,self.name,self.location_id,self.status)
 		if "Telecom Manager" in roles:
 			send_status_notification(self.customer,self.name,self.location_id,self.status)

def update_timesheet_issue(referenced_timesheet,issue_name,status,old_status):
	timesheet_doc = frappe.get_doc("Timesheet",referenced_timesheet)
	time_logs = timesheet_doc.time_logs
	for row in time_logs:
		if row.issue == issue_name and row.issue_status != status:
			row.update({
				"issue_status": status
			})
		else:
			print "Not Changed"
	#time_logs.save()
	timesheet_doc.save(ignore_permissions = True)
	
def assign_back_to_manager(name,raised_by,status,comment_for_hold):
	todo_doc = frappe.new_doc("ToDo")
	todo_doc.owner = raised_by
	todo_doc.reference_type = "Issue"
	todo_doc.reference_name = name
	todo_doc.assigned_by = frappe.session.user
	todo_doc.description = comment_for_hold
	todo_doc.save(ignore_permissions = True)
	print "assigne--",todo_doc.description

@frappe.whitelist()
def get_events(start, end):
	#frappe.errprint("inside my calendar")
	events = []
	add_issues(events, start, end)
	return events

def add_issues(events, start, end):
	query = """select name, subject, opening_date, due_date,
		status, docstatus
		from `tabIssue` where
		(opening_date between %s and %s or due_date between %s and %s)"""

	for d in frappe.db.sql(query, (start, end, start, end), as_dict=True):
		e = {
			"name": d.name,
			"doctype": "Issue",
			"opening_date": d.opening_date,
			"due_date": d.due_date,
			"status": d.status,
			"subject": d.subject,
			"docstatus": d.docstatus
		}
		if e not in events:
			events.append(e)

@frappe.whitelist()
def get_permission_query_conditions(user):
	roles = frappe.get_roles(user)
	names=[]
	if "Technician" in roles:
		reference_names=frappe.get_all("ToDo",fields='reference_name', filters={'owner':user})
		for i in range(0,len(reference_names)):
			names.insert(i,reference_names[i]["reference_name"]) 
		list2 = tuple([x.encode('UTF8') for x in list(names) if x])
		cond="";
		if len(list2)>1:
			cond = "in {0}".format(list2)
		if len(list2)==1:
			cond = "= '{0}'".format(list(list2)[0])
		if "Technician" in roles:
			#frappe.db.sql("""select name from `tabIssue` where name {0}""".format(cond),as_list=1,debug=1)
			return "`tabIssue`.name {0}".format(cond);
	if "Telecom Manager" in roles:
		cond="= '{0}'".format(user)
		return "`tabIssue`.owner {0}".format(cond);

@frappe.whitelist()
def send_status_notification(customer,Issue_name,location_id,status):
	email=frappe.db.get_value("Contact",{"location_id": location_id, "customer": customer},"email_id")
	frappe.sendmail(
				recipients=email,
				sender=frappe.session.user,
				subject=Issue_name+" Status",
				message=frappe.render_template("templates/email/status_notification.html", {"Name":customer,"Issue_name": Issue_name,"status":status}) 
		)

def send_status_notification_to_manager(owner,customer,Issue_name,location_id,status):
	manager_name=frappe.db.get_value("User",{"name":owner},"first_name")
	frappe.sendmail(
				recipients=owner,
				sender=frappe.session.user,
				subject=Issue_name+" Status",
				message=frappe.render_template("templates/email/status_notification_to _manager.html", {"Name":manager_name,"Issue_name": Issue_name,"customer":customer,"status": status,"user":frappe.session.user}) 
	)

@frappe.whitelist()
def finalize_timesheet_on_thursday():
	if frappe.utils.data.get_datetime("2017-03-14 23:59:59").strftime('%A') == "Tuesday":
		cur_thursday=frappe.utils.data.get_datetime("2017-03-14 23:59:59")
		print "cur_thursday",frappe.utils.data.now_datetime()
	today = frappe.utils.data.now_datetime()
	offset = (today.weekday() - 5) % 7
	last_friday = today - timedelta(days=offset)
	if last_friday.strftime('%A') == "Friday":
		print "last_friday",last_friday
		print  "Day",last_friday.strftime('%A')

	issues = frappe.db.sql("""select iss.`name` from `tabIssue` as iss 
									where iss.due_date between %(last_friday)s and %(cur_thursday)s 
									""",{"last_friday":last_friday,"cur_thursday":cur_thursday},as_dict=True,debug=1)
	print "Closed_issue",issues
	timesheet_dic={}
	closed_timesheet=[] 
	for i in issues:
		issue_doc = frappe.get_doc("Issue",i['name'])
		if issue_doc and issue_doc.referenced_timesheet:
			if timesheet_dic and issue_doc.referenced_timesheet in timesheet_dic.keys():
				timesheet_dic[issue_doc.referenced_timesheet].append(issue_doc.name+'-'+issue_doc.status)
			else:	
				timesheet_dic[issue_doc.referenced_timesheet] = [issue_doc.name+'-'+issue_doc.status]
		
 	for timesheet in timesheet_dic:
 		flag=0
		print timesheet
		for issue in timesheet_dic[timesheet]:
			if issue.split("-")[-1]=="Closed":
				flag=1
				print "values",issue.split("-")[-1]
			else:
				 break;

		if flag==1:
				closed_timesheet.append(timesheet)

	print "closed_timesheet",closed_timesheet 
	for timesheet in closed_timesheet:
		issue = frappe.db.get_value("Issue",{"referenced_timesheet": timesheet},"name")
		if issue:
			closed_issue_doc=frappe.get_doc("Issue",issue)
			technician_user=frappe.db.get_value("ToDo",{"reference_name": issue},"owner")
			if technician_user:
				todo_doc = frappe.new_doc("ToDo")
				todo_doc.owner = closed_issue_doc.raised_by
				todo_doc.reference_type = "Timesheet"
				todo_doc.reference_name = timesheet
				todo_doc.assigned_by = technician_user
				todo_doc.description = "Finalize"+" " +timesheet
				todo_doc.save(ignore_permissions = True)
				print "assigne--",todo_doc.description


	
