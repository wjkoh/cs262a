var data;

// For default arguments, pass in -1
function getData(minTime, maxTime, numNodes, numMessages) {
    // $.get('http://localhost:8000/data.js', function(contents) { data = contents; })
    // jQuery.ajax({
    //        url: "csvToJs.py",
    //        success: function (output) {
    //            data = output;
    //            console.log(output)
    //            updateFrame(data);
    //        }
    // });

    d3.text("currData.js", function(error, contents) {
        if(error) return console.warn(error);
        data = eval(contents);
        updateFrame(data);
    });
}

function initializeFrame() {
    maxSliders[0] = 1;
    maxSliders[1] = 1;

    userSliders[0] = 1;
    userSliders[1] = 1;

    userMinTime = 0;
    userMaxTime = 0;

    getData();
}

function updateFrame(allData) {
    var numNodes = allData.length;
    var numMessages = allData[0].length;

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
            
            var x = d3.time.scale()
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
    createToolbox();
}
