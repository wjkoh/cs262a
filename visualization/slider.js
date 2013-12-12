// Each time parameters are updated, call this function
// to update the displayed parameters
function updateParams() {
  $( "#slider > input" ).each(function(i, val) {
    // read initial values from markup and remove that
    $( this ).val($($( "#slider > span" ).get(i)).slider("value"))
  })
}

// Sets up time window sliders
function updateSliderText() {
      userMinTime = $( "#timerange-slider" ).slider( "values", 0 );
      userMaxTime = $( "#timerange-slider" ).slider( "values", 1 );
      var minVal = new Date(userMinTime*1000).toLocaleTimeString();
      var maxVal = new Date(userMaxTime*1000).toLocaleTimeString();
      $( "#timerange" ).text(minVal + " - " + maxVal );
}

function createTimeSlider() {
  $( "#timerange-slider" ).slider({
    range: true,
    min: minTime,
    max: maxTime,
    step: 60,
    values: [ userMinTime, userMaxTime ],
    slide: function(event,ui) {updateSliderText() }
  });
}

// Sets up num nodes / messages sliders
function createGraphSlider() {
  $( "#slider > span" ).each(function(i) {
    $( this ).empty().slider({
      value: userSliders[i],
      orientation: "horizontal",
      min: 1,
      max: maxSliders[i],
      animate: true,
      step: 1,
      slide: function( event, ui ) {
        $($( "#slider > input" ).get(i)).val( ui.value );
        userSliders[i] = ui.value;
      }
    });
  });
}

function createToolbox() {
    $("#slider").empty().html(" \
              <br/><br/><br/> \
              <label>Number of Nodes:</label> \
              <input type=\"text\" class=\"configtext\" readonly> \
              <br/><span>10</span> \
 \
              <br /> <br /> <br /> \
              <label>Number of Messages:</label> \
              <input type=\"text\" class=\"configtext\" readonly> \
              <br/><span>15</span>");

    createTimeSlider();
    createGraphSlider();
    updateParams();
}
