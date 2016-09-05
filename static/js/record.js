'use strict';

// set up toggle-ability for app recording
var appIsRecording = false;
var recordingArray = [];
var currentTheme = 1;
updateBgColor(currentTheme);


function sendSongToServer() {
    if (recordingArray.length > 0) {
        var params = {
            "keypresses": JSON.stringify(recordingArray)
        };

        $('#save-message-div').html('Saving ...');

        $.post("/save_recording", params, function (data) {
            recordingArray = [];
            updateMsgDivStatus(data.status);
        });
    }
}


function toggleRecording(evt) {
    $.get('/logged_in', function(data) {
        if (data.status === 'success') {

            if (appIsRecording) {
                sendSongToServer();
            } else {
                // so old save messages don't get confused with new ones
                clearMsgDiv();
            }

            appIsRecording = !appIsRecording;

        } else {
            var div = $('#start-message');
            div.html(data.message);
            div.show();
        }
    });
}


// validate key pressed is a letter
// and action app based on input
function isLetter(char) {
    return /^[a-z]$/.test(char);
}

function actionApp(keyPressed) {
    var soundFilepath = '/static/sounds/' + currentTheme + '/' + keyPressed + '.mp3';
    var audio = new Audio(soundFilepath);

    audio.play();
    letterAnimationMap[keyPressed]();
    collectGarbage();
}

function updateSong(keyPressed) {
    recordingArray.push({
        "timestamp": Date.now(),
        "key": keyPressed,
        "theme": currentTheme
    });
}

function hideStartMessage() {
    $('#start-message').hide();
}

function showHelp() {
    $('#helpModal').modal('toggle');
    hideStartMessage();
}

function onKeyPress(evt) {
    var keyPressed = evt.key.toLowerCase();

    if (isLetter(keyPressed)) {
        hideStartMessage();
        actionApp(keyPressed);

        if (appIsRecording) {
            updateSong(keyPressed);
        }
    } else if (keyPressed === ' ') {
        nextTheme();
    } else if (keyPressed === '?') {
        showHelp();
    } else if (keyPressed === 'enter') {
        toggleRecording();
    }
}

$(document).keydown(onKeyPress);
