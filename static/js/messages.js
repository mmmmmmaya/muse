'use strict';

function updateMsgDivStatus(status) {
    var msgDiv = $('#save-message-div');

    if (status === 'success') {
        msgDiv.html('Saved!');
    } else {
        msgDiv.html('Error! ' + status);
    }
}

function clearMsgDiv() {
    $('#save-message-div').html('');
}
