var themeColors = [
    ['#fd9696', '#fdca96', '#fdfd96', '#cafd96', '#96cafd', '#9696fd'],  // symphony
    ['#802e0a', '#cfb085', '#ffffff', '#afcfaf', '#85c9cf', '#6f4e37'],  // meditative
    ['#f2f3f4', '#91a3b0', '#e7feff', '#b2beb5', '#6e7f80', '#a2a2d0'],  // dubstep
    ['#ffffff', '#fce4a5', '#101936', '#bd8173', '#40233f', '#2c1e3f'],  // acoustic
    ['#ff005a', '#ffa500', '#daff00', '#5aff00', '#005aff', '#a500ff']   // chiptune
];

var backgrounds = [
    '#ededed',  // symphony: brass, strings, woodwind, percussion
    '#fff5ee',  // meditative: bells, gongs, singing bowls
    '#1f1f1f',  // dubstep: bass, synth, drums
    '#eac193',  // acoustic: piano, guitar
    '#ffffff'   // chiptune: 8bit
];

var nonHovers = ['', '#6f4e37', '#a2a2d0', '#2c1e3f', '#000000'];
var hovers = ['', '#802e0a', '#e7feff', '#bd8173', '#707070'];

function getNumThemes() {
    return themeColors.length;
}

function getThemeColors(theme) {
    return themeColors[theme-1];
}

function getThemeBg(theme) {
    return backgrounds[theme-1];
}

function nextTheme() {
    if (currentTheme === 5) {
        currentTheme = 1;
    } else {
        currentTheme++;
    }

    updateBgColor(currentTheme);
    updateTextColor(currentTheme);
}

function updateBgColor(theme) {
    $('body').css("background-color", backgrounds[theme-1]);
}


function updateTextColor(theme) {
    var color;
    var updateWithHover = ['.navbar-brand', '.navbar-default .navbar-nav>li>a',
                         '.fa-facebook-square', '.fa-github', '.fa-linkedin-square'];
    var updateNoHover = ['#start-message', '#save-message-div'];

    for (var i = 0; i < updateWithHover.length; i++) {
        $(updateWithHover[i]).css('color', nonHovers[theme-1]);

        $(updateWithHover[i]).hover(
            function() {
                $(this).css('color', hovers[theme-1]);
            },

            function() {
                $(this).css('color', nonHovers[theme-1]);
            }
        );
    }

    for (var j = 0; j < updateNoHover.length; j++) {
        $(updateNoHover[j]).css('color', nonHovers[theme-1]);
    }
}