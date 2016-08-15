'use strict';

function waitThenPress(keypress, waitTime) {
    setTimeout(function(){
        actionApp(keypress.next_key);
    }, waitTime);
}

function playbackRecording(content) {
    var waitTime = 1;

    for (var i = 0; i < content.length; i++) {
        keypress = content[i];
        waitThenPress(keypress, waitTime);
        waitTime += keypress.time_to_next;
    }
}

function playbackButtonClicked(evt) {
    var urlString = '/fetch_recording/' + this.id;

    $.get(urlString, function(data){
        if (data.status === 'success') {
            playbackRecording(data.content);
        } else {
            alert('Could not load recording.');
        }
    });
}

$('.playback').click(playbackButtonClicked);
