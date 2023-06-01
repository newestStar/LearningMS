import frappe
from frappe import _
from lms.lms.utils import has_course_moderator_role


def get_context(context):
	context.no_cache = 1
	context.is_moderator = has_course_moderator_role()
	submission = frappe.form_dict["submission"]
	assignment = frappe.form_dict["assignment"]

	context.assignment = frappe.db.get_value(
		"LMS Assignment", assignment, ["title", "name", "type", "question"], as_dict=1
	)

	if submission == "new-submission":
		context.submission = frappe._dict()
	else:
		context.submission = frappe.db.get_value(
			"LMS Assignment Submission",
			submission,
			["name", "assignment_attachment", "comments", "status", "member", "member_name"],
			as_dict=True,
		)
		if not context.is_moderator and frappe.session.user != context.submission.member:
			raise frappe.PermissionError(_("You don't have permission to access this page."))

	if not context.assignment or not context.submission:
		raise frappe.PermissionError(_("Invalid Submission URL"))
