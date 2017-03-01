from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
# from frappe.boot import get_bootinfo

# def boot_session(bootinfo):
# 	frappe.errprint(bootinfo)

def validate(self, method=None):
	if self.due_date:
		if self.due_date < self.opening_date:
			frappe.throw("Due Date can not be date in past")

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
