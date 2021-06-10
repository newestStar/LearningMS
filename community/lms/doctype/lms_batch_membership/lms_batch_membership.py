# -*- coding: utf-8 -*-
# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class LMSBatchMembership(Document):

    def validate(self):
        self.validate_membership_in_same_batch()
        self.validate_membership_in_different_batch_same_course()

    def validate_membership_in_same_batch(self):
        previous_membership = frappe.db.get_value("LMS Batch Membership",
            filters={
                "member": self.member,
                "batch": self.batch,
                "name": ["!=", self.name]
            },
            fieldname=["member_type","member"],
            as_dict=1)

        if previous_membership:
            member_name = frappe.db.get_value("User", self.member, "full_name")
            frappe.throw(_("{0} is already a {1} of {2}").format(member_name, previous_membership.member_type, self.batch))

    def validate_membership_in_different_batch_same_course(self):
        course = frappe.db.get_value("LMS Batch", self.batch, "course")
        previous_membership = frappe.get_all("LMS Batch Membership",
                                    filters={
                                        "member": self.member,
                                        "name": ["!=", self.name]
                                    },
                                    fields=["batch", "member_type", "name"]
                                )

        for membership in previous_membership:
            batch_course = frappe.db.get_value("LMS Batch", membership.batch, "course")
            if batch_course == course and (membership.member_type == "Student" or self.member_type == "Student"):
                member_name = frappe.db.get_value("User", self.member, "full_name")
                frappe.throw(_("{0} is already a {1} of {2} course through {3} batch").format(member_name, membership.member_type, course, membership.batch))

    def get_user_batch(course, user=frappe.session.user):
        return frappe.db.get_value("LMS Batch Membership", {"member": user, "course": course}, "batch")

@frappe.whitelist()
def create_membership(batch, member=None, member_type="Student", role="Member"):
    frappe.get_doc({
        "doctype": "LMS Batch Membership",
        "batch": batch,
        "role": role,
        "member_type": member_type,
        "member": member or frappe.session.user
    }).save(ignore_permissions=True)
    return "OK"
