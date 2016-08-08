'use strict';

function isLetter(char){
    return /^[A-Za-z]$/.test(char);
}

function onKeyPress(evt) {
    var keyPressed = evt.key;

    if (isLetter(keyPressed)){
        var img_filepath = 'static/images/' + keyPressed + '.png';
        var sound_filepath = 'static/sounds/' + keyPressed + '.mp3';
        var audio = new Audio(sound_filepath);
        audio.play();

        $('#image').attr('src', img_filepath);
    }
}

$(document).keypress(onKeyPress);