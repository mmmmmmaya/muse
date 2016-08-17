var themeColors = [
    ['#fd9696', '#fdca96', '#fdfd96', '#cafd96', '#96cafd', '#9696fd'],  // bubbly
    ['#802e0a', '#cfb085', '#ffffff', '#afcfaf', '#85c9cf', '#6f4e37'],  // meditative
    ['#f2f3f4', '#91a3b0', '#e7feff', '#b2beb5', '#6e7f80', '#a2a2d0'],  // dubstep
    ['#ffffff', '#fce4a5', '#101936', '#bd8173', '#40233f', '#2c1e3f'],  // acoustic
    ['#ff005a', '#ffa500', '#daff00', '#5aff00', '#005aff', '#a500ff']   // weird al
]

var backgrounds = [
    '#ededed',  // bubbly
    '#fff5ee',  // meditative
    '#1f1f1f',  // dubstep
    '#eac193',  // acoustic
    '#ffffff'   // weird al
]

function getThemeColors(theme) {
    return themeColors[theme];
}

function getThemeGray(theme) {
    return backgrounds[theme];
}

function updateBgColor(theme) {
    $('body').css("background-color", backgrounds[theme]);
}