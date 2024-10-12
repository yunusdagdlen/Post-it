function open_share_modal(postit_uuid) {
    var link = postit_uuid;
    $("#copy_uuid").text(link);
    $("#copied_hidden_link").val(link)
    $("#share_note").modal('show');
    $("#edit_note_modal").modal('hide');
    $("#copy_link_button").attr("onclick", `copy_single_note_url('${link}')`);

}

function open_edit_modal(title, uuid) {
    $.ajax({
        type: 'GET',
        url: `get_note_text/${uuid}`,
        success: function (data) {
            console.log(data);
            let get_text = data.note
            $("#postit_edit_title").val(title);
            $("#postit_edit_content").val(get_text);
            $("#hidden_uuid").val(uuid);
            $("#edit_note_modal").modal('show');
        },
        error: function () {
            alert('Error')
        }
    });
}

function delete_postit(id) {
    $.ajax({
        type: 'POST',
        url: `del/${id}`,
        success: function () {
            const urlParams = new URLSearchParams(window.location.search);
            const mode = urlParams.get('mode');
            if (mode === 'active') {
                $(`#${id}`).fadeOut()
            } else {
                location.reload();
            }

        },
        error: function () {
            alert('Error')
        }
    });
}

function change_filter(filter) {
    const workspace_id = Cookies.get('workspace_uuid');
    const link = window.location.pathname;
    final_link = link + '?workspace_uuid=' + workspace_id + '&mode=' + filter;
    window.location.href = final_link
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
    const workspace_id = Cookies.get('workspace_uuid');
    const link = window.location.href;
    copyText = link + '?workspace_uuid=' + workspace_id
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
