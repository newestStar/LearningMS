// Copyright (c) 2021, FOSS United and contributors
// For license information, please see license.txt

frappe.ui.form.on("LMS Certificate", {
	onload: (frm) => {
		frm.set_query("member", function (doc) {
			return {
				filters: {
					ignore_user_type: 1,
				},
			};
		});
	},
	refresh: (frm) => {
		if (frm.doc.name)
			frm.add_web_link(
				`/courses/${frm.doc.course}/${frm.doc.name}`,
				"See on Website"
			);
	},
});
