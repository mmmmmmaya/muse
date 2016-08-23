'use strict';

function waitThenPress(keypress, waitTime) {
    setTimeout(function() {
        currentTheme = keypress.theme;
        actionApp(keypress.key_pressed);
    }, waitTime);
}

function playbackRecording(content) {
    var keypress;
    var waitTime = 1;

    for (var i = 0; i < content.length; i++) {
        keypress = content[i];
        waitThenPress(keypress, waitTime);
        waitTime += keypress.time_to_next;
    }
}

function playbackPageLoaded(evt) {
    var recordingId = $('#svg').data('id');
    var urlString = '/fetch_recording/' + recordingId;

    $.get(urlString, function(data) {
        if (data.status === 'success') {
            playbackRecording(data.content);
        } else {
            alert('Could not load recording.');
        }
    });
}

$(document).ready(playbackPageLoaded);
