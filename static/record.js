'use strict';

// set up toggle-ability for app recording
var appIsRecording = false;
var recordingArray = [];
// TODO placeholder for now until I get multiple themes set up
var currentTheme = 1;

function toggleRecording() {
    // TODO probably update button text or img to indicate if recording is active
    appIsRecording = !appIsRecording;
}

function sendSongToServer() {
    // TODO potentially ask user if they actually want to store the recording first
    if (recordingArray.length > 0) {
        var params = {
            "recording": JSON.stringify(recordingArray)
        };

        $.post("/api/save_recording", params, function (data) {
            recordingArray = [];
        });
    }
}

function recordButtonPressed(evt){
    if (appIsRecording) {
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
    recordingArray.push({
        "timestamp": Date.now(),
        "key": keyPressed,
        "theme": currentTheme
    });
}

function onKeyPress(evt) {
    var keyPressed = evt.key;

    if (isLetter(keyPressed)) {
        actionApp(keyPressed);

        if (appIsRecording){
            updateSong(keyPressed);
        }
    }
}

$(document).keypress(onKeyPress);
