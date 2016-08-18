var codeProgress = [];
var konamiCode = ['arrowup', 'arrowup',
                  'arrowdown', 'arrowdown',
                  'arrowleft', 'arrowright',
                  'arrowleft', 'arrowright',
                  'b', 'a'];

/** Functions to Track User Progress **/
function konamiTracker(key) {
    var key = key.toLowerCase();
    var nextNeededIndex = codeProgress.length;

    if (key === konamiCode[nextNeededIndex]) {
        codeProgress.push(key);
        checkCodeComplete();
    } else {
        codeProgress = [];
    }
}

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
    playSong();
    playDDR();

    collectGarbage();
}

function playSong() {
    var soundFilepath = 'static/sounds/mario.mp3';
    var audio = new Audio(soundFilepath);
    audio.play();
}

function playDDR() {
    showTopArrows();
    scrollRandomArrows();
}

function showTopArrows() {
    var arrowStartPosition = 5
    var arrowSpacing = 60
    var verticalStrokeColor = "black"
    var arrowYStartPosition = 5
    var arrowYEndStartPosition = 150
    var margin = 150;

    var labelLine = svgContainer.append("line")
            .attr("x1", arrowStartPosition + margin)
            .attr("y1", arrowYStartPosition)
            .attr("x2", arrowStartPosition + margin)
            .attr("y2", arrowYEndStartPosition)
            .attr("stroke-width", 2)
            .attr("stroke", verticalStrokeColor);

    var right = svgContainer.append("line")
            .attr("x1", arrowStartPosition + margin)
            .attr("y1", arrowYStartPosition)
            .attr("x2", 20 + margin)
            .attr("y2", 20)
            .attr("stroke-width", 2)
            .attr("stroke", "black");

    var left = svgContainer.append("line")
            .attr("x1", right.attr("x1"))
            .attr("y1", right.attr("y1"))
            .attr("x2", right.attr("x2")-30)
            .attr("y2", right.attr("y2"))
            .attr("stroke-width", 2)
            .attr("stroke", "black");
}
