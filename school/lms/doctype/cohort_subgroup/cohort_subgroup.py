# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import random_string

class CohortSubgroup(Document):
    def before_save(self):
        if not self.invite_code:
            self.invite_code = random_string(8)

    def get_invite_link(self):
        cohort = frappe.get_doc("Cohort", self.cohort)
        return f"{frappe.utils.get_url()}/courses/{self.course}/join/{cohort.slug}/{self.slug}/{self.invite_code}"

    def has_student(self, email):
        """Check if given user is a student of this subgroup.
        """
        q = {
            "doctype": "Cohort Student",
            "subgroup": self.name,
            "email": email
        }
        return frappe.db.exists(q)

    def has_join_request(self, email):
        """Check if given user is a student of this subgroup.
        """
        q = {
            "doctype": "Cohort Join Request",
            "subgroup": self.name,
            "email": email
        }
        return frappe.db.exists(q)

    def get_join_requests(self, status="Pending"):
        q = {
            "subgroup": self.name,
            "status": status
        }
        return frappe.get_all("Cohort Join Request", filters=q, fields=["*"], order_by="creation")

    def get_mentors(self):
        emails = frappe.get_all("Cohort Mentor", filters={"subgroup": self.name}, fields=["email"], pluck='email')
        return [frappe.get_doc("User", email) for email in emails]

    def get_students(self):
        emails = frappe.get_all("LMS Batch Membership", filters={"subgroup": self.name}, fields=["member"], pluck='member')
        return [frappe.get_doc("User", email) for email in emails]

    def is_mentor(self, email):
        q = {
            "doctype": "Cohort Mentor",
            "subgroup": self.name,
            "email": email
        }
        return frappe.db.exists(q)

#def after_doctype_insert():
#    frappe.db.add_unique("Cohort Subgroup", ("cohort", "slug"))
