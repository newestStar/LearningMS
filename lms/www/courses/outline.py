import frappe
from lms.lms.utils import get_chapters


def get_context(context):
	context.no_cache = 1
	context.course = frappe.db.get_value(
		"LMS Course", frappe.form_dict["course"], ["name", "title"], as_dict=True
	)
	context.chapters = get_chapters(context.course.name)
