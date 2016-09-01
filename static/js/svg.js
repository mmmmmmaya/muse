'use strict';

var svgContainer = d3.select('svg');
var bottomSVGLayer = svgContainer.append('g');
var topSVGLayer = svgContainer.append('g');

var svgHeight;
var svgWidth;

resetSVGDims();

function resetSVGDims(evt) {
    svgWidth = svgContainer[0][0]['clientWidth'];
    svgHeight = svgContainer[0][0]['clientHeight'];
}

$(window).resize(resetSVGDims);
