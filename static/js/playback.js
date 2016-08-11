'use strict';

function waitThenPress(keypress, waitTime) {
    // TODO make a more accurate timer
    setTimeout(function(){
        actionApp(keypress.next_key);
    }, waitTime);
}

function playbackRecording(content) {
    var waitTime = 0;
    var keypress = content[0];
    actionApp(keypress.this_key);

    for (var i = 0; i < content.length; i++) {
        waitTime += keypress.time_to_next;
        keypress = content[i];

        waitThenPress(keypress, waitTime);
    }
}

function playbackLinkClicked(evt) {
    var urlString = '/fetch_recording/' + this.id;

    $.get(urlString, function(data){
        if (data.status === 'success') {
            playbackRecording(data.content);
        }
        // TODO else{ display error or something }
    });
}

$('.playback').click(playbackLinkClicked);
