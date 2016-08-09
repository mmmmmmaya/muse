'use strict';

// set up toggle-ability for app recording
var recording = false;
var song = [];

function toggleRecording() {
    // TODO probably update button text or img to indicate if recording is active
    recording = !recording;
}

function sendSongToServer() {
    // TODO potentially ask user if they actually want to store the song first
    if (song.length > 0) {
        var params = {
            "song": JSON.stringify(song)
        };

        $.post("/api/save_song", params, function (data) {
            song = [];
        });
    }
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

    if (isLetter(keyPressed)) {
        actionApp(keyPressed);

        if (recording){
            updateSong(keyPressed);
        }
    }
}

$(document).keypress(onKeyPress);
