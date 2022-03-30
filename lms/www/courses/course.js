frappe.ready(() => {

  hide_wrapped_mentor_cards();

  $("#cancel-request").click((e) => {
    cancel_mentor_request(e);
  });

  $(".join-batch").click((e) => {
    join_course(e)
  });

  $(".view-all-mentors").click((e) => {
    view_all_mentors(e);
  });

  $(".review-link").click((e) => {
    show_review_dialog(e);
  });

  $(".icon-rating").click((e) => {
    highlight_rating(e);
  });

  $("#submit-review").click((e) => {
    submit_review(e);
  })

  $("#notify-me").click((e) => {
    notify_user(e);
  })

  $("#certification").click((e) => {
    create_certificate(e);
  });

  $("#submit-for-review").click((e) => {
    submit_for_review(e);
  });

  $("#apply-certificate").click((e) => {
      apply_cetificate(e);
  });

  $(".slot").click((e) => {
      submit_slot(e);
  });

  $(document).scroll(function() {
    let timer;
    clearTimeout(timer);
    timer = setTimeout(() => { handle_overlay_display.apply(this, arguments); }, 500);
  });

})

var hide_wrapped_mentor_cards = () => {
  var offset_top_prev;

  $(".member-parent .member-card").each(function () {
    var offset_top = $(this).offset().top;
    if (offset_top > offset_top_prev) {
      $(this).addClass('wrapped').slideUp("fast");
    }
    if (!offset_top_prev) {
      offset_top_prev = offset_top;
    }

  });

  if ($(".wrapped").length < 1) {
    $(".view-all-mentors").hide();
  }
}

var cancel_mentor_request = (e) => {
  e.preventDefault()
  frappe.call({
    "method": "lms.lms.doctype.lms_mentor_request.lms_mentor_request.cancel_request",
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
}

var join_course = (e) => {
  e.preventDefault();
  var course = $(e.currentTarget).attr("data-course")
  if (frappe.session.user == "Guest") {
    window.location.href = `/login?redirect-to=/courses/${course}`;
    return;
  }
  var batch = $(e.currentTarget).attr("data-batch");
  batch = batch ? decodeURIComponent(batch) : "";
  frappe.call({
    "method": "lms.lms.doctype.lms_batch_membership.lms_batch_membership.create_membership",
    "args": {
      "batch": batch ? batch : "",
      "course": course
    },
    "callback": (data) => {
      if (data.message == "OK") {
        frappe.msgprint(__("You are now a student of this course."));
        setTimeout(function () {
          window.location.href = `/courses/${course}/learn/1.1`;
        }, 2000);
      }
    }
  })
}

var view_all_mentors = (e) => {
  $(".wrapped").each((i, element) => {
    $(element).slideToggle("slow");
  })
  var text_element = $(".view-all-mentors .course-instructor .all-mentors-text");
  var text = text_element.text() == "View all mentors" ? "View less" : "View all mentors";
  text_element.text(text);

  if ($(".mentor-icon").css("transform") == "none") {
    $(".mentor-icon").css("transform", "rotate(180deg)");
  } else {
    $(".mentor-icon").css("transform", "");
  }
}

var show_review_dialog = (e) => {
  e.preventDefault();
  $("#review-modal").modal("show");
}

var highlight_rating = (e) => {
  var rating = $(e.currentTarget).attr("data-rating");
  $(".icon-rating").removeClass("star-click");
  $(".icon-rating").each((i, elem) => {
    if (i <= rating-1) {
      $(elem).addClass("star-click");
    }
  })
}

var submit_review = (e) => {
  e.preventDefault();
  var rating = $(".rating-field").children(".star-click").length;
  var review = $(".review-field").val();
  if (!review || !rating) {
    $(".error-field").text("Both Rating and Review are required.");
    return;
  }
  frappe.call({
    method: "lms.lms.doctype.lms_course_review.lms_course_review.submit_review",
    args: {
      "rating": rating,
      "review": review,
      "course": decodeURIComponent($(e.currentTarget).attr("data-course"))
    },
    callback: (data) => {
      if (data.message == "OK") {
        $(".review-modal").modal("hide");
        window.location.reload();
      }
    }
  })
};

var notify_user = (e) => {
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
      $("#interest-alert").removeClass("hide");
      $("#notify-me").addClass("hide");
    }
  })
};

const create_certificate = (e) => {
  e.preventDefault();
  course = $(e.currentTarget).attr("data-course");
  frappe.call({
    method: "lms.lms.doctype.lms_certification.lms_certification.create_certificate",
    args: {
      "course": course
    },
    callback: (data) => {
      window.location.href = `/courses/${course}/${data.message.name}`;
    }
  })
};


const element_not_in_viewport = (el) => {
  const rect = el.getBoundingClientRect();
  return rect.bottom < 0 || rect.right < 0 || rect.left > window.innerWidth || rect.top > window.innerHeight;
};

const handle_overlay_display = () => {
  const element = $(".related-courses").length && $(".related-courses")[0];
  if (element && element_not_in_viewport(element)) {
    $(".course-overlay-card").css({
      "position": "fixed",
      "top": "30%",
      "bottom": "inherit"
    });
  }
  else if (element && !element_not_in_viewport(element)) {
    $(".course-overlay-card").css({
        "position": "absolute",
        "top": "inherit",
        "bottom": "5%"
      });
  }
};

const submit_for_review = (e) => {
  let course = $(e.currentTarget).data("course");
  frappe.call({
    method: "lms.lms.doctype.lms_course.lms_course.submit_for_review",
    args: {
      "course": course
    },
    callback: (data) => {
      if (data.message == "No Chp") {
        frappe.msgprint(__(`There are no chapters in this course.
          Please add chapters and lessons to your course before you submit it for review.`));
      } else if (data.message == "OK") {
        frappe.msgprint(__("Your course has been submitted for review."))
        window.location.reload();
      }
    }
  })
};

const apply_cetificate = (e) => {
    frappe.call({
        method: "lms.lms.doctype.course_evaluator.course_evaluator.get_schedule",
        args: {
            "course": $(e.currentTarget).data("course")
        },
        callback: (data) => {
            let options = "";
            data.message.forEach((obj) => {
                options += `<button class="btn btn-sm btn-secondary mr-3 slot"
                    data-course="${$(e.currentTarget).data("course")}"
                    data-day="${obj.day}" data-start="${obj.start_time}" data-end="${obj.end_time}">
                    ${obj.day} ${obj.start_time} - ${obj.end_time}</button>`;
            });
            e.preventDefault();
            $("#slot-modal .slots").html(options);
            $("#slot-modal").modal("show");
        }
    })
};

const submit_slot = (e) => {
    const target = $(e.currentTarget);
    frappe.call({
        method: "lms.lms.doctype.lms_certificate_request.lms_certificate_request.create_certificate_request",
        args: {
            "course": target.data("course"),
            "day": target.data("day"),
            "start_time": target.data("start"),
            "end_time": target.data("end")
        },
        callback: (data) => {

        }
    });
};
