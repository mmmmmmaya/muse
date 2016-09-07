'use strict';

function makeDataIdSelector(recordingId) {
    return '[data-id*="' + recordingId + '"]';
}

function getElementByClassAndId(className, recordingId) {
    var dataIdSelector = makeDataIdSelector(recordingId);
    var divSelector = className + dataIdSelector;
    var nameDiv = $(divSelector);

    return nameDiv;
}

function toggleRenameForm(evt) {
    var recordingId = $(evt.originalEvent.target).data('id');

    var nameDiv = getElementByClassAndId('.recording-name', recordingId);
    var renameForm = getElementByClassAndId('.rename-form', recordingId);

    nameDiv.toggleClass('hide');
    renameForm.toggleClass('hide');
}

$('.rename-button').click(toggleRenameForm);
$('.cancel-rename').click(toggleRenameForm);


function updateRecordingNameDiv(data) {
    var nameDiv = getElementByClassAndId('.recording-name', data.recording_id);
    var html = data.title;

    nameDiv.html(html);

    $('.rename-form').addClass('hide');
    $('.recording-name').removeClass('hide');
}

function recordingRenamed(evt) {
    evt.preventDefault();
    $('#save-message-div').html('Saving ...');

    var params = $(evt.originalEvent.target).serialize();

    $.post("/rename", params, function (data) {
        updateMsgDivStatus(data.status);
        updateRecordingNameDiv(data);
    });
}

$('.rename-form').submit(recordingRenamed);


function recordingDeleted(evt) {
    $('#save-message-div').html('Deleting ...');
    console.log($(evt.originalEvent.target));
    var recordingId = $(evt.originalEvent.target).data('id');
    var params = {"recording_id": recordingId};
    console.log(params);

    $.post("/delete", params, function (data) {
        updateMsgDivStatus(data.status);
        var selector = makeDataIdSelector(data.id);
        $(selector).remove();
    });
}

$('.delete').click(recordingDeleted);


function updateButtonText(recordingId) {
    var toggleButton = getElementByClassAndId('.toggle-public', recordingId);

    toggleButton.toggleClass('public');

    var isPublic = toggleButton.hasClass('public');
    var toggleButtonHTML = isPublic ? 'Make Private' : 'Make Public';

    toggleButton.html(toggleButtonHTML);
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
