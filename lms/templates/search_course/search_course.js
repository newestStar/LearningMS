frappe.ready(() => {
	$("#search-course").keyup((e) => {
		search_course(e);
	});

	$(".close-search-empty-state").click((e) => {
		close_search_empty_state(e);
	});

	$("#open-search").click((e) => {
		show_search_bar(e);
	});

	$('#search-modal').on('hidden.bs.modal', () => {
		hide_search_bar();
	});

});

const search_course = (e) => {
	let input = $(e.currentTarget).val();
	if (input == window.input) return;
	window.input = input;

	if (input.length < 3 || input.trim() == "") {
		$(".result-row").remove();
		return;
	}

	frappe.call({
		method: "lms.lms.doctype.lms_course.lms_course.search_course",
		args: {
			text: input,
		},
		callback: (data) => {
			render_course_list(data);
		},
	});
};

const render_course_list = (data) => {
	let courses = data.message;
	$(".result-row").remove();

	if (! courses.length) {
		let element = `<a class="result-row">
			${__("No result found")}
		</a>`;
		$(element).insertAfter("#search-course");
		return;
	}


	for (let i in courses) {
		let element = `<a class="result-row" href="/courses/${courses[i].name}">
			${courses[i].title}
		</a>`;
		$(element).insertAfter("#search-course");
	}
};

const close_search_empty_state = (e) => {
	$(".search-empty-state").addClass("hide");
	$("#search-course").val("");
};

const show_search_bar = (e) => {
	$("#search-modal").modal("show");
	setTimeout(() => {
		$("#search-course").focus();
	}, 1000)
}

const hide_search_bar = (e) => {
	$("#search-course").val("");
	$(".result-row").remove();
}
