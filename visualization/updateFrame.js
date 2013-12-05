// For default arguments, pass in -1
function getData(minTime, maxTime, numNodes, numMessages) {
    var data =
      [
        [
         [new Data(1, 0, 0, 'message 00'),
          new Data(1, 1, 1, 'message 00'),
          new Data(1, 5, 2, 'message 00'),
          new Data(5, 3, 0, 'message 01'),
          new Data(5, 5, 1, 'message 01'),
          new Data(5, 9, 2, 'message 01'),
          new Data(10, 11, 0, 'message 02'),
          new Data(10, 17, 1, 'message 02'),
          new Data(10, 22, 2, 'message 02'),
          new Data(15, 10, 0, 'message 03'),
          new Data(15, 19, 1, 'message 03'),
          new Data(15, 25, 2, 'message 03'),
         ],

         [new Data(1, 8,  0, 'm2 00'),
          new Data(5, 6,  0, 'm2 01'),
          new Data(10, 3, 0, 'm2 02'),
          new Data(19, 2, 0, 'm2 03'),
         ],

         [new Data(1, 8, 0 , 'm2 00'),
          new Data(5, 6, 0 , 'm2 01'),
          new Data(10, 3, 0, 'm2 02'),
          new Data(15, 2, 0, 'm2 03'),
         ],
        ],
        [
         [new Data(1, 2, 0, 'message 00'),
          new Data(1, 4, 1, 'message 00'),
          new Data(1, 7, 2, 'message 00'),
          new Data(5, 3, 0, 'message 01'),
          new Data(5, 6, 1, 'message 01'),
          new Data(5, 8, 2, 'message 01'),
          new Data(10, 8, 0, 'message 02'),
          new Data(10, 10, 1, 'message 02'),
          new Data(10, 12, 2, 'message 02'),
          new Data(15, 14, 0, 'message 03'),
          new Data(15, 17, 1, 'message 03'),
          new Data(15, 18, 2, 'message 03'),
         ],

         [new Data(1, 8, 0 , 'm2 00'),
          new Data(5, 6, 0 , 'm2 01'),
          new Data(10, 3, 0, 'm2 02'),
          new Data(15, 2, 0, 'm2 03'),
         ],

         [new Data(1, 8, 0 , 'm2 00'),
          new Data(5, 6, 0 , 'm2 01'),
          new Data(10, 3, 0, 'm2 02'),
          new Data(15, 2, 0, 'm2 03'),
         ],
        ],
      ];
    return data;
}

function initializeFrame() {
    var allData = getData(-1, -1, -1, -1);
    var numNodes = 2;
    var numMessages = 3;
    maxTime = d3.max(allData, function(d) {
                       return d3.max(d, function(d) {
                       return d3.max(d, function(d) {
                           return d.timestamp; }) }) });
    minTime = d3.min(allData, function(d) {
                       return d3.min(d, function(d) {
                       return d3.min(d, function(d) {
                           return d.timestamp; }) }) });

    maxSliders[0] = numNodes;
    maxSliders[1] = numMessages;

    // TODO these will not exist until after the current function completes!
    userSliders[0] = numNodes;
    userSliders[1] = numMessages;
    updateFrame();
    createToolbox();
}

function updateFrame() {
    // Synthetic data for now
    var allData = getData(userMinTime, userMaxTime, userSliders[0], userSliders[1]);
    var numNodes = 2;
    var numMessages = 3;
    maxTime = d3.max(allData, function(d) {
                       return d3.max(d, function(d) {
                       return d3.max(d, function(d) {
                           return d.timestamp; }) }) });
    minTime = d3.min(allData, function(d) {
                       return d3.min(d, function(d) {
                       return d3.min(d, function(d) {
                           return d.timestamp; }) }) });

    maxSliders[0] = numNodes;
    maxSliders[1] = numMessages;

    d3.selectAll('.charts').text('');
    for(var node_i = 0; node_i < userSliders[0]; ++node_i) {
        var currRowName = 'chart_' + node_i.toString()
        var currRowDiv = d3.selectAll('.charts')
                         .append('div')
                         .attr('class', currRowName)

        for(var msg_i = 0; msg_i < userSliders[1]; ++msg_i) {
            var data = allData[node_i][msg_i];

            var margin = {top: 20, right: 15, bottom: 60, left: 60}
              , width = 500 - margin.left - margin.right
              , height = 250 - margin.top - margin.bottom;
            
            var x = d3.scale.linear()
                      .domain([minTime, maxTime])
                      .range([ 0, width ]);
            
            var y = d3.scale.linear()
                      .domain([0, d3.max(data, function(d) { return d.value; })])
                      .range([ height, 0 ]);

            var chart = currRowDiv
            .append('svg:svg')
            .attr('width', width + margin.right + margin.left)
            .attr('height', height + margin.top + margin.bottom)
            .attr('float', 'left')
            .attr('class', 'chart' + node_i.toString() + "_" + msg_i.toString())

            var main = chart.append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
            .attr('width', width)
            .attr('height', height)
            .attr('fill', 'lightblue')
            .attr('class', 'main')   
                
            // draw the x axis
            var xAxis = d3.svg.axis()
            .scale(x)
            .tickPadding(5)
            .orient('bottom');

            main.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .attr('class', 'main axis date')
            .call(xAxis);

            // draw the y axis
            var yAxis = d3.svg.axis()
            .scale(y)
            .tickPadding(5)
            .ticks(5)
            .orient('left');

            main.append('g')
            .attr('transform', 'translate(0,0)')
            .attr('class', 'main axis date')
            .call(yAxis);

            var g = main.append("svg:g"); 
            
            g.selectAll("scatter-dots")
              .data(data)
              .enter().append("svg:circle")
                  .attr("cx", function (d,i) { return x(d.timestamp); } )
                  .attr("cy", function (d) { return y(d.value); } )
                  .attr("r", 8)
                  .style("fill", function (d,i) { return colors[d.index]; })
                  .append("svg:title")
                  .text(function(d) { return d.message; });

            $('svg circle').tipsy({ 
            gravity: 'w', 
            html: true, 
            title: function() { return this.__data__.message; }
            });
        }
    }

    // Recreate each time because time slider changes
}
