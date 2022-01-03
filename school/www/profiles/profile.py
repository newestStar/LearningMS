import frappe
from school.page_renderers import get_profile_url_prefix
from urllib.parse import urlencode

def get_context(context):
    context.no_cache = 1

    try:
        username = frappe.form_dict["username"]
    except KeyError:
        username = frappe.db.get_value("User", frappe.session.user, ["username"])
        if username:
            frappe.local.flags.redirect_location = get_profile_url_prefix() + username
            raise frappe.Redirect
    try:
        context.member = frappe.get_doc("User", {"username": username})
    except:
        context.template = "www/404.html"
        return
    context.hide_primary_contact = frappe.db.get_single_value("LMS Settings", "hide_primary_contact")
    context.show_contacts_section = show_contacts_section(context.member, context.hide_primary_contact)
    context.profile_tabs = get_profile_tabs(context.member)

def show_contacts_section(member, hide_primary_contact):
    if member.github or member.linkedin or member.medium:
        return True
    if hide_primary_contact or member.hide_private:
        return False
    return True

def get_profile_tabs(user):
    """Returns the enabled ProfileTab objects.

    Each ProfileTab is rendered as a tab on the profile page and the
    they are specified as profile_tabs hook.
    """
    tabs = frappe.get_hooks("profile_tabs") or []
    return [frappe.get_attr(tab)(user) for tab in tabs]
