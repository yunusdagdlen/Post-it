
function open_share_modal(postit_uuid,) {
    var link = '127.0.0.1:5000/postit' + postit_uuid
    $("#copy_uuid").text(link);
    $("#share_note").modal('show');
}

function open_edit_modal(editing_note_title, editing_note_text) {

    $("#edit_note").modal('show');
    $("#edit_note_title").text(editing_note_title);
}

