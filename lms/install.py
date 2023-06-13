import frappe
from frappe.desk.page.setup_wizard.setup_wizard import add_all_roles_to


def after_install():
	add_pages_to_nav()


def after_sync():
	create_lms_roles()
	set_default_home()
	add_all_roles_to("Administrator")


def add_pages_to_nav():
	pages = [
		{"label": "Explore", "idx": 1},
		{"label": "Courses", "url": "/courses", "parent": "Explore", "idx": 2},
		{"label": "Classes", "url": "/classes", "parent": "Explore", "idx": 3},
		{"label": "Statistics", "url": "/statistics", "parent": "Explore", "idx": 4},
		{"label": "Jobs", "url": "/jobs", "parent": "Explore", "idx": 5},
		{"label": "People", "url": "/community", "parent": "Explore", "idx": 6},
	]

	for page in pages:
		filters = frappe._dict()
		if page.get("url"):
			filters["url"] = ["like", "%" + page.get("url") + "%"]
		else:
			filters["label"] = page.get("label")

		if not frappe.db.exists("Top Bar Item", filters):
			frappe.get_doc(
				{
					"doctype": "Top Bar Item",
					"label": page.get("label"),
					"url": page.get("url"),
					"parent_label": page.get("parent"),
					"idx": page.get("idx"),
					"parent": "Website Settings",
					"parenttype": "Website Settings",
					"parentfield": "top_bar_items",
				}
			).save()


def before_uninstall():
	delete_custom_fields()
	delete_lms_roles()


def create_lms_roles():
	create_course_creator_role()
	create_moderator_role()


def delete_lms_roles():
	roles = ["Course Creator", "Moderator"]
	for role in roles:
		if frappe.db.exists("Role", role):
			frappe.db.delete("Role", role)


def set_default_home():
	frappe.db.set_single_value("Portal Settings", None, "default_portal_home", "/courses")


def create_course_creator_role():
	if not frappe.db.exists("Role", "Course Creator"):
		role = frappe.get_doc(
			{
				"doctype": "Role",
				"role_name": "Course Creator",
				"home_page": "",
				"desk_access": 0,
			}
		)
		role.save(ignore_permissions=True)


def create_moderator_role():
	if not frappe.db.exists("Role", "Moderator"):
		role = frappe.get_doc(
			{
				"doctype": "Role",
				"role_name": "Moderator",
				"home_page": "",
				"desk_access": 0,
			}
		)
		role.save(ignore_permissions=True)


def delete_custom_fields():
	fields = [
		"user_category",
		"headline",
		"college",
		"city",
		"verify_terms",
		"country",
		"preferred_location",
		"preferred_functions",
		"preferred_industries",
		"work_environment_column",
		"time",
		"role",
		"carrer_preference_details",
		"skill",
		"certification_details",
		"internship",
		"branch",
		"github",
		"medium",
		"linkedin",
		"profession",
		"looking_for_job",
		"cover_image" "work_environment",
		"dream_companies",
		"career_preference_column",
		"attire",
		"collaboration",
		"location_preference",
		"company_type",
		"skill_details",
		"certification",
		"education",
		"work_experience",
		"education_details",
		"hide_private",
		"work_experience_details",
		"profile_complete",
	]

	for field in fields:
		frappe.db.delete("Custom Field", {"fieldname": field})
