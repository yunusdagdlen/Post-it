
function open_share_modal(postit_uuid) {
    var link = postit_uuid;
    $("#copy_uuid").text(link);
    $("#copied_hidden_link").val(link)
    $("#share_note").modal('show');
    $("#edit_note_modal").modal('hide');
    $("#copy_link_button").attr("onclick", `copy_single_note_url('${link}')`);

}

function open_edit_modal(title, uuid) {
    $("#edit_note_modal").modal('show');
    var get_text = $("#text_" + uuid).text();
    $("#postit_edit_title").val(title);
    $("#postit_edit_content").val(get_text);
    $("#hidden_uuid").val(uuid);
    console.log()

}

function del_button(id) {
    $.ajax({
        type: 'POST',
        url: `del/${id}`,
        success: function () {
            $(`#${id}`).fadeOut()
        },
        error: function () {
            alert('Error')
        }
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
    Swal.fire({
        position: 'center',
        icon: 'success',
        title: 'Copied to clipboard',
        showConfirmButton: false,
        timer: 1500
    })
}

function get_workspace_func() {
    workspace_id = document.cookie
    link = 'http://127.0.0.1:5000/?'
    copyText = link + workspace_id
    copyToClipboard(copyText);
    Swal.fire({
        position: 'center',
        icon: 'success',
        title: 'Your Workspace Link ,Copy to Clipboard',
        showConfirmButton: false,
        timer: 1500
    })
}

function copy_single_note_url(link) {
    var url = '127.0.0.1:5000'
    copyToClipboard(url + '/postit/' + link);
}

function open_single_note() {
    link = $("#copy_uuid").text()
    var win = window.open("" + "/postit/" + link, '_blank');
    if (win) {
        //Browser has allowed it to be opened
        win.focus();
    } else {
        //Browser has blocked it
        alert('Please allow popups for this website');
    }
}

function flip() {
    $('.card-2').toggleClass('flipped');
}

flag = true;

function flip_postit(id) {
    if (flag) {
        $(`#back_${id}`).css('display', 'none')
        $(`#front_${id}`).css('display', 'flex')
        $(`#front_${id}`).fadeOut()
        $(`#back_${id}`).fadeIn()
        flag = false
    } else {
        $(`#back_${id}`).css('display', '')
        $(`#front_${id}`).css('display', 'none')
        $(`#front_${id}`).fadeIn()
        $(`#back_${id}`).fadeOut()
        flag = true
    }
}
