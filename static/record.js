'use strict';

// set up toggle-ability for app recording
var recording = false;

function toggleRecording(evt) {
    recording = !recording;
}

$('#record-button').click(toggleRecording);


// validate key pressed is a letter
// and action app based on input
function isLetter(char){
    return /^[A-Za-z]$/.test(char);
}

function onKeyPress(evt) {
    var keyPressed = evt.key;

    if (recording && isLetter(keyPressed)){
        var imgFilepath = 'static/images/' + keyPressed + '.png';
        var soundFilepath = 'static/sounds/' + keyPressed + '.mp3';
        var audio = new Audio(soundFilepath);

        audio.play();
        $('#image').attr('src', imgFilepath);
    }
}

$(document).keypress(onKeyPress);
