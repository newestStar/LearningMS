frappe.ready(() => {
  if (frappe.session.user != "Guest") {
    frappe.call({
      'method': 'community.lms.doctype.lms_mentor_request.lms_mentor_request.has_requested',
      'args': {
        course: decodeURIComponent($("#course-title").attr("data-course")),
      },
      'callback': (data) => {
        if (data.message > 0) {
          $("#mentor-request").addClass("hide");
          $("#already-applied").removeClass("hide")
        }
      }
    })
  }

  $("#apply-now").click((e) => {
    e.preventDefault();
    if (frappe.session.user == "Guest") {
      window.location.href = `/login?redirect-to=/courses/${$(e.currentTarget).attr("data-course")}`;
      return;
    }
    frappe.call({
      "method": "community.lms.doctype.lms_mentor_request.lms_mentor_request.create_request",
      "args": {
        "course": decodeURIComponent($(e.currentTarget).attr("data-course"))
      },
      "callback": (data) => {
        if (data.message == "OK") {
          $("#mentor-request").addClass("hide");
          $("#already-applied").removeClass("hide")
        }
      }
    })
  })

  $("#cancel-request").click((e) => {
    e.preventDefault()
    frappe.call({
      "method": "community.lms.doctype.lms_mentor_request.lms_mentor_request.cancel_request",
      "args": {
        "course": decodeURIComponent($(e.currentTarget).attr("data-course"))
      },
      "callback": (data) => {
        if (data.message == "OK") {
          $("#mentor-request").removeClass("hide");
          $("#already-applied").addClass("hide")
        }
      }
    })
  })

  $(".join-batch").click((e) => {
    e.preventDefault();
    var course = $(e.currentTarget).attr("data-course")
    if (frappe.session.user == "Guest") {
      window.location.href = `/login?redirect-to=/courses/${course}`;
      return;
    }
    batch = decodeURIComponent($(e.currentTarget).attr("data-batch"))
    frappe.call({
      "method": "community.lms.doctype.lms_batch_membership.lms_batch_membership.create_membership",
      "args": {
        "batch": batch
      },
      "callback": (data) => {
        if (data.message == "OK") {
          frappe.msgprint(__("You are now a student of this course."));
          setTimeout(function () {
            window.location.href = `/courses/${course}/home`;
          }, 2000);
        }
      }
    })
  })

  $(".manage-batch").click((e) => {
    e.preventDefault();
    var batch = decodeURIComponent($(e.currentTarget).attr("data-batch"));
    var course = decodeURIComponent($(e.currentTarget).attr("data-course"));
    frappe.call({
      method: "community.lms.doctype.lms_batch_membership.lms_batch_membership.update_current_membership",
      args: {
        batch: batch,
        course: course,
        member: frappe.session.user
      },
      callback: (data) => {
        window.location.href = `/courses/${course}/home`;
      }
    })
  })
})
