$(document).ready( function() {
    $('#btn_update').click( function () {
        console.log('click in button')
    });

    $('#chk_all_books').change( function () {
        console.log('change en checkbox')
    });

    // evento al seleccionar un usuario
    $('#user_selected').change( function () {
        console.log('change')
        var optionSelected = $("option:selected", this);
        var valueSelected = this.value;
        var chkSelectedAllBooks =  $('#chk_all_books').is(':checked');
        var csrf = $("input[name=csrfmiddlewaretoken]").val();
        console.log(csrf)
        $.ajax({
            method : "GET",
            url : "/favoritesApp/load_books_user/"+valueSelected,
            dataType : "JSON",
            data : {
                csrfmiddlewaretoken: csrf
            }
        })
        .done (function(response){
            console.log(response)
            var size = Object.keys(response["alert"]).length
            if ( size > 0 ) {
                alert(response["alert"])
                //$('#messages').html(JSON.stringify(response["errors"]));
            }
        })

    });

});

function deleteMessage(id) {
    console.log('click mensaje: ' + id)
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log(csrf)
    $.ajax({
        method : "GET",
        url : "/wall/delete_msg_ajax/"+id,
        dataType : "JSON",
        data : {
            csrfmiddlewaretoken: csrf
        }
    })
    .done (function(response){
        console.log(response)
        var size = Object.keys(response["alert"]).length
        if ( size > 0 ) {
            alert(response["alert"])
            //$('#messages').html(JSON.stringify(response["errors"]));
        }
    })
}

function deleteComment(id) {
    console.log('click comentario: ' + id)
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log(csrf)
    $.ajax({
        method : "GET",
        url : "/wall/delete_comment_ajax/"+id,
        dataType : "JSON",
        data : {
            csrfmiddlewaretoken: csrf
        }
    })
    .done (function(response){
        console.log(response)
        var size = Object.keys(response["alert"]).length
        if ( size > 0 ) {
            alert(response["alert"])
            //$('#messages').html(JSON.stringify(response["errors"]));
        }
    })

}

function addMessage(){
    var data = $("#formMessage").serialize()
    $.ajax({
        method : "POST",
        url : "/wall/add_message_ajax",
        data : data,
        dataType : "JSON"
    })
    .done (function(response){
        var size = Object.keys(response["alert"]).length
        if ( size > 0 ) {
            alert(response["alert"])
        } else {
            console.log("no hay mensajes")
        }

    })
}

function addComment(formComment){
    var data = $("#"+formComment).serialize()
    $.ajax({
        method : "POST",
        url : "/wall/add_comment_ajax",
        data : data,
        dataType : "JSON"
    })
    .done (function(response){
        var size = Object.keys(response["alert"]).length
        if ( size > 0 ) {
            alert(response["alert"])
        } else {
            console.log("no hay mensajes")
        }

    })
    location.reload();
}
