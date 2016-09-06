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
var hovers = ['', '#85c9cf', '#e7feff', '#bd8173', '#707070'];

function getNumThemes() {
    return themeColors.length;
}

function getThemeColors(theme) {
    return themeColors[theme-1];
}

function getThemeBg(theme) {
    return backgrounds[theme-1];
}

function updateThemeColors(theme) {
    updateThemeBgColor(theme);
    updateTextColor(theme);
    updateDropdowns(theme);
}

function nextTheme() {
    if (currentTheme === 5) {
        currentTheme = 1;
    } else {
        currentTheme++;
    }

    updateThemeColors(currentTheme);
}

function updateColor(element, color) {
    $(element).css('color', color);
}

function updateThemeBgColor(theme) {
    updateBgColor('body', backgrounds[theme-1]);
}

function updateBgColor (element, color) {
    $(element).css('background-color', color);
}

function updateHoverBg(element, notHovering, hovering) {
    $(element).hover(
        function() {
            updateBgColor(this, hovering);
        },

        function() {
            updateBgColor(this, notHovering);
        }
    );
}

function updateHoverText(element, notHovering, hovering) {
    $(element).hover(
        function() {
            updateColor(this, hovering);
        },

        function() {
            updateColor(this, notHovering);
        }
    );
}

function updateTextColor(theme) {
    var color;
    var index = theme -1;
    var updateWithHover = ['.navbar-brand', '.fa-facebook-square', '.fa-github',
                           '.fa-linkedin-square', '.dropdown-menu>li>a', '.navbar-nav>li>a'];
    var updateNoHover = ['#start-message', '#save-message-div'];

    for (var i = 0; i < updateWithHover.length; i++) {
        updateColor(updateWithHover[i], nonHovers[index]);
        updateHoverText(updateWithHover[i], nonHovers[index], hovers[index]);
    }

    for (var j = 0; j < updateNoHover.length; j++) {
        updateColor(updateNoHover[j], nonHovers[index]);
    }
}

function updateDropdowns(theme) {
    var index = theme - 1;
    var background = backgrounds[index];
    var navItems = '.navbar-nav>li>a';
    var toggler = navItems + '.dropdown-toggle';

    // set background for all pieces of dropdown menu
    updateBgColor('.dropdown-menu', 'transparent');
    updateBgColor('.dropdown-menu>li>a', 'transparent');

    // set the colors for dropdown toggle, both focused and unfocused
    $(toggler).focus(
        function() {
            updateBgColor(this, hovers[index]);
            updateColor(this, nonHovers[index]);
            updateHoverText(this, nonHovers[index], nonHovers[index]);
        }
    );

    $(toggler).blur(
        function() {
            updateBgColor(this, 'transparent');
            updateHoverText(this, nonHovers[index], hovers[index]);
        }
    );
}
