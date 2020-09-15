
$(function(){
    $("#mysearch").on("keyup",function(){
        var formData = $("#search-form").serialize()
        var myUrl = $("#search-form").attr('data-url') || window.location.href
        $.ajax({
            method: 'GET',
            url: myUrl,
            data: formData,
            success: function (response) {
                $("#results_section").html(response['form'])
                // console.log($("results_section").html(response['form']))
            },
            error: function (rs, e) {
                console.log(rs.responseText);
            }
        })
    })
})

