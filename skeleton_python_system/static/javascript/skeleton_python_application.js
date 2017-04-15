$(document).ready(function() {

  var elementSelector = '#view';
  var counter = 0;
  var model = { };

  draw(elementSelector, model);
});

function draw(selector, model) {

  var element = $(selector);
  var width = element.width();
  var height = element.height();
  var svg = d3.select(selector)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  g = svg.append('g').attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');


}
