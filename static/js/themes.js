var themeColors = [
    ['#fd9696', '#fdca96', '#fdfd96', '#cafd96', '#96cafd', '#9696fd'],  // bubbly
    ['#802e0a', '#cfb085', '#ffffff', '#afcfaf', '#85c9cf', '#6f4e37'],  // meditative
    ['#f2f3f4', '#91a3b0', '#e7feff', '#b2beb5', '#6e7f80', '#a2a2d0'],  // dubstep
    ['#b06f84', '#b07b6f', '#b09b6f', '#a5b06f', '#6fa5b0', '#7b6fb0'],  // acoustic
    ['#ff005a', '#ffa500', '#daff00', '#5aff00', '#005aff', '#a500ff']   // weird al
]

var grays = [
    '#ededed',  // bubbly
    '#fff5ee',  // meditative
    '#1f1f1f',  // dubstep
    '#5a5a5a',  // acoustic
    '#ffffff'   // weird al
]

function getThemeColors(theme) {
    return themeColors[theme];
}

function getThemeGray(theme) {
    return grays[theme];
}

function updateBgColor(theme) {
    $('body').css("background-color", grays[theme]);
}