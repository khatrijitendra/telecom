from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname, getseries
from frappe.utils import cstr
from frappe import _

def validate(self, method=None):
	validate_values(self)
	# check if abbriviation is already taken
	is_duplicate_abbr(self)

def validate_values(self):
	if frappe.defaults.get_global_default('cust_master_name') == 'Naming Series' and not self.naming_series:
		frappe.throw(_("Series is mandatory"), frappe.MandatoryError)

def is_duplicate_abbr(self):
	# if abbr is duplicate then raise the error
	abbr_list = frappe.db.sql("""SELECT abbr FROM tabCustomer""", as_list = 1)
	if frappe.db.sql("""SELECT abbr FROM tabCustomer WHERE abbr = "%s" and name <> "%s" """%(self.abbr,self.name)):
		frappe.throw(_("Abbriviation {0} is already taken").format(self.abbr))

def after_rename(self, olddn, newdn, merge=False,method=None):
	set_field = ''
	if frappe.defaults.get_global_default('cust_master_name') == 'Customer Name':
		frappe.db.set(self, "customer_name", newdn)
		update_contact(self)
		set_field = ", customer_name=%(newdn)s"
		abbr = self.abbr#frappe.db.get_value("Customer",newdn,"abbr") + "-"
	update_customer_address(self,newdn, set_field,abbr)

def update_contact(self):
	frappe.db.sql("""update `tabContact` set customer_name=%s, modified=NOW()
		where customer=%s""", (self.customer_name, self.name))

def update_customer_address(self, newdn, set_field,abbr):
	frappe.errprint("inside telecom update_customer_address")
	# ERPNext
	# frappe.db.sql("""update `tabAddress` set address_title=%(newdn)s
	# 	{set_field} where customer=%(newdn)s"""\
	# 	.format(set_field=set_field), ({"newdn": newdn}))
	"""
		rename all the addresses
	"""
	# get all the addresses which needs to be rename
	condn = abbr + "%"
	addresses = frappe.db.sql("""SELECT name FROM tabAddress addr WHERE customer='%s' AND name NOT LIKE '%s' ORDER BY name ASC"""%(newdn, condn))

	for address in addresses:
		# rename the address
		current_series = abbr + getseries(abbr, 4, '')
		frappe.db.sql("""update `tabAddress` set location_id=%(current_series)s, name=%(current_series)s
			{set_field} where name=%(address)s""".format(set_field=set_field), ({"newdn": newdn, "current_series": current_series, "address":address}))


