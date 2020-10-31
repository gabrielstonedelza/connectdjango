$(function(){
//userprofile connections
    $(document).on("click", "#connection_butt", (event) => {
      event.preventDefault();
      var formData = $("#connection_form").serialize();
      var pk = $("#connection_butt").attr('value')
      
      $.ajax({
        type: "POST",
        url: `/connection/${pk}/`,
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
//    profile connections
// $(document).on("click", "#profile_connection_butt", (event) => {
//       event.preventDefault();
//       var formData = $("#profile_connection_form").serialize();
//       var pk = event.currentTarget.value

//       $.ajax({
//         type: "POST",
//         url: '/profile_following/'+pk+'/',
//         data: formData,
//         dataType: "json",
//         success: (response) => {
//           $("#profile_connection_section").html(response["results"]);
//         },
//         error: (rs, e) => {
//           console.log(rs.responseText);
//         },
//       });
//     });
//    followers
// $(document).on("click", "#profile_connection_followers_butt", (event) => {
//       event.preventDefault();
//       var formData = $("#profile_connection_followers_form").serialize();
//       var pk = event.currentTarget.value

//       $.ajax({
//         type: "POST",
//         url: '/profile_connection_followers/'+pk+'/',
//         data: formData,
//         dataType: "json",
//         success: (response) => {
//           $("#profile_connection_followers_section").html(response["results"]);
//         },
//         error: (rs, e) => {
//           console.log(rs.responseText);
//         },
//       });
//     });

    // userprofile connection

    // $(document).on("click", "#userprofile_connection_button", (event) => {
    //   event.preventDefault();
    //   var formData = $("#userprofile_connection_form").serialize();
    //   var pk = event.currentTarget.value

    //   $.ajax({
    //     type: "POST",
    //     url: '/userprofile_connection/'+pk+'/',
    //     data: formData,
    //     dataType: "json",
    //     success: (response) => {
    //       $("#userprofile_connection_section").html(response["results"]);
    //     },
    //     error: (rs, e) => {
    //       console.log(rs.responseText);
    //     },
    //   });
    // });
    // userprofile followers connection
    // $(document).on("click", "#userprofile_followers_connection_button", (event) => {
    //   event.preventDefault();
    //   var formData = $("#userprofile_followers_connection_form").serialize();
    //   var pk = event.currentTarget.value

    //   $.ajax({
    //     type: "POST",
    //     url: '/userprofile_followers_connection/'+pk+'/',
    //     data: formData,
    //     dataType: "json",
    //     success: (response) => {
    //       $("#userprofile_followers_section").html(response["results"]);
    //     },
    //     error: (rs, e) => {
    //       console.log(rs.responseText);
    //     },
    //   });
    // });

})