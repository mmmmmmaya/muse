'use strict';

// set up toggle-ability for app recording
var recording = false;
var song = [];

function toggleRecording() {
    recording = !recording;
}

function sendSongToServer() {
    var params = {
        "song": song
    };

    $.post("/api/save_song", params, function (data) {
        song = [];
    });
}

function recordButtonPressed(evt){
    if (recording) {
        sendSongToServer();
    }

    toggleRecording();
}

$('#record-button').click(recordButtonPressed);


// validate key pressed is a letter
// and action app based on input
function isLetter(char){
    return /^[A-Za-z]$/.test(char);
}

function actionApp(keyPressed) {
    var imgFilepath = 'static/images/' + keyPressed + '.png';
    var soundFilepath = 'static/sounds/' + keyPressed + '.mp3';

    var audio = new Audio(soundFilepath);

    audio.play();
    $('#image').attr('src', imgFilepath);
}

function updateSong(keyPressed) {
    song.push({
        "timestamp": Date.now(),
        "key": keyPressed
    });
}

function onKeyPress(evt) {
    var keyPressed = evt.key;

    if (recording && isLetter(keyPressed)){
        actionApp(keyPressed);
        updateSong(keyPressed);
    }
}

$(document).keypress(onKeyPress);
