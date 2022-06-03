{% set title = frappe.db.get_value("LMS Course", doc.course, "title") %}
<p> {{ _('Your evaluation for the course ${0} has been scheduled on ${1} at ${2}.').format(title, frappe.utils.format_date(doc.date, "medium"), frappe.utils.format_time(doc.start_time, "short")) }}</p>
<p> {{ _("Please prepare well and be on time for the evaluations.") }} </p>
