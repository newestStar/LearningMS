from __future__ import unicode_literals
import frappe
from frappe import _

def execute():
    frappe.reload_doc("lms", "doctype", "lms_batch_membership")
    memberships = frappe.get_all("LMS Batch Membership", ["member", "name"])
    for membership in memberships:
        email = frappe.db.get_value("Community Member", membership.member, "email")
        frappe.db.set_value("LMS Batch Membership", membership.name, "member", email)
