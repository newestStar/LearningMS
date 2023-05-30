import frappe
from frappe.utils import cstr
from frappe import _
from lms.lms.utils import can_create_courses


def get_context(context):
	context.no_cache = 1

	if not can_create_courses():
		message = "You do not have permission to access this page."
		if frappe.session.user == "Guest":
			message = "Please login to access this page."

		raise frappe.PermissionError(_(message))

	quizname = frappe.form_dict["quizname"]
	if quizname == "new-quiz":
		context.quiz = frappe._dict()
	else:
		fields_arr = ["name", "question", "type"]
		for num in range(1, 5):
			fields_arr.append("option_" + cstr(num))
			fields_arr.append("is_correct_" + cstr(num))
			fields_arr.append("explanation_" + cstr(num))
			fields_arr.append("possibility_" + cstr(num))

		context.quiz = frappe.db.get_value("LMS Quiz", quizname, ["title", "name"], as_dict=1)
		context.quiz.questions = frappe.get_all(
			"LMS Quiz Question", {"parent": quizname}, fields_arr, order_by="idx"
		)
