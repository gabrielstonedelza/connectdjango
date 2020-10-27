$(function () {

  $(document).on("submit", "#feedback_form", function (event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: $(this).serialize(),
      dataType: "json",
      success: function (response) {
        $("#feedback_section").html(response["form"]);
        $("input").val("");
      },
      error: function (rs, e) {
        console.log(rs.responseText);
      },
    });
  });

  setTimeout(function () {
    $(".alert").slideUp(3000);
  }, 5000);

//   for contact form
$(document).on("submit", "#contac_form", function (event) {
    event.preventDefault();
    message = "Thank you for contacting us we will get back to you soon"
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: $(this).serialize(),
      dataType: "json",
      success: function (response) {
        $("#contact_form_section").html(response["form"]);
        $("textarea").val("");
        $("input").val("");
        $("#showmessage_success").html(message)
        setTimeout(function () {
            $("#showmessage_success").slideUp(3000);
          }, 5000);
      },
      error: function (rs, e) {
        console.log(rs.responseText);
      },
    });
  });

});
