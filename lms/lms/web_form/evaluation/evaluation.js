frappe.ready(function () {
	frappe.web_form.after_save = () => {
		let data = frappe.web_form.get_values();
		if (data.class) {
			setTimeout(() => {
				window.location.href = `/classes/${data.class}`;
			}, 2000);
		}
	};
});
