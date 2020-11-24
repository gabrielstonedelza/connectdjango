$(function () {
  
  // blog like button
  $(document).on("click", "#like_blog_button", (event) => {
    event.preventDefault();
    var formData = $("#like_blog_form").serialize();
    var slug = $("#like_blog_button").attr("value");

    $.ajax({
      type: "POST",
      url: `/like_blog/${slug}/`,
      data: formData,
      dataType: "json",
      success: (response) => {
        $("#like_section").html(response["like"]);
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
        
        $('#comment-trigger-like-section').hide();
    } else {
     
        $('#comment-trigger-like-section').show();
    }
    
    lastScrollTop = scrollTop;
});
});
