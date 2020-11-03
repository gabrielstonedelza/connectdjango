$(function () {
  setTimeout(function () {
    $(".alert").slideUp(3000);
  }, 5000);

  // like section for tutorial
  $(document).on("click", "#like", function (event) {
    event.preventDefault();
    var id = $("#like").attr("value");
    var myformData = $("#theForm").serialize();
    $.ajax({
      type: "POST",
      url: "/like_tutorial/" + id + "/",
      data: myformData,
      dataType: "json",
      success: function (response) {
        $("#like-section").html(response["form"]);
        console.log($("#like-section").html(response["form"]));
      },
      error: function (rs, e) {
        console.log(rs.responseText);
      },
    });
  });

  // homepage cycle
  $(".cycle-slideshow").cycle({
    speed: 600,
    manualSpeed: 100,
  });
});
