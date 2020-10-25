$(function(){

  // $(".reply-btn").on('click',function(){
  //   $(this).parent().parent().next('.replies-comments').fadeToggle();
  // });
  setTimeout(function(){
    $(".alert").slideUp(3000);
  },5000);

  //comment functions
  $(document).on('submit', '.comment-form', function (event) {
    event.preventDefault();
    $.ajax({
      type:'POST',
      url:$(this).attr('action'), 
      data:$(this).serialize(),
      dataType:'json',
      success:function(response){
        $("#comments_section").html(response['comments']);
        $("input").val('');
        $(".reply-btn").on('click',function(){
          $(this).parent().parent().next('.replies-comments').fadeToggle();
          $("textarea").val('');
        });

      },
      error:function(rs,e){
        console.log(rs.responseText);
      }
    });
  });

  // $(document).on('submit','.reply-form',function(event){
  //   event.preventDefault();
  //   $.ajax({
  //     type:'POST',
  //     url:$(this).attr('action'),
  //     data:$(this).serialize(),
  //     dataType:'json',
  //     success:function(response){
  //       $(".main-comment-section").html(response['comments']);
  //       $("input").val('');
  //       $(".reply-btn").on('click',function(){
  //         $(this).parent().parent().next('.replies-comments').fadeToggle();
  //         $("input").val('');
  //       });

  //     },
  //     error:function(rs,e){
  //       console.log(rs.responseText);
  //     }
  //   });
  // });

})