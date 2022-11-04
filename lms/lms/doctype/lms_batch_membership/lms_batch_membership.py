# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class LMSBatchMembership(Document):
	def validate(self):
		self.validate_membership_in_same_batch()
		self.validate_membership_in_different_batch_same_course()

	def validate_membership_in_same_batch(self):
		filters = {"member": self.member, "course": self.course, "name": ["!=", self.name]}
		if self.batch:
			filters["batch"] = self.batch
		previous_membership = frappe.db.get_value(
			"LMS Batch Membership", filters, fieldname=["member_type", "member"], as_dict=1
		)

		if previous_membership:
			member_name = frappe.db.get_value("User", self.member, "full_name")
			course_title = frappe.db.get_value("LMS Course", self.course, "title")
			frappe.throw(
				_("{0} is already a {1} of the course {2}").format(
					member_name, previous_membership.member_type, course_title
				)
			)

	def validate_membership_in_different_batch_same_course(self):
		"""Ensures that a studnet is only part of one batch."""
		# nothing to worry if the member is not a student
		if self.member_type != "Student":
			return

		course = frappe.db.get_value("LMS Batch", self.batch, "course")
		memberships = frappe.get_all(
			"LMS Batch Membership",
			filters={
				"member": self.member,
				"name": ["!=", self.name],
				"member_type": "Student",
				"course": self.course,
			},
			fields=["batch", "member_type", "name"],
		)

		if memberships:
			membership = memberships[0]
			member_name = frappe.db.get_value("User", self.member, "full_name")
			frappe.throw(
				_("{0} is already a Student of {1} course through {2} batch").format(
					member_name, course, membership.batch
				)
			)


@frappe.whitelist()
def create_membership(
	course, batch=None, member=None, member_type="Student", role="Member"
):
	frappe.get_doc(
		{
			"doctype": "LMS Batch Membership",
			"batch": batch,
			"course": course,
			"role": role,
			"member_type": member_type,
			"member": member or frappe.session.user,
		}
	).save(ignore_permissions=True)
	return "OK"


@frappe.whitelist()
def update_current_membership(batch, course, member):
	all_memberships = frappe.get_all(
		"LMS Batch Membership", {"member": member, "course": course}
	)
	for membership in all_memberships:
		frappe.db.set_value("LMS Batch Membership", membership.name, "is_current", 0)

	current_membership = frappe.get_all(
		"LMS Batch Membership", {"batch": batch, "member": member}
	)
	if len(current_membership):
		frappe.db.set_value(
			"LMS Batch Membership", current_membership[0].name, "is_current", 1
		)
