from __future__ import unicode_literals
import frappe
from frappe import throw, _

def validate_employee_for_technician_role(doc, method=None):
	if "technician" in [d.role for d in doc.get("user_roles")]:
		if not doc.manager:
			frappe.msgprint(_("Please set Manager for this user to set technician Role"))
			doc.get("user_roles").remove(doc.get("user_roles", {"role": "technician"})[0])