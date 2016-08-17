'use strict';

var letterAnimationMap = {
    'a': function() {footprints();},
    'b': function() {bundle();},
    'c': function() {circleGrid();},
    'd': function() {chord();},
    'e': function() {explode();},
    'f': function() {force();},
    'g': function() {smile();},
    'h': function() {hexBurst();},
    'i': function() {implode();},
    'j': function() {partition();},
    'k': function() {staffTwirl();},
    'l': function() {flash();},
    'm': function() {wink();},
    'n': function() {stripes();},
    'o': function() {rainbow();},
    'p': function() {pack();},
    'q': function() {suckedIn();},
    'r': function() {raindrop();},
    's': function() {stipple();},
    't': function() {takeOff();},
    'u': function() {tree();},
    'v': function() {treemap();},
    'w': function() {wiggle();},
    'x': function() {stack();},
    'y': function() {pie();},
    'z': function() {zigzag();}
}

var svgContainer = d3.select('svg');
var svgHeight;
var svgWidth;
resetSVGDims();

function getRandomInt(min, max) {
    var min = Math.ceil(min);
    var max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

function chooseRandomDim(max, offset) {
    var offset = offset || 0;
    var random = getRandomInt(0, max);

    if (offset !== 0) {
        random += offset;
    }

    return random;
}

function chooseRandomSizeMultiple() {
    return getRandomInt(1, 50);
}

function chooseRandomSizeOne() {
    return getRandomInt(25, 300);
}

function chooseRandomColor() {
    var colors = getThemeColors(currentTheme);
    var index = getRandomInt(0, colors.length);

    return colors[index];
}

function collectGarbage() {
    var maxElements = 500;
    var svg = $('#svg')[0];

    if (svg.childElementCount > maxElements) {
        var maxDeleteIndex = svg.childElementCount - maxElements;
        var children = svg.children;

        for (var i = 0; i < maxDeleteIndex; i++) {
            svg.removeChild(children[0]);
        }
    }
}


function footprints() {

}


function bundle() {

}


function makeCircle(radius, x, y) {
    var circle = svgContainer.append('circle')
        .attr('cy', y)
        .attr('cx', x)
        .attr('r', radius);

    return circle;
}

function makeCircleWithVanish(radius, x, y) {
    var fill = chooseRandomColor();
    var circle = makeCircle(radius, x, y);
    circle.attr('fill', fill);

    var randomTimeout = getRandomInt(1, 1500);
    setTimeout(function() {
        circle.attr('class', 'magictime vanishOut');
    }, randomTimeout);
}

function circleGrid() {
    var numCircles = 6;
    var radius = chooseRandomSizeMultiple();

    var offset = radius * numCircles * -1;
    var x = chooseRandomDim(svgWidth, offset);
    var y = chooseRandomDim(svgHeight, offset);
    var originalY = y;

    for (var i = 0; i < numCircles; i++) {
        y = originalY;

        for (var j = 0; j < numCircles; j++) {
            makeCircleWithVanish(radius, x, y);
            y += (radius*2) + 2;
        }

        x += (radius*2) + 2;
    }
}


function chord() {

}


function generateHexData(radius, x, y) {
    var h = (Math.sqrt(3)/2)

    return [
        { 'x':  radius/2+x, 'y': -radius*h+y},
        { 'x':  radius+x,   'y': y},
        { 'x':  radius/2+x, 'y': radius*h+y},
        { 'x': -radius/2+x, 'y': radius*h+y},
        { 'x': -radius+x,   'y': y},
        { 'x': -radius/2+x, 'y': -radius*h+y},
    ];
}

function addParticles(radius, x, y, size, fill) {
    var radiusData = generateHexData(radius, x, y);

    for (var i = 0; i < radiusData.length; i++) {
        var thisX = radiusData[i]['x'];
        var thisY = radiusData[i]['y'];

        var circle = makeCircle(size, thisX, thisY).attr('fill', fill);

        if (i < 3) {
            circle.attr('class', 'magictime openDownRightOut');
        } else {
            circle.attr('class', 'magictime openDownLeftOut');
        }
    }
}

function explode() {
    var x = chooseRandomDim(svgWidth);
    var y = chooseRandomDim(svgHeight);
    var explosionRadius = chooseRandomSizeOne();
    var centerFill = chooseRandomColor();
    var particleSize = 30;
    var particleFill = chooseRandomColor();

    while (particleFill === centerFill) {
        particleFill = chooseRandomColor();
    }

    var center = makeCircle(particleSize, x, y).attr('fill', centerFill)
                                                 .attr('class', 'magictime vanishOut');

    addParticles(explosionRadius, x, y, particleSize, particleFill);
}


function force() {

}


function smile() {

}


function makeHexagon(radius, x, y, fill) {
    var hexagonData = generateHexData(radius, x, y);

    var drawHexagon = 
        d3.svg.line()
            .x(function(d) { return d.x; })
            .y(function(d) { return d.y; })
            .interpolate('cardinal-closed')
            .tension('1');

    var enterElements = svgContainer.append('path')
                                    .attr('d', drawHexagon(hexagonData))
                                    .attr('fill', fill)
                                    .attr('class', 'magictime puffOut');
}

function hexBurst() {
    for (var i = 0; i < 15; i++){
        var x = chooseRandomDim(svgWidth);
        var y = chooseRandomDim(svgHeight);
        var radius = chooseRandomSizeMultiple();
        var fill = chooseRandomColor();

        makeHexagon(radius, x, y, fill);
    }
}


function implode() {

}


function partition() {

}


function staffTwirl() {
    var strokeColor = chooseRandomColor();
    var x = chooseRandomDim(svgWidth);
    var x2 = chooseRandomDim(svgWidth);

    var y = chooseRandomDim(svgHeight);
    var y2 = chooseRandomDim(svgHeight);

    var rectangle = svgContainer.append('line')
                                .attr('x1', x)
                                .attr('y1', y)
                                .attr('x2', x2)
                                .attr('y2', y2)
                                .attr('stroke', strokeColor)
                                .attr('stroke-width', 10)
                                .attr('stroke-dasharray','20,5');

    setTimeout(function() {
        rectangle.attr('class', 'magictime foolishOut')
    }, 300);
}


function flash() {
    var flashColor = chooseRandomColor();

    $('body').css('background-color', flashColor);
    setTimeout(function() {
        updateBgColor(currentTheme);
    }, 400);
}


function wink() {

}


function drawStripe(i) {
    var y = 60 * i;
    var fill = chooseRandomColor();

    var rectangle = svgContainer.append('rect')
                         .attr('x', 0)
                         .attr('y', y)
                         .attr('width', '100%')
                         .attr('height', '60')
                         .attr('fill', fill)
                         .attr('class', 'magictime slideLeftRetourn');
    setTimeout(function() {
        rectangle.attr('class', 'magictime slideRight')
    }, 500);
}

function stripes() {
    var numStripes = Math.floor(svgHeight/60);

    for (var i = 0; i <= numStripes; i++) {
        if (i % 2 == 0) {
            drawStripe(i);
        }
    }
}


function drawOverlappingCircles(x, y) {
    var radius = Math.min(x, y) * .8;
    var colors = getThemeColors(currentTheme);
    var bgColor = getThemeBg(currentTheme)
    var radiusDecrement = radius / (colors.length + 2);

    for (var i = 0; i < colors.length; i++) {
        var circle = makeCircle(radius, x, y);
        circle.attr('fill', colors[i])
              .attr('class', 'rainbow');
        radius -= radiusDecrement;
    }

    var centerCircle = makeCircle(radius, x, y);
    centerCircle.attr('fill', bgColor)
                .attr('class', 'rainbow');
}

function drawRainbowRect(x, y, height) {
    var fill = getThemeBg(currentTheme);

    var rectangle = svgContainer.append('rect')
                         .attr('x', x)
                         .attr('y', y)
                         .attr('width', '100%')
                         .attr('height', height)
                         .attr('fill', fill)
                         .attr('class', 'rainbow');

    return rectangle;
}

function rainbow() {
    var x = svgWidth/2;
    var y = (4/5) * svgHeight;
    var height = (svgHeight/2) + 1;

    drawOverlappingCircles(x, y);


    var bottom = drawRainbowRect(0, y, height);
    var top = drawRainbowRect(0, 0, y);
    top.attr('class', 'rainbow magictime rainbowAnimate');

    setTimeout(function () {
        d3.selectAll(".rainbow").remove();
    }, 1000);
}


function pack() {
    var data = makeData(8, 0);

    var nodes = d3.layout.pack()
      .value(function(d) { return d.size;})
      .size([svgWidth, svgHeight])
      .nodes(data);

    nodes.shift();

    var chart = svgContainer.selectAll('circles')
                            .data(nodes)
                        .enter().append('svg:circle')
                            .attr('cx', function(d) { return d.x; })
                            .attr('cy', function(d) { return d.y; })
                            .attr('r', function(d) { return d.r; })
                            .attr('fill', function(d) { return d.name; })
                            .attr('stroke', 'grey');

    setTimeout(function() {
        chart.attr('class', 'magictime packAnimate');
    }, 100);
}


function suckedIn() {
    var x = svgWidth/2;
    var y = svgHeight/2;
    var radius = chooseRandomSizeOne();
    var strokeColor = chooseRandomColor();

    var circle = makeCircle(radius, x, y);
    circle.attr('fill', 'transparent')
          .attr('stroke', strokeColor)
          .attr('stroke-width', 10)
          .attr('stroke-dasharray','20,5')
          .attr('class', 'magictime spaceOutUp');
}

function raindrop() {

}


function stipple() {

}


function takeOff() {
    var x = chooseRandomDim(svgWidth);
    var y = chooseRandomDim(svgHeight);
    var radius = chooseRandomSizeOne();
    var fill = chooseRandomColor();

    var circle = makeCircle(radius, x, y);
    circle.attr('fill', fill);

    setTimeout(function() {
        circle.attr('class', 'magictime tinRightOut');
    }, 1000);
}


function makeMoreChildren(maxDepth, currentDepth) {
    var random = getRandomInt(0, 5);
    var children = [];
    currentDepth++;

    for (var i = 0; i < random; i++) {
        var shouldMakeChild = getRandomInt(0, 2);

        if (shouldMakeChild === 1) {
            var child = makeData(maxDepth, currentDepth);

            if (child) {
                children.push(child);
            }
        }
    }

    currentDepth--;
    return children;
}

function makeData(maxDepth, currentDepth) {
    var data = {'name': chooseRandomColor(),
                'size': getRandomInt(1, 1000)};

    if (currentDepth < maxDepth) {
        data.children = makeMoreChildren(maxDepth, currentDepth);
    }

    return data;
}

function tree() {
    var radius = 15;
    var treeData = makeData(6, 0);
    var chart = svgContainer.append('svg:g');

    var layout = d3.layout.tree().size([(svgHeight-(radius*2)),(svgWidth-(radius*2))]);

    var diagonal = d3.svg.diagonal()
        .projection(function(d) { return [d.y, d.x]; });

    var nodes = layout.nodes(treeData);
    var links = layout.links(nodes);

    var link = chart.selectAll('pathlink')
                    .data(links)
                    .enter().append('svg:path')
                    .attr('class', 'link')
                    .attr('d', diagonal);

    var node = chart.selectAll('g.node')
                    .data(nodes)
                    .enter().append('svg:g')
                    .attr('transform', function(d) { return 'translate(' + d.y + ',' + d.x + ')'; })
                    .attr('fill', function(d) { return d.name; });

    node.append('svg:circle')
        .attr('r', radius);

    setTimeout(function() {
        chart.attr('class', 'magictime puffOut');
    }, 1000);

}


function treemap() {

}


function wiggle() {

}


function stack() {

}


function pie(){

}


function getLineData(x, y) {
    var lineData = [];
    var randomAmplitude = getRandomInt(10, 40);
    var length = Math.ceil(svgHeight/randomAmplitude);

    for (var i = 0; i < length; i++) {
        lineData.push({'x': x, 'y': y});
        y += randomAmplitude;

        if (i % 2 == 0) {
            x += randomAmplitude;
        } else{
            x -= randomAmplitude;
        }
    }

    return lineData;
}

function drawZigzag() {
    var x = chooseRandomDim(svgWidth);
    var y = chooseRandomDim(svgHeight);
    var strokeColor = chooseRandomColor();

    var lineData = getLineData(x, y);

    var lineFunction = d3.svg.line()
                             .x(function(d) { return d.x; })
                             .y(function(d) { return d.y; })
                             .interpolate('linear');

    var lineGraph = svgContainer.append('path')
                                .attr('d', lineFunction(lineData))
                                .attr('stroke', strokeColor)
                                .attr('stroke-width', 15)
                                .attr('fill', 'transparent');

    return lineGraph;
}

function animateZigZag(zigzag) {
    zigzag.attr('class', 'magictime slideDownRetourn');

    setTimeout(function() {
        zigzag.attr('class', 'magictime slideUp');
    }, 250);

    setTimeout(function() {
        zigzag.attr('stroke', 'transparent');
    }, 1300);
}

function zigzag() {
    var zigzag = drawZigzag();
    animateZigZag(zigzag);
}

function resetSVGDims(evt){
    svgWidth = svgContainer[0][0]['clientWidth'];
    svgHeight = svgContainer[0][0]['clientHeight'];
}

$(window).resize(resetSVGDims);