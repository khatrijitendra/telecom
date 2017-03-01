# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "telecom_v7"
app_title = "Telecom"
app_publisher = "Jitendra"
app_description = "Telecom Advocate"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "sangram.p@indictranstech.com"
app_license = "MIT"

# Includes in <head>
# ------------------
fixtures = ['Custom Field', 'Property Setter', "Print Format","Custom Script"]

calendars = ["Issue"] 

#boot_session = "telecom_v7.custom_script.issue.issue.boot_session"
# include js, css files in header of desk.html
# app_include_css = "/assets/telecom_v7/css/telecom_v7.css"
app_include_js = "/assets/js/telecom_v7.js"

# include js, css files in header of web template
# web_include_css = "/assets/telecom_v7/css/telecom_v7.css"
# web_include_js = "/assets/telecom_v7/js/telecom_v7.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "telecom_v7.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "telecom_v7.install.before_install"
# after_install = "telecom_v7.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "telecom_v7.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
permission_query_conditions = {
 "Issue": "telecom_v7.custom_script.issue.issue.get_permission_query_conditions",
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Customer": {
        "validate": "telecom_v7.custom_script.customer.customer.validate",
        "after_rename": "telecom_v7.custom_script.customer.customer.after_rename"
    },
    "Address": {
        "validate": "telecom_v7.custom_script.address.address.validate",
        "autoname": "telecom_v7.custom_script.address.address.autoname"
    },
    "Issue": {
        "validate": "telecom_v7.custom_script.issue.issue.validate"
    },
    "User": {
        "validate": "telecom_v7.custom_script.user.user.validate_employee_for_technician_role"
    }    
}    


doctype_js = {
    "Customer":["custom_script/customer/customer.js"],
    "Address":["custom_script/address/address.js"],
    "Contact":["custom_script/contact/contact.js"],
    "Issue":["custom_script/issue/issue.js"],
    "Timesheet":["custom_script/timesheet/timesheet.js"]
}

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"telecom_v7.tasks.all"
# 	],
# 	"daily": [
# 		"telecom_v7.tasks.daily"
# 	],
# 	"hourly": [
# 		"telecom_v7.tasks.hourly"
# 	],
# 	"weekly": [
# 		"telecom_v7.tasks.weekly"
# 	]
# 	"monthly": [
# 		"telecom_v7.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "telecom_v7.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "telecom_v7.event.get_events"
# }

