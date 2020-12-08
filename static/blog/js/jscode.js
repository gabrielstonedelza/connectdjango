$(function () {
  setTimeout(function () {
    $(".alert").slideUp(3000);
  }, 5000);
  
  $("#show-my-messages").animate({ scrollTop: $('#show-my-messages').prop("scrollHeight")}, 1000);
  $("#chat-message-input").keyup(function(e){
    if (e.keyCode === 13) {  // enter, return
      $("#show-my-messages").animate({ scrollTop: $('#show-my-messages').prop("scrollHeight")}, 1000);
  }
  })
  
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
});
