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
    $('#home-button').addClass('hide');

    playSong();
    playDDR();

    $('#home-button').removeClass('hide');
}

function playSong() {
    var soundFilepath = 'static/sounds/mario.mp3';
    var audio = new Audio(soundFilepath);
    audio.play();
}

function playDDR() {
    var size = 120;
    var gap = size / 8;

    showTopArrows(size, gap);
    updateScore(0);

    scrollArrows(size, gap);
    flashScore();
}

function getXDims(size, gap) {
    var dirs = ['left', 'down', 'up', 'right'];
    var startX = (svgWidth / 2) - ((2 * size) + (1.5 * gap));
    var xDims = {

    };

    for (var i = 0; i < dirs.length; i++) {
        var dim = startX + (i * (size + gap));
        var direction = dirs[i];
        xDims[direction] = dim;
    }

    return xDims;
}

function showTopArrows(size, gap) {
    var dirs = ['left', 'down', 'up', 'right'];
    var xDims = getXDims(size, gap);

    for (var i = 0; i < dirs.length; i++) {
        var direction = dirs[i];
        var imagePath = '/static/images/' + direction + '.png';
        var x = xDims[direction];

        bottomSVGLayer.append('image')
                      .attr('class', 'top-arrow')
                      .attr('x', x)
                      .attr('y', size/2)
                      .attr('height', size)
                      .attr('width', size)
                      .attr('xlink:href', imagePath);
    }
}

function getRecordedArrows() {
  return[{'time_to_next_arrow': 500,
          'direction': 'up'},
          {'time_to_next_arrow': 500,
          'direction': 'down'},
          {'time_to_next_arrow': 500,
          'direction': 'left'},
          {'time_to_next_arrow': 0,
          'direction': 'right'}]
}

function makeArrow(direction, size, x) {
    var imagePath = '/static/images/color_' + direction + '.png';

    topSVGLayer.append('image')
               .attr('x', x)
               .attr('y', svgHeight)
               .attr('height', size)
               .attr('width', size)
               .attr('xlink:href', imagePath)
               .attr('class', 'arrow-scroll');
}

function makeAndScrollArrow(direction, size, x, waitTime) {
    setTimeout(function() {
        makeArrow(direction, size, x);
    }, waitTime);
}

function scrollArrows(size, gap) {
    var arrows = getRecordedArrows();
    var waitTime = 1;
    var xDims = getXDims(size, gap);

    for (var i = 0; i < arrows.length; i++) {
        arrow = arrows[i];
        var direction = arrow.direction;

        var x = xDims[direction];

        makeAndScrollArrow(direction, size, x, waitTime);
        waitTime += arrow.time_to_next_arrow;
    }
}

function updateScore(score) {
    var html = 'Score: ' + score;
    $('#score').html(html);
}

function flashScore() {
    $('#score').addClass('ddr-score');
}
