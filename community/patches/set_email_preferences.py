from __future__ import unicode_literals
import frappe

def execute():
	members = frappe.get_all("Community Member", ["name", "email_preference"])
	for member in members:
		if not member.email_preference:
			frappe.db.set_value("Community Member", member.name, "email_preference", "Email on every Message")