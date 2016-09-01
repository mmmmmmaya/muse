var codeProgress = [];
var konamiCode = ['arrowup', 'arrowup',
                  'arrowdown', 'arrowdown',
                  'arrowleft', 'arrowright',
                  'arrowleft', 'arrowright',
                  'b', 'a'];

/** Functions to Track User Progress **/
function konamiTracker(evt) {
    var key = evt.key.toLowerCase();
    var nextNeededIndex = codeProgress.length;

    if (key === konamiCode[nextNeededIndex]) {
        codeProgress.push(key);
        checkCodeComplete();
    } else {
        codeProgress = [];
    }
}

$(document).keydown(konamiTracker);

function checkCodeComplete() {
    var equal = false;

    if (konamiCode.length === codeProgress.length) {
        equal = arraysEqual(konamiCode, codeProgress);
    }

    if (equal) {
        konamiRedirect();
    }
}

function arraysEqual(arrayA, arrayB) {
    var equals = true;

    for (var i = 0; i < arrayA.length; i++) {
        if (arrayA[i] !== arrayB[i]) {
            equals = false;
            break;
        }
    }

    return equals;
}

function konamiRedirect() {
    var form = $('<form action="/" method="POST"></form>');
    form.append('<input type="hidden" name="konami" value="konami" />');
    form.append('<input type="submit" />');
    form.submit();
}

/** Functions to show reward **/
function playKonamiPrize() {
    $('#home-button').toggle();

    playSong();
    playDDR();

    $('#home-button').toggle();
}

function playSong() {
    var soundFilepath = 'static/sounds/mario.mp3';
    var audio = new Audio(soundFilepath);
    audio.play();
}

function playDDR() {
    showTopArrows();
    updateScore(0);

    var score = scrollArrows();
    flashScore(score);
}

function showTopArrows() {
    var dirs = ['left', 'down', 'up', 'right'];
    var size = 120;
    var gap = size / 8;
    var startX = (svgWidth / 2) - ((2 * size) + (1.5 * gap));

    for (var i = 0; i < dirs.length; i++) {
        var imagePath = '/static/images/' + dirs[i] + '.png';
        var x = startX + (i * (size + gap));

        bottomSVGLayer.append('image')
                      .attr('class', 'top-arrow')
                      .attr('x', x)
                      .attr('y', size/2)
                      .attr('height', size)
                      .attr('width', size)
                      .attr('xlink:href', imagePath);
    }
}

function scrollArrows() {
    flashScore(100);
}

function updateScore(score) {
    var html = 'Score: ' + score;

    topSVGLayer.append('text')
               .attr('x', 30)
               .attr('y', 100)
               .attr('id', 'score')
               .attr('font-size', '200%')
               .html(html);
}

function flashScore(score) {
    $('#score').addClass('ddr-score');
}
