var data;

// For default arguments, pass in -1
function getData() {
    args = [userSliders[0], userMinTime, userMaxTime, grepCommand];
    $("#statustext").html("Loading new data...")

    jQuery.ajax({
           url: "./csvToJs.py",
           type: "POST",
           data: JSON.stringify(args),
           datatype:"text",
           success: function (output) {
               data = eval(output);
               updateFrame(data);
               $("#statustext").html("")
           }
    });

    // d3.text("currData.js", function(error, contents) {
    //     if(error) return console.warn(error);
    //     data = eval(contents);
    //     updateFrame(data);
    // });
}

function initializeFrame() {
    maxSliders[0] = 1;
    maxSliders[1] = 10;

    userSliders[0] = 1;
    userSliders[1] = 2;

    userMinTime = 1;
    userMaxTime = 10;

    grepCommand = $("#greptext").val()

    getData();
}

function updateFrame(allData) {
    var numNodes = allData.length;
    var numMessages = allData[0].length;

    maxTime = d3.max(allData, function(d) {
                       return d3.max(d, function(d) {
                       return d3.max(d, function(d) {
                           return d.timestamp*1000; }) }) });
    minTime = d3.min(allData, function(d) {
                       return d3.min(d, function(d) {
                       return d3.min(d, function(d) {
                           return d.timestamp*1000; }) }) });

    maxSliders[0] = numNodes;
    maxSliders[1] = numMessages;

    grepCommand = $("#greptext").val()

    d3.selectAll('.charts').text('');
    for(var node_i = 0; node_i < userSliders[0]; ++node_i) {
        var currRowName = 'chart_' + node_i.toString()
        var currRowDiv = d3.selectAll('.charts')
                         .append('div')
                         .attr('class', currRowName)
                         .style('.margin', '0 auto')
                         .style('white-space', 'nowrap')
                         .style('overflow-x', 'scroll')
                         .style('overflow-y', 'hidden')

        for(var msg_i = 0; msg_i < userSliders[1]; ++msg_i) {
            var data = allData[node_i][msg_i];

            var margin = {top: 20, right: 25, bottom: 60, left: 60}
              , width = 500 - margin.left - margin.right
              , height = 250 - margin.top - margin.bottom;
            
            var x = d3.time.scale()
                      .domain([minTime, maxTime])
                      .range([ 0, width ]);
            
            var y = d3.scale.linear()
                      .domain([0, d3.max(data, function(d) { return d.value; })])
                      .range([ height, 0 ]);

            var chart = currRowDiv
            .append('div')
            .attr('class', 'main')
            .append('svg:svg')
            .attr('width', width + margin.right + margin.left)
            .attr('height', height + margin.top + margin.bottom)
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
                  .attr("cx", function (d,i) { return x(d.timestamp*1000); } )
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

        // Sort log by timestamp
        var allNodeMessages = []
        allNodeMessages = allNodeMessages.concat.apply(allNodeMessages, allData[node_i]);
        allNodeMessages.sort(function(a, b) {
            return (a.timestamp > b.timestamp) ? 1 : -1;
        })

        // Print the raw log messages
        var currLogDiv = currRowDiv
            .append("div")
            .style("border", "none")
            .style("display", "inline-block")
            .style("height", height + margin.top + margin.bottom)
            .style("overflow", "auto")
            .selectAll("p")
            .data(allNodeMessages)
            .enter()
            .append("p")
            .attr('class', 'logtext')
            .html(function(d) {
                return new Date(d.timestamp*1000).toLocaleTimeString() +
                       ": " + d.message +
                       "<br/>";
            })
    }

    // Recreate each time because time slider changes
    createToolbox();
}
