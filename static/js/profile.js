'use strict';

function makeDataIdSelector(recordingId) {
    return '[data-id*="' + recordingId + '"]';
}

function recordingRenamed(evt) {
    evt.preventDefault();
    $('#save-message-div').html('Saving ...');

    var params = $(evt.originalEvent.target).serialize();

    $.post("/rename", params, function (data) {
        updateMsgDivStatus(data.status);
    });
}

$('.rename-form').submit(recordingRenamed);


function recordingDeleted(evt) {
    $('#save-message-div').html('Deleting ...');

    var recordingId = $(evt.originalEvent.target).data('id');
    var params = {"recording_id": recordingId};

    $.post("/delete", params, function (data) {
        updateMsgDivStatus(data.status);
        var selector = makeDataIdSelector(data.id);
        $(selector).remove();
    });
}

$('.delete').click(recordingDeleted);


function updateButtonText(recordingId) {
    var dataIdSelector = makeDataIdSelector(recordingId);
    var buttonSelector = '.toggle-public' + dataIdSelector;
    var toggleButton = $(buttonSelector);

    var isPublic = toggleButton.hasClass('public');
    var toggleButtonHTML = isPublic ? 'Make Private' : 'Make Public';

    toggleButton.html(toggleButtonHTML);
    toggleButton.toggleClass('public');
}

function toggleRecordingPublic(evt) {
    $('#save-message-div').html('Saving ...');

    var recordingId = $(evt.originalEvent.target).data('id');
    var params = {"recording_id": recordingId};

    $.post("/toggle_public", params, function (data) {
        updateMsgDivStatus(data.status);
        updateButtonText(recordingId);
    });
}

$('.toggle-public').click(toggleRecordingPublic);


function setupFacebookButtons(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];

    if (d.getElementById(id)) {
        return;
    }

    js = d.createElement(s);
    js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.7";
    fjs.parentNode.insertBefore(js, fjs);
}

$(document).ready(function() {
        setupFacebookButtons(document, 'script', 'facebook-jssdk');
});
