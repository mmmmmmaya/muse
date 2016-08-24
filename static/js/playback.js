'use strict';

function waitThenPress(keypress, waitTime) {
    setTimeout(function() {                 // because of differences in indexing,
        currentTheme = keypress.theme - 1;  // theme id in the db is 1 more than in js
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
