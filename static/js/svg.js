'use strict';

var svgContainer = d3.select('svg');
var bottomSVGLayer = svgContainer.append('g');
var topSVGLayer = svgContainer.append('g');

var svgHeight;
var svgWidth;
var yOffset;

resetSVGDims();

function resetSVGDims(evt) {
    yOffset = $('#top-nav')[0]['clientHeight'];
    var bottomNavHeight = $('#bottom-nav')[0]['clientHeight'];

    svgWidth = svgContainer[0][0]['clientWidth'];
    svgHeight = svgContainer[0][0]['clientHeight'] - (bottomNavHeight);
}

$(window).resize(resetSVGDims);
