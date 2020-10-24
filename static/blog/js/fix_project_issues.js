$(function () {
  $(document).on("submit", ".add_fix_form", function (event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: $(this).serialize(),
      dataType: "json",
      success: function (response) {
        $("#show_add_fix_section").html(response["issue"]);
        $("textarea").val("");
      },
      error: function (rs, e) {
        console.log(rs.responseText);
      },
    });
  });
});
