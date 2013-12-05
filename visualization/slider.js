// Each time parameters are updated, call this function
// to update the displayed parameters
function updateParams() {
  $( "#slider > input" ).each(function(i, val) {
    // read initial values from markup and remove that
    $( this ).val($($( "#slider > span" ).get(i)).slider("value"))
  })
}

// Sets up time window sliders
function createTimeSlider() {
  $( "#timerange-slider" ).slider({
    range: true,
    min: userMinTime,
    max: userMaxTime,
    values: [ minTime, maxTime ],
    slide: function( event, ui ) {
      $( "#timerange" ).val(ui.values[ 0 ] + " - " + ui.values[ 1 ]);
    }
  });
  $( "#timerange" ).val($( "#timerange-slider" ).slider( "values", 0 ) +
    " - " + $( "#timerange-slider" ).slider( "values", 1 ) );
}

// Sets up num nodes / messages sliders
function createGraphSlider() {
  $( "#slider > span" ).each(function(i) {
    $( this ).empty().slider({
      value: maxSliders[i],
      orientation: "horizontal",
      min: 1,
      max: userSliders[i],
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
  createTimeSlider();
  createGraphSlider();
  updateParams();
}
