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
  minTime = parseInt($( "#minTime" ).val(), 10);
  maxTime = parseInt($( "#maxTime" ).val(), 10);
  $( "#timerange-slider" ).slider({
    range: true,
    min: minTime,
    max: maxTime,
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
  var maxes = $( "#maxSliders" ).val().split(' ');
  $( "#slider > span" ).each(function(i) {
    // read initial values from markup and remove that
    var value = parseInt( $( this ).text(), 10 );
    $( this ).empty().slider({
      value: value,
      orientation: "horizontal",
      min: 1,
      max: parseInt(maxes[i], 10),
      animate: true,
      step: 1,
      slide: function( event, ui ) {
        $($( "#slider > input" ).get(i)).val( ui.value );
      }
    });
  });
}

function createToolbox() {
  createTimeSlider();
  createGraphSlider();
  updateParams();
}
