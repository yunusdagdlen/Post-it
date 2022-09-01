function open_share_modal(postit_uuid) {
    var link = '127.0.0.1:5000/postit' + postit_uuid
    $("#copy_uuid").text(link);
    $("#share_note").modal('show');
    $("#edit_note_modal").modal('hidden')
}

function open_edit_modal(title,content,uuid) {
    $("#edit_note_modal").modal('show');
    $("#postit_edit_title").val(title);
    $("#postit_edit_content").val(content)
    $("#hidden_uuid").val(uuid)

}

function get_workspace_func(){
    workspace_id=document.cookie
    link='http://127.0.0.1:5000/?'
    $("#show_copy_workspace").text('copy')
    $("#get_workspace").val(link+workspace_id)
}
