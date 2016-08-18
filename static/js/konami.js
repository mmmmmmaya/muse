var codeProgress = [];
var konamiCode = ['arrowup', 'arrowup',
                  'arrowdown', 'arrowdown',
                  'arrowleft', 'arrowright',
                  'arrowleft', 'arrowright',
                  'b', 'a'];


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

function checkCodeComplete() {
    var equal = false;

    if (konamiCode.length === codeProgress.length) {
        equal = arraysEqual(konamiCode, codeProgress);
    }

    if (equal) {
        playKonamiPrize();
    }
}

function konamiTracker(key) {

    var key = key.toLowerCase();
    var nextNeededIndex = codeProgress.length;

    if (key === konamiCode[nextNeededIndex]) {
        console.log('match');
        codeProgress.push(key);
        checkCodeComplete();
    } else {
        codeProgress = [];
    }
}

function playKonamiPrize() {

}
