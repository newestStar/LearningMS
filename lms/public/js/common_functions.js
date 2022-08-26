frappe.ready(() => {

    setup_vue_and_file_size();

    $(".join-batch").click((e) => {
        join_course(e);
    });

    $(".notify-me").click((e) => {
        notify_user(e);
    });

    $(".btn-chapter").click((e) => {
        add_chapter(e);
    });

    $(document).on("click", ".btn-save-chapter", (e) => {
        save_chapter(e);
    });

});


const setup_vue_and_file_size = () => {
    frappe.require("/assets/frappe/node_modules/vue/dist/vue.js", () => {
        Vue.prototype.__ = window.__;
        Vue.prototype.frappe = window.frappe;
    });

    frappe.provide("frappe.form.formatters");
    frappe.form.formatters.FileSize = file_size;
};


const file_size = (value) => {
    if(value > 1048576) {
        value = flt(flt(value) / 1048576, 1) + "M";
    } else if (value > 1024) {
        value = flt(flt(value) / 1024, 1) + "K";
    }
    return value;
};


const join_course = (e) => {
    e.preventDefault();
    let course = $(e.currentTarget).attr("data-course");
    if (frappe.session.user == "Guest") {
        window.location.href = `/login?redirect-to=/courses/${course}`;
        return;
    }

    let batch = $(e.currentTarget).attr("data-batch");
    batch = batch ? decodeURIComponent(batch) : "";
    frappe.call({
        "method": "lms.lms.doctype.lms_batch_membership.lms_batch_membership.create_membership",
        "args": {
            "batch": batch ? batch : "",
            "course": course
        },
        "callback": (data) => {
            if (data.message == "OK") {
                $(".no-preview-modal").modal("hide");
                frappe.show_alert({
                    message: __("You are now a student of this course."),
                    indicator:'green'
                }, 3);
                setTimeout(function () {
                    window.location.href = `/courses/${course}/learn/1.1`;
                }, 3000);
            }
        }
    })
};


const notify_user = (e) => {
    e.preventDefault();
    var course = decodeURIComponent($(e.currentTarget).attr("data-course"));
    if (frappe.session.user == "Guest") {
        window.location.href = `/login?redirect-to=/courses/${course}`;
        return;
    }

    frappe.call({
        method: "lms.lms.doctype.lms_course_interest.lms_course_interest.capture_interest",
        args: {
            "course": course
        },
        callback: (data) => {
            $(".no-preview-modal").modal("hide");
            frappe.show_alert({
                message: __("You have opted to be notified for this course. You will receive an email when the course becomes available."),
                indicator:'green'
            }, 3);
            setTimeout(() => {
                window.location.reload();
            }, 3000);
        }
    })
};


const add_chapter = (e) => {
    if ($(".new-chapter").length) {
        scroll_to_chapter_container();
        return;
    }

    let next_index = $("[data-index]").last().data("index") + 1 || 1;
    let add_after = $(`.chapter-parent:last`).length ? $(`.chapter-parent:last`) : $("#outline-heading");

    $(`<div class="chapter-parent chapter-edit new-chapter">
        <div contenteditable="true" data-placeholder="${__('Chapter Name')}" class="chapter-title-main"></div>
        <div class="chapter-description small my-2" contenteditable="true"
            data-placeholder="${__('Short Description')}"></div>
        <button class="btn btn-sm btn-secondary d-block btn-save-chapter"
        data-index="${next_index}"> ${__('Save')} </button>
        </div>`).insertAfter(add_after);

    scroll_to_chapter_container();
};


const scroll_to_chapter_container = () => {
    $([document.documentElement, document.body]).animate({
        scrollTop: $(".new-chapter").offset().top
    }, 1000);
    $(".new-chapter").find(".chapter-title-main").focus();
}


const save_chapter = (e) => {
    let target = $(e.currentTarget);
    let parent = target.closest(".chapter-parent");

    frappe.call({
        method: "lms.lms.doctype.lms_course.lms_course.save_chapter",
        args: {
            "course": $("#title").data("course"),
            "title": parent.find(".chapter-title-main").text(),
            "chapter_description": parent.find(".chapter-description").text(),
            "idx": target.data("index"),
            "chapter": target.data("chapter") ? target.data("chapter") : ""
        },
        callback: (data) => {
            frappe.show_alert({
                message: __("Saved"),
                indicator: "green",
            });
            setTimeout(() => {
                window.location.reload();
            }, 1000)
        }
    });
};

