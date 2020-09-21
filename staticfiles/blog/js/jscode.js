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

  // for swiper
  var swiper = new Swiper('.swiper-container', {
    effect: 'coverflow',
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: 'auto',
    coverflowEffect: {
      rotate: 50,
      stretch: 0,
      depth: 100,
      modifier: 1,
      slideShadows: true,
    },
    pagination: {
      el: '.swiper-pagination',
    },
  });
});
