$(function () {
  $(document).on("click", "#like_button", (event) => {
    event.preventDefault();
    var formData = $("#like_tutorial_form").serialize();
    var pk = $("#like_button").attr("value");

    $.ajax({
      type: "POST",
      url: `/like-tutorial/${pk}/`,
      data: formData,
      dataType: "json",
      success: (response) => {
        $("#likes_section").html(response["likes"]);
      },
      error: (rs, e) => {
        console.log(rs.responseText);
      },
    });
  });
});
