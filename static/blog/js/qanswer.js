$(function(){

  setTimeout(function(){
    $(".alert").slideUp(3000);
  },5000);

 

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 
const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
  beforeSend:(xhr) =>{
    xhr.setRequestHeader("X-CSRFTOKEN",  csrftoken)
  }
})


   //comment functions
   $(document).on('submit', '.comment-form', function (event) {
    event.preventDefault();
    const comment = document.getElementById('commentform');
    $.ajax({
      type:'POST',
      url:$(this).attr('action'), 
      data:{
        "comment": comment.value
      },
      dataType:'json',
      success:function(response){
        $("#comments_section").html(response['comments']);
        $("input").val('');
      },
      error:function(rs,e){
        console.log(rs.responseText);
      }
    });
  });
})