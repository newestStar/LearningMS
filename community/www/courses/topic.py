import frappe

def get_context(context):
    context.no_cache = 1

    try:
        course_name = get_queryparam("course", '/courses')
        context.course = get_course(course_name)

        topic_name = get_queryparam("topic", '/courses/' + course_name)
        context.topic = get_topic(course_name, topic_name)
        context.livecode_url = get_livecode_url()
    except frappe.DoesNotExistError:
        context.template = 'www/404.html'

def get_livecode_url():
    doc = frappe.get_doc("LMS Settings")
    return doc.livecode_url

def get_queryparam(name, redirect_when_not_found):
    try:
        return frappe.form_dict[name]
    except KeyError:
        frappe.local.flags.redirect_location = redirect_when_not_found
        raise frappe.Redirect

def get_course(name):
    try:
        course = frappe.get_doc('LMS Course', name)
    except frappe.DoesNotExistError:
        raise
    return course

def get_topic(course_name, topic_name):
    try:
        topic = frappe.get_doc('LMS Topic', topic_name)
    except frappe.DoesNotExistError:
        raise
    if topic.course != course_name:
        raise frappe.DoesNotExistError()
    return topic
