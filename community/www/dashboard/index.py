import frappe
from ...lms.doctype.lms_sketch.lms_sketch import get_recent_sketches

def get_context(context):
	context.no_cache = 1
	context.member = frappe.get_all("Community Member", {"email": frappe.session.user}, ["name", "email", "photo", "full_name"])[0]
	context.abbr = "".join([s[0] for s in context.member.full_name.split()])
	context.memberships = get_memberships(context.member.name)
	context.courses = get_courses(context.memberships)
	context.activity = get_activity(context.memberships)
	context.sketches = list(filter(lambda x: x.owner == frappe.session.user, get_recent_sketches()))

def get_memberships(member):
	return frappe.get_all("LMS Batch Membership", {"member": member}, ["batch", "member_type", "creation"])

def get_courses(memberships):
	courses = []
	for membership in memberships:
		course = frappe.db.get_value("LMS Batch", membership.batch, "course")
		course_details = frappe.get_doc("LMS Course", course)
		course_in_list = list(filter(lambda x: x.name == course_details.name, courses))
		if not len(course_in_list):
			course_details.description = course_details.description[0:100] + "..."
			course_details.joining = membership.creation
			if membership.member_type != "Student":
				course_details.member_type = membership.member_type
			courses.append(course_details)
	return courses

def get_activity(memberships):
	messages, courses = [], {}
	batches = [x.batch for x in memberships]
	for batch in batches:
		courses[batch] = frappe.db.get_value("LMS Batch", batch, "course")
	messages = frappe.get_all("LMS Message", {"batch": ["in", ",".join(batches)]}, ["message", "author", "creation", "batch"], order_by='creation desc')
	for message in messages:
		message.course = courses[message.batch]
		message.profile, message.full_name = frappe.db.get_value("Community Member", message.author, ["photo", "full_name"])
		if not message.profile:
			message.abbr = "".join([s[0] for s in message.full_name.split()])
	return messages