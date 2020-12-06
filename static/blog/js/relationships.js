$(function () {
  //userprofile connections
  $(document).on("click", "#connection_butt", (event) => {
    event.preventDefault();
    var formData = $("#connection_form").serialize();
    var id = $("#connection_butt").attr("value");

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

  // add pending members
  $(document).on("click", "#add_pending_member_button", (event) => {
    event.preventDefault();

    var formData = $("#add_pending_members_form").serialize();
    var id = event.currentTarget.value;

    $.ajax({
      type: "POST",
      url: "/add_pending_members/" + id + "/",
      data: formData,
      dataType: "json",
      success: (response) => {
        $("#add_pending_members_section").html(response["pending"]);
      },
      error: (rs, e) => {
        console.log(rs.responseText);
      },
    });
  });

  // add new members
  $(document).on("click", "#add_new_member_button", (event) => {
    event.preventDefault();

    var formData = $("#add_new_members_form").serialize();
    var id = event.currentTarget.value;

    $.ajax({
      type: "POST",
      url: "/add_members/" + id + "/",
      data: formData,
      dataType: "json",
      success: (response) => {
        $("#add_new_members_section").html(response["can_chat"]);
        $("#my-members").html(response["can_chat"]);
      },
      error: (rs, e) => {
        console.log(rs.responseText);
      },
    });
  });

  // request to join room
  $(document).on("click", "#join_room_button", (event) => {
    event.preventDefault();

    var formData = $("#join_room_form").serialize();
    var slug = $("#join_room_button").attr("value");

    $.ajax({
      type: "POST",
      url: "/join_room/" + slug + "/",
      data: formData,
      dataType: "json",
      success: (response) => {
        $("#join_room_section").html(response["joinroom"]);
      },
      error: (rs, e) => {
        console.log(rs.responseText);
      },
    });
  });
});
