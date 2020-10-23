$(function (){
    $(document).on('click','#approve_button',(event)=>{
        event.preventDefault()
        var formData = $("#approve_file_form").serialize();
        var pk = $("#approve_button").attr('value')

        $.ajax({
            type: "POST",
            url: `/project-file/${pk}/approve_code/`,
            data: formData,
            dataType: "json",
            success: (response) => {
              $("#approve_file_section").html(response["file"]);
            },
            error: (rs, e) => {
              console.log(rs.responseText);
            },
          });
    })
})