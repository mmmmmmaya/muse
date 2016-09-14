var codeProgress = [];
var dirs = ['left', 'down', 'up', 'right'];
var konamiCode = ['arrowup', 'arrowup',
                  'arrowdown', 'arrowdown',
                  'arrowleft', 'arrowright',
                  'arrowleft', 'arrowright',
                  'b', 'a'];
var score = 0;

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

    playDDR();
    playSong();

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
    updateScore();

    $(document).keydown(keepScore);

    getRecordedArrows(size, gap);
    flashScore();
}

function getXDims(size, gap) {
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

function getRecordedArrows(size, gap) {
    $.get('/fetch_konami', function(data) {
        var arrows = data.content;
        scrollArrows(size, gap, arrows);
    });
}

function makeArrow(direction, size, x) {
    var imagePath = '/static/images/color_' + direction + '.png';
    var className = 'arrow-scroll ' + direction;

    topSVGLayer.append('image')
               .attr('x', x)
               .attr('y', size * 10)
               .attr('height', size)
               .attr('width', size)
               .attr('xlink:href', imagePath)
               .attr('class', className);
}

function makeAndScrollArrow(direction, size, x, waitTime) {
    setTimeout(function() {
        makeArrow(direction, size, x);
    }, waitTime);
}

function scrollArrows(size, gap, arrows) {
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


/** Functions to keep score **/
function updateScore() {
    var html = 'Score: ' + score;
    $('#score').html(html);
}

function flashScore() {
    $('#score').addClass('ddr-score');
}

function isArrow(key) {
    var isArrow = false;

    if (dirs.indexOf(key) > -1) {
        isArrow = true;
    }

    return isArrow;
}

function checkProximityAndUpdateScore(keyPressed) {
    var selector = '#konami-svg g .arrow-scroll.' + keyPressed;
    var arrows = $(selector);

    var topArrows = $('.top-arrow');
    var topArrowOffset = topArrows.offset().top;

    for (var i = 0; i < arrows.length; i++) {
        var arrow = $(arrows[i]);
        var arrowOffset = arrow.offset().top;

        if (Math.abs(arrowOffset - topArrowOffset) < 30) {
            arrow.hide();
            score += 10;
        }
    }

    updateScore();
}

function keepScore(evt) {
    var keyPressed = evt.key.toLowerCase().replace('arrow', '');

    if (isArrow(keyPressed)) {
        checkProximityAndUpdateScore(keyPressed);
    }
}
