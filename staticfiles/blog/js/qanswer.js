$(function(){

  $(".reply-butt").on('click',function(event){
    $(this).parent().next('.replied-answers').fadeToggle();
    });

    // answers ajax
  $(document).on("submit",".answer-form",function(event){
    // event.preventDefault()
      $('textarea').val('')
  })

  // reply form
  $(document).on("submit", ".reply-form", function (event) {
    $("textarea").val("");
    $(".reply-butt").on("click", function (event) {
      $(this).parent().next(".replied-answers").fadeToggle();
    });
  });

  // group comment form
  $(document).on("submit", "#group_post_comments", function (event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: $(this).serialize(),
      dataType: "json",
      success: function (response) {
        $("#group_comments_section").html(response["form"]);
        $("textarea").val("");
      },
      error: function (rs, e) {
        console.log(rs.responseText);
      },
    });
  });

  // group post like
  $(document).on("click","#post_like",(event)=> {
    event.preventDefault()
    formData = $("#group_post_form").serialize()
    id = $("#post_like").attr('value')
    console.log(id)

    $.ajax({
      type: "POST",
      url: "/like_gpost/" +id+"/",
      data: formData,
      dataType: "json",
      success: (response) => {
        $("#group_post_like_section").html(response["depost"]);
      },
      error: (rs, e) => {
        console.log(rs.responseText);
      },
    })
  })

})
