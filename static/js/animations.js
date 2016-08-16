'use strict';

var letterAnimationMap = {
    'a': function() {},
    'b': function() {},
    'c': function() {circleGrid()},
    'd': function() {},
    'e': function() {explode()},
    'f': function() {},
    'g': function() {},
    'h': function() {hexBurst()},
    'i': function() {implode()},
    'j': function() {},
    'k': function() {},
    'l': function() {},
    'm': function() {},
    'n': function() {},
    'o': function() {},
    'p': function() {},
    'q': function() {},
    'r': function() {raindrop()},
    's': function() {stipple()},
    't': function() {takeOff()},
    'u': function() {},
    'v': function() {},
    'w': function() {wiggle()},
    'x': function() {},
    'y': function() {},
    'z': function() {}
}

var svgContainer = d3.select("svg");
var svgWidth = svgContainer[0][0]['clientWidth'];
var svgHeight = svgContainer[0][0]['clientHeight'];

function getRandomInt(min, max) {
    var min = Math.ceil(min);
    var max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

function chooseRandomX() {
    return getRandomInt(0, svgWidth);
}

function chooseRandomY() {
    return getRandomInt(0, svgHeight);
}

function chooseRandomSize() {
    return getRandomInt(1, 50);
}

function chooseRandomColor() {
    var colors = getThemeColors(currentTheme);
    var index = getRandomInt(0, colors.length);

    return colors[index];
}

function hexBurst() {
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

    var enterElements = svgContainer.append("path")
                                    .attr("d", drawHexagon(hexagonData))
                                    .attr("stroke", "white")
                                    .attr("stroke-width", 1)
                                    .attr("fill", fill)
                                    .attr('class', 'magictime puffOut');
}

function makeCircle(radius, x, y, fill) {
    var circle = svgContainer.append("circle")
        .attr("cy", y)
        .attr("cx", x)
        .attr("r", radius)
        .attr("stroke", "white")
        .attr("stroke-width", 1)
        .attr("fill", fill);

    return circle;
}

function makeCircleWithVanish(radius, x, y) {
    var fill = chooseRandomColor();
    var circle = makeCircle(radius, x, y, fill);

    var randomTimeout = getRandomInt(1, 1500);
    setTimeout(function() {
        circle.attr('class', 'magictime vanishOut');
    }, randomTimeout);
}

function circleGrid() {
    var x = chooseRandomX();
    var y = chooseRandomY();
    var original_y = y;
    var radius = chooseRandomSize();

    for (var i = 0; i < 6; i++) {
        y = original_y;

        for (var j = 0; j < 6; j++) {
            makeCircleWithVanish(radius, x, y);
            y += (radius*2) + 2;
        }

        x += (radius*2) + 2;
    }
}

function takeOff() {
    var x = chooseRandomX();
    var y = chooseRandomY();
    var radius = chooseRandomSize();
    var fill = chooseRandomColor();

    var takeOffCircle = makeCircle(radius, x, y, fill);
    setTimeout(function() {
        takeOffCircle.attr('class', 'magictime tinRightOut');
    }, 1000);
}
