'use strict';

function onKeyPress(evt) {
    var keyPressed = evt.key;
    var img_filepath = 'static/letters/' + keyPressed + '.png';
    var sound_filepath = 'static/sounds/' + keyPressed + '.mp3';

    $('#image').attr('src', img_filepath);
}

$(document).keypress(onKeyPress);