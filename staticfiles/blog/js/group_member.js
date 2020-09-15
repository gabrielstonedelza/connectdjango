$(function(){
    // request to join group
    $(document).on('click','#join_group_button',(event)=>{
        event.preventDefault()

        var formData = $("#join_group_form").serialize()
        // var id = event.currentTarget.value;
        var id = $("#join_group_button").attr('value')
        console.log(id)

        $.ajax({
            type: 'POST',
            url: '/join_group/'+id+'/',
            data: formData,
            dataType: 'json',
            success:(response)=>{
                $("#join_group_section").html(response['form'])
            },
            error: (rs,e)=>{
                console.log(rs.responseText);
            }
        })
    })

    // add pending members
    $(document).on('click','#add_pending_member_button',(event)=>{
        event.preventDefault()

        var formData = $("#add_pending_members_form").serialize()
        var id = event.currentTarget.value;
        // var id = $("#add_pending_members_button").attr('value')
        console.log(id)

        $.ajax({
            type: 'POST',
            url: '/add_pending_members/'+id+'/',
            data: formData,
            dataType: 'json',
            success:(response)=>{
                $("#add_pending_members_section").html(response['form'])
            },
            error: (rs,e)=>{
                console.log(rs.responseText);
            }
        })
    })

    // remove members
    $(document).on('click','#remove_member_button',(event)=>{
        event.preventDefault()

        var formData = $("#remove_member_form").serialize()
        var id = event.currentTarget.value;
        console.log(id)

        $.ajax({
            type: 'POST',
            url: '/remove_member/'+id+'/',
            data: formData,
            dataType: 'json',
            success:(response)=>{
                $("#remove_members_section").html(response['form'])
            },
            error: (rs,e)=>{
                console.log(rs.responseText);
            }
        })
    })
})