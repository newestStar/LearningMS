# -*- coding: utf-8 -*-
# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from community.www.courses.utils import get_member_with_email
from frappe import _
from community.lms.doctype.lms_batch_membership.lms_batch_membership import create_membership
from community.query import find, find_all

class LMSBatch(Document):
    def validate(self):
        self.validate_if_mentor()
        if not self.code:
            self.generate_code()

    def validate_if_mentor(self):
        course = frappe.get_doc("LMS Course", self.course)
        if not course.is_mentor(frappe.session.user):
           frappe.throw(_("You are not a mentor of the course {0}").format(course.title))

    def after_insert(self):
        create_membership(batch=self.name, member_type="Mentor")

    def generate_code(self):
        short_code = frappe.db.get_value("LMS Course", self.course, "short_code")
        course_batches = frappe.get_all("LMS Batch",{"course":self.course})
        self.code = short_code + str(len(course_batches) + 1)

    def get_mentors(self):
        memberships = frappe.get_all(
                    "LMS Batch Membership",
                    {"batch": self.name, "member_type": "Mentor"},
                    ["member"])
        member_names = [m['member'] for m in memberships]
        return find_all("Community Member", name=["IN", member_names])

    def is_member(self, email, member_type=None):
        """Checks if a person is part of a batch.

        If member_type is specified, checks if the person is a Student/Mentor.
        """
        member = find("Community Member", email=email)
        if not member:
            return

        filters = {
            "batch": self.name,
            "member": member.name
        }
        if member_type:
            filters['member_type'] = member_type
        return frappe.db.exists("LMS Batch Membership", filters)

    def get_students(self):
        """Returns (email, full_name, username) of all the students of this batch as a list of dict.
        """
        memberships = frappe.get_all(
                    "LMS Batch Membership",
                    {"batch": self.name, "member_type": "Student"},
                    ["member"])
        member_names = [m['member'] for m in memberships]
        members = frappe.get_all(
                    "Community Member",
                    {"name": ["IN", member_names]},
                    ["email", "full_name", "username"])
        return members


@frappe.whitelist()
def get_messages(batch):
    messages =  frappe.get_all("LMS Message", {"batch": batch}, ["*"], order_by="creation")
    for message in messages:
        message.message = frappe.utils.md_to_html(message.message)
        member_email = frappe.db.get_value("Community Member", message.author, ["email"])
        if member_email == frappe.session.user:
            message.author_name = "You"
            message.is_author = True
    return messages

@frappe.whitelist()
def save_message(message, batch):
    doc = frappe.get_doc({
        "doctype": "LMS Message",
        "batch": batch,
        "author": get_member_with_email(),
        "message": message
    })
    doc.save(ignore_permissions=True)
