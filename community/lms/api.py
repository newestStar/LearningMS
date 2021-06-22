"""API methods for the LMS.
"""

import frappe

@frappe.whitelist()
def autosave_section(section, code):
    """Saves the code edited in one of the sections.
    """
    doc = frappe.get_doc(
        doctype="Code Revision",
        section=section,
        code=code,
        author=frappe.session.user)
    doc.insert()
    return {"name": doc.name}

@frappe.whitelist()
def submit_solution(exercise, code):
    """Submits a solution.

    @exerecise: name of the exercise to submit
    @code: solution to the exercise
    """
    ex = frappe.get_doc("Exercise", exercise)
    if not ex:
        return
    doc = ex.submit(code)
    return {"name": doc.name, "creation": doc.creation}

@frappe.whitelist()
def save_current_lesson(course_name, lesson_name):
    """Saves the current lesson for a student/mentor.
    """
    name = frappe.get_value(
        doctype="LMS Batch Membership",
        filters={
            "course": course_name,
            "member": frappe.session.user
        },
        fieldname="name")
    if not name:
        return
    doc = frappe.get_doc("LMS Batch Membership", name)
    doc.current_lesson = lesson_name
    doc.save(ignore_permissions=True)
    return {"current_lesson": doc.current_lesson}
