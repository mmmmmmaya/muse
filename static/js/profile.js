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

        var dataIdSelector = makeDataIdSelector();

        $('.rename-form').find(dataIdSelector)
                        .attr('value', data.title);
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
    var toggleButton = $('.toggle-public').find(dataIdSelector)[0];
    console.log(toggleButton);
    // if (toggleButton.classList.)
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
