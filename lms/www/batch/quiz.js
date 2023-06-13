frappe.ready(() => {
	$("#quiz-title").focusout((e) => {
		if ($("#quiz-title").val() != $("#quiz-title").data("title")) {
			save_quiz({ quiz_title: $("#quiz-title").val() });
		}
	});

	$(".question-row").click((e) => {
		edit_question(e);
	});

	$(".btn-add-question").click((e) => {
		show_question_modal();
	});
});

const show_quiz_modal = () => {
	let quiz_dialog = new frappe.ui.Dialog({
		title: __("Create Quiz"),
		fields: [
			{
				fieldtype: "Data",
				label: __("Quiz Title"),
				fieldname: "quiz_title",
				reqd: 1,
			},
		],
		primary_action: (values) => {
			quiz_dialog.hide();
			save_quiz(values);
		},
	});

	quiz_dialog.show();
};

const show_question_modal = (values = {}) => {
	let fields = get_question_fields(values);

	this.question_dialog = new frappe.ui.Dialog({
		title: __("Add Question"),
		fields: fields,
		primary_action: (data) => {
			if (values) data.name = values.name;
			save_question(data);
		},
	});

	question_dialog.show();
};

const get_question_fields = (values = {}) => {
	let dialog_fields = [
		{
			fieldtype: "Text Editor",
			fieldname: "question",
			label: __("Question"),
			reqd: 1,
			default: values.question || "",
		},
		{
			fieldtype: "Select",
			fieldname: "type",
			label: __("Type"),
			options: ["Choices", "User Input"],
			default: values.type || "Choices",
		},
	];
	Array.from({ length: 4 }, (x, i) => {
		num = i + 1;

		dialog_fields.push({
			fieldtype: "Section Break",
			fieldname: `section_break_${num}`,
		});

		let option = {
			fieldtype: "Small Text",
			fieldname: `option_${num}`,
			label: __(`Option ${num}`),
			depends_on: "eval:doc.type=='Choices'",
			default: values[`option_${num}`] || "",
		};

		if (num <= 2) option.mandatory_depends_on = "eval:doc.type=='Choices'";

		dialog_fields.push(option);

		dialog_fields.push({
			fieldtype: "Data",
			fieldname: `explanaion_${num}`,
			label: __("Explanation"),
			depends_on: "eval:doc.type=='Choices'",
			default: values[`explanaion_${num}`] || "",
		});

		let is_correct = {
			fieldtype: "Check",
			fieldname: `is_correct_${num}`,
			label: __("Is Correct"),
			depends_on: "eval:doc.type=='Choices'",
			default: values[`is_correct_${num}`] || 0,
		};

		if (num <= 2)
			is_correct.mandatory_depends_on = "eval:doc.type=='Choices'";

		dialog_fields.push(is_correct);

		possibility = {
			fieldtype: "Small Text",
			fieldname: `possibility_${num}`,
			label: __(`Possible Answer ${num}`),
			depends_on: "eval:doc.type=='User Input'",
			default: values[`possibility_${num}`] || "",
		};

		if (num == 1)
			possibility.mandatory_depends_on = "eval:doc.type=='User Input'";

		dialog_fields.push(possibility);
	});

	return dialog_fields;
};

const edit_question = (e) => {
	let question = $(e.currentTarget).data("question");
	frappe.call({
		method: "lms.lms.doctype.lms_quiz.lms_quiz.get_question_details",
		args: {
			question: question,
		},
		callback: (data) => {
			if (data.message) show_question_modal(data.message);
		},
	});
};

const save_quiz = (values) => {
	frappe.call({
		method: "lms.lms.doctype.lms_quiz.lms_quiz.save_quiz",
		args: {
			quiz_title: values.quiz_title,
			quiz: $("#quiz-form").data("name") || "",
		},
		callback: (data) => {
			frappe.show_alert({
				message: __("Saved"),
				indicator: "green",
			});
			setTimeout(() => {
				window.location.href = `/quizzes/${data.message}`;
			}, 2000);
		},
	});
};

const save_question = (values) => {
	frappe.call({
		method: "lms.lms.doctype.lms_quiz.lms_quiz.save_question",
		args: {
			quiz: $("#quiz-form").data("name") || "",
			values: values,
			index: $("#quiz-form").data("index") + 1,
		},
		callback: (data) => {
			if (data.message) this.question_dialog.hide();

			frappe.show_alert({
				message: __("Saved"),
				indicator: "green",
			});
			setTimeout(() => {
				window.location.reload();
			}, 1000);
		},
	});
};
