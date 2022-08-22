import frappe

def execute():
    if not frappe.db.exists("Role", "Course Instructor"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Course Instructor",
            "home_page": "/dashboard",
        })
        role.save(ignore_permissions=True)
