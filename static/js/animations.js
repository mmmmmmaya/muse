'use strict';

var letterAnimationMap = {
    'a': function() {footprints();},
    'b': function() {spiral();},
    'c': function() {circleGrid();},
    'd': function() {piano();},
    'e': function() {explode();},
    'f': function() {force();},
    'g': function() {speedy();},
    'h': function() {hexBurst();},
    'i': function() {implode();},
    'j': function() {verticalChecker();},
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
    'v': function() {flashingLights();},
    'w': function() {wiggle();},
    'x': function() {starburst();},
    'y': function() {splatter();},
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


function spiral() {
    var x = chooseRandomDim(svgWidth);
    var y = chooseRandomDim(svgHeight);
    var radius = chooseRandomSizeMultiple();
    var fill = chooseRandomColor();

    var circle = makeCircle(radius, x, y)
                .attr('class', 'magictime spiralIn')
                .attr('fill', fill);
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


function drawMajorKeys(x, y, numKeys, pianoKeyWidth,
                        spaceBetweenKeys, pianoHeight) {
    var x = x;
    var keyColor = chooseRandomColor();
    var keys = [];

    for (var i = 0; i < numKeys; i++) {
        var rectangle = svgContainer.append('rect')
                         .attr('x', x)
                         .attr('y', y)
                         .attr('width', pianoKeyWidth)
                         .attr('height', pianoHeight)
                         .attr('fill', keyColor)
                         .attr('class', 'piano');
        keys.push(rectangle);
        x += (pianoKeyWidth + spaceBetweenKeys);
    }

    return keys;
}

function drawMinorKeys(x, y, numKeys, pianoKeyWidth,
                        spaceBetweenKeys, pianoHeight, majorKeyColor) {
    var minorKeyWidth = (2/3)*pianoKeyWidth;
    var x = x + minorKeyWidth;
    var keyColor = ensureDifferentColor(majorKeyColor);
    var strokeFill = getThemeBg(currentTheme);

    for (var i = 0; i < numKeys-1; i++) {
        if (i !== 2) {
            var rectangle = svgContainer.append('rect')
                             .attr('x', x)
                             .attr('y', y)
                             .attr('width', minorKeyWidth)
                             .attr('height', pianoHeight/2)
                             .attr('fill', keyColor)
                             .attr('stroke', strokeFill)
                             .attr('stroke-width', spaceBetweenKeys)
                             .attr('class', 'piano');
        }

        x += (pianoKeyWidth + spaceBetweenKeys);
    }
}

function d3Delete(className, time) {
    setTimeout(function () {
        var selector = "." + className;
        d3.selectAll(selector).remove();
    }, time);
}

function animatePiano(keyColor) {

    setInterval(function(){

    }, 500);

    var keys = d3.selectAll('.piano')[0];
    var activeFill = ensureDifferentColor(keyColor);
    var timePressed = 200;
    var timeToNextKey = 100;
    var timer = timeToNextKey;

    for (var i = 0; i < keys.length; i++) {
        var originalColor;
        console.log(keys[i]);
        setTimeout(function() {
            console.log(keys[i]);
            originalColor = keys[i].attr('fill');
            keys[i].attr('fill', activeFill);
        }, timer);

        timer += timePressed;

        setTimeout(function() {
            keys[i].attr('fill', originalColor);
        }, timer);

        timer += timeToNextKey;
    }

}

function piano() {
    var numKeys = 7;
    var pianoKeyWidth = (svgWidth * (2/3))/numKeys;
    var spaceBetweenKeys = 5;
    var totalPianoWidth = (numKeys * pianoKeyWidth)
                        + ((numKeys - 1) * spaceBetweenKeys);
    var pianoHeight = (2/3) * svgHeight;

    var x = (svgWidth - totalPianoWidth) / 2;
    var y = (svgHeight - pianoHeight) / 2;

    var majorKeys = drawMajorKeys(x, y, numKeys, pianoKeyWidth,
                                        spaceBetweenKeys, pianoHeight);
    var majorKeyColor = d3.select('.piano').attr('fill');
    drawMinorKeys(x, y, numKeys, pianoKeyWidth,
                    spaceBetweenKeys, pianoHeight, majorKeyColor);

    // TODO finish animate
    // animatePiano(majorKeyColor);
    d3Delete('piano', 3000);
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

function ensureDifferentColor(color) {
    var secondColor = chooseRandomColor();

    while (color === secondColor) {
        secondColor = chooseRandomColor();
    }

    return secondColor;
}

function explode() {
    var x = chooseRandomDim(svgWidth);
    var y = chooseRandomDim(svgHeight);
    var explosionRadius = chooseRandomSizeOne();
    var centerFill = chooseRandomColor();
    var particleSize = 30;
    var particleFill = ensureDifferentColor(centerFill);

    var center = makeCircle(particleSize, x, y).attr('fill', centerFill)
                                                 .attr('class', 'magictime vanishOut');

    addParticles(explosionRadius, x, y, particleSize, particleFill);
}

// gives the force its bounciness
function bounce(link, node) {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
}

// Returns a list of all nodes under the root.
function flatten(root) {
    var nodes = []
    var i = 0;

    function recurse(node) {
        if (node.children) {
            node.children.forEach(recurse);
        }

        if (!node.id) {
            node.id = ++i;
            nodes.push(node);
        }
    }

    recurse(root);
    return nodes;
}

function makeForce() {
    var link = svgContainer.selectAll(".link");
    var node = svgContainer.selectAll(".node");

    var root = makeData(9,0);
    var nodes = flatten(root);
    var links = d3.layout.tree().links(nodes);

    var force = d3.layout.force()
                         .size([svgWidth, svgHeight])
                         .friction(0.1)
                         .charge(-500)
                         .gravity(0)
                         .on("tick", function(){ bounce(link, node); })
                         .nodes(nodes)
                         .links(links)
                         .start();

    // Update the links…
    link = link.data(links, function(d) { return d.target.id; });

    // Exit any old links.
    link.exit().remove();

    // Enter any new links.
    link.enter().insert("line", ".node")
        .attr("class", "link")
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

      // Update the nodes…
      node = node.data(nodes, function(d) { return d.id; }).style("fill", function(d) { return d.name; });

      // Exit any old nodes.
      node.exit().remove();

      // Enter any new nodes.
      node.enter().append("circle")
          .attr("class", "node")
          .attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y; })
          .attr("r", function(d) { return Math.sqrt(d.size) / 10 || 4.5; })
          .style("fill", function(d) { return d.name; })
          .call(force.drag);

    return [links, nodes];
}


function force() {
    makeForce();

    setTimeout(function() {
        var links = svgContainer.selectAll(".link")
                                .attr('class', 'magictime bombOutLeft');
        var nodes = svgContainer.selectAll(".node")
                                .attr('class', 'magictime puffOut');
    }, 500);
}

function splatter() {
    makeForce();

    var links = svgContainer.selectAll(".link");
    var nodes = svgContainer.selectAll(".node");

    links.attr('class', 'magictime shrinkToCenter');
    nodes.attr('class', 'magictime shrinkToCenter');
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


function drawChecker(i) {
    var x = 20 * i;
    var fill = chooseRandomColor();

    var rectangle = svgContainer.append('rect')
                         .attr('x', x)
                         .attr('y', 0)
                         .attr('width', '20')
                         .attr('height', '20')
                         .attr('fill', fill)
                         .attr('class', 'magictime slideToBottom');
}

function ceilingDraw(func) {
    var num = Math.floor(svgWidth/20);

    for (var i = 0; i <= num; i++) {
        if (i % 2 == 0) {
            func(i);
        }
    }
}

function verticalChecker() {
    ceilingDraw(drawChecker);
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

    d3Delete('rainbow', 1000);
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
        chart.attr('class', 'magictime shrinkToCenter');
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
    // TODO prevent 1 level return
    var data = {'name': chooseRandomColor(),
                'size': getRandomInt(1, 10000)};

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


function drawLights(i) {
    var radius = 20;
    var x = radius * (i+1);
    var fill = chooseRandomColor();

    var light = makeCircle(radius/2, x, 0)
                    .attr('fill', fill)
                    .attr('class', 'lights');

    d3Delete('lights', 2500);

}

function flashingLights() {
    var flashLength = 5;

    for (var i = 0; i < flashLength; i++) {
        var timer = 500 * i;

        setTimeout(function() {
            ceilingDraw(drawLights);
        }, timer);
    }
}


function wiggle() {

}


function CalculateStarPoints(centerX, centerY, arms,
                                outerRadius, innerRadius) {
   var results = '';
   var pairs = []

   var angle = Math.PI / arms;

   for (var i = 0; i < 2 * arms; i++) {
        if (i % 2 == 0) {
            var r = outerRadius;
        } else {
            var r = innerRadius;
        }

      var currX = centerX + Math.cos(i * angle) * r;
      var currY = centerY + Math.sin(i * angle) * r;
      var pair = currX + "," + currY;

      pairs.push(pair);
      results = pairs.join(' ');
   }

   return results;
}

function starburst() {
    var fill = chooseRandomColor();
    var points = CalculateStarPoints(svgWidth/2, svgHeight/2, 5, 100, 50);
    var star = svgContainer.append('svg:polygon')
                           .attr('points', points)
                           .attr('fill', fill);
    star.attr('class', 'magictime zoomInToExit');
}


function speedy(){
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