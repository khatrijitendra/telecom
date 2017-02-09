from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries

def autoname(self,method=None):
	frappe.errprint("inside autoname")
	if(self.customer):
		abbr = frappe.db.get_value("Customer",self.customer,"abbr")
		self.name = make_autoname(abbr + "-.####")
	else:
		if not self.address_title:
			self.address_title = self.customer \
				or self.supplier or self.sales_partner or self.lead

		if self.address_title:
			self.name = cstr(self.address_title).strip() + "-" + cstr(self.address_type).strip()
		else:
			throw(_("Address Title is mandatory."))

def validate(self,method=None):
	frappe.errprint("inside validate")
	if(self.customer):
		self.location_id = self.name

@frappe.whitelist()
def get_customer_addresses(doctype, txt, searchfield, start, page_len, filters):
	condition = ""
	if filters.get("customer"):
		condition = "customer='%(customer)s'"%filters
	else:
		condition = "customer<>''"

	return frappe.db.sql("""select name from tabAddress where name like '%(txt)s' and %(cond)s"""%{"cond":condition, 'txt': "%%%s%%" % txt})
	
@frappe.whitelist()
def get_address_display(address_dict):
	if not address_dict:
		return
	if not isinstance(address_dict, dict):
		address_dict = frappe.db.get_value("Address", address_dict, "*", as_dict=True) or {}

	template = frappe.db.get_value("Address Template", \
		{"country": address_dict.get("country")}, "template")
	if not template:
		template = frappe.db.get_value("Address Template", \
			{"is_default": 1}, "template")

	if not template:
		frappe.throw(_("No default Address Template found. Please create a new one from Setup > Printing and Branding > Address Template."))

	return frappe.render_template(template, address_dict)
