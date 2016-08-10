'use strict';

function playbackRecording(steps) {
    console.log('got steps');
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
