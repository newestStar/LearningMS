// Copyright (c) 2022, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("LMS Class", {
	onload: function (frm) {
		frm.set_query("student", "students", function (doc) {
			return {
				filters: {
					ignore_user_type: 1,
				},
			};
		});
	},

	fetch_lessons: (frm) => {
		frm.clear_table("scheduled_flow");
		frappe.call({
			method: "lms.lms.doctype.lms_class.lms_class.fetch_lessons",
			args: {
				courses: frm.doc.courses,
			},
			callback: (r) => {
				if (r.message) {
					console.log(r.message);
					r.message.forEach((lesson) => {
						console.log(typeof lesson);
						let row = frm.add_child("scheduled_flow");
						row.lesson = lesson.name;
					});
					frm.refresh_field("scheduled_flow");
				}
			},
		});
	},
});
