$(function(){
//userprofile connections
    $(document).on("click", "#connection_butt", (event) => {
      event.preventDefault();
      var formData = $("#connection_form").serialize();
      var id = $("#connection_butt").attr('value')
      
      $.ajax({
        type: "POST",
        url: `/connection/${id}/`,
        data: formData,
        dataType: "json",
        success: (response) => {
          $("#connection_section").html(response["results"]);
        },
        error: (rs, e) => {
          console.log(rs.responseText);
        },
      });
    });

})