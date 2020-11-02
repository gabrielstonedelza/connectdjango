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
$(document).on("submit", "#contact_form", function (event) {
    event.preventDefault();
    message = "Thank you for contacting us we will get back to you soon"

    const name = document.getElementById('contact_name')
    const email = document.getElementById('contact_email')
    const subject = document.getElementById('subject')
    const cmessage = document.getElementById('contact_message')
    $.ajax({
      type: "POST",
      url: $(this).attr("action"),
      data: {
        "name": name.value,
        "email": email.value,
        "subject": subject.value,
        "message": cmessage.value
      },
      dataType: "json",
      success: function (response) {
        $("#contact_form_section").html(response["form"]);
        $("textarea").val("");
        $("input").val("");
        $("#showmessage_success").html(message)
        setTimeout(function () {
            $("#showmessage_success").slideUp(3000);
          }, 5000);
      },
      error: function (rs, e) {
        console.log(rs.responseText);
      },
    });
  });

});
