'use strict';

var letterAnimationMap = {
    'a': function() {hexWave()},
    'b': function() {stipple()},
    'c': function() {explode()},
    'd': '',
    'e': '',
    'f': '',
    'g': '',
    'h': '',
    'i': '',
    'j': '',
    'k': '',
    'l': '',
    'm': '',
    'n': '',
    'o': '',
    'p': '',
    'q': '',
    'r': '',
    's': '',
    't': '',
    'u': '',
    'v': '',
    'w': '',
    'x': '',
    'y': '',
    'z': ''
}

var svgContainer = d3.select("svg");

function getRandomInt(min, max) {
    var min = Math.ceil(min);
    var max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

function chooseRandomX() {
    var max = svgContainer[0][0]['clientWidth'];

    return getRandomInt(0, max);
}

function chooseRandomY() {
    var max = svgContainer[0][0]['clientHeight'];

    return getRandomInt(0, max);
}

function chooseRandomSize() {
    return getRandomInt(1, 100);
}

function chooseRandomColor() {
    var colors = getThemeColors(currentTheme);
    var index = getRandomInt(0, colors.length);

    return colors[index];
}

function hexWave() {
    for (var i = 0; i < 20; i++){
        var x = chooseRandomX();
        var y = chooseRandomY();
        var radius = chooseRandomSize();
        var fill = chooseRandomColor();

        makeHexagon(radius, x, y, fill);
    }
}

function makeHexagon(radius, x, y, fill) {
    var h = (Math.sqrt(3)/2),
        hexagonData = [
          { "x":  radius+x,   "y": y}, 
          { "x":  radius/2+x, "y": radius*h+y},
          { "x": -radius/2+x, "y": radius*h+y},
          { "x": -radius+x,   "y": y},
          { "x": -radius/2+x, "y": -radius*h+y},
          { "x":  radius/2+x, "y": -radius*h+y}
        ];

    var drawHexagon = 
        d3.svg.line()
            .x(function(d) { return d.x; })
            .y(function(d) { return d.y; })
            .interpolate("cardinal-closed")
            .tension("1");

    var enterElements = 
        svgContainer.append("path")
                    .attr("d", drawHexagon(hexagonData))
                    .attr("stroke", "white")
                    .attr("stroke-width", 1)
                    .attr("fill", fill);
}
