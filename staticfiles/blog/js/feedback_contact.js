$(function () {

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


  $(document).on("submit", "#feedback_form", function (event) {
    event.preventDefault();

    const feedback = document.getElementById("feedform");

    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: {
        "feedback": feedback.value
      },
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

//   for contact form

});
