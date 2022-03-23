# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.user import get_system_managers
from frappe import _
from frappe.utils import get_link_to_form

class JobOpportunity(Document):
	pass

@frappe.whitelist()
def report(job, reason):
    system_managers = get_system_managers(only_name=True)
    user = frappe.db.get_value("User", frappe.session.user, "full_name")
    subject = _("User {0} has reported the job post {1}").format(user, job)
    args = {
        "job": job,
        "job_url": get_link_to_form("Job Opportunity", job),
        "user": user,
        "reason": reason
    }
    frappe.sendmail(
        recipients = system_managers,
        subject=subject,
        header=[subject, "green"],
        template = "job_report",
        args=args,
        now=True)
