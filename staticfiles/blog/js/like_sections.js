$(function () {
  // tutorial like button
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

  // blog like button
  $(document).on("click", "#like_blog_button", (event) => {
    event.preventDefault();
    var formData = $("#like_blog_form").serialize();
    var pk = $("#like_blog_button").attr("value");

    $.ajax({
      type: "POST",
      url: `/like-blog/${pk}/`,
      data: formData,
      dataType: "json",
      success: (response) => {
        $("#like_blog_section").html(response["likes"]);
      },
      error: (rs, e) => {
        console.log(rs.responseText);
      },
    });
  });

  // hide and show like and comment box
  var lastScrollTop = 0;

$(window).scroll(function() {

    var scrollTop = $(this).scrollTop();
    
    if (scrollTop < lastScrollTop) {
        
        $('#like-helpful-section').hide();
    } else {
     
        $('#like-helpful-section').show();
    }
    
    lastScrollTop = scrollTop;
});
});
