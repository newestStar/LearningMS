(() => {
  // ../community/community/public/js/profile.js
  frappe.ready(() => {
    if (frappe.session.user == "Guest") {
      var link_array = $(".nav-link").filter((i, elem) => $(elem).text().trim() === "My Profile");
      link_array.length && $(link_array[0]).addClass("hide");
    }
  });
})();
//# sourceMappingURL=website.bundle.HL5DXFIV.js.map
