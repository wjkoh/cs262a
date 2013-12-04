// Each time parameters are updated, call this function
function updateParams() {
  // $( "#nodetext" ).val( "$" + $( "#timerange-slider" ).slider( "values", 0 ));
  $( "#slider > input" ).each(function(i, val) {
    // read initial values from markup and remove that
    $( this ).val($($( "#slider > span" ).get(i)).slider("value"))
  })
}

$(function() {
  $( "#timerange-slider" ).slider({
    range: true,
    min: 0,
    max: 500,
    values: [ 75, 300 ],
    slide: function( event, ui ) {
      $( "#timerange" ).val(ui.values[ 0 ] + " - " + ui.values[ 1 ] );
    }
  });
  $( "#timerange" ).val($( "#timerange-slider" ).slider( "values", 0 ) +
    " - " + $( "#timerange-slider" ).slider( "values", 1 ) );
});

$(function() {
  $( "#slider > span" ).each(function() {
    // read initial values from markup and remove that
    var value = parseInt( $( this ).text(), 10 );
    $( this ).empty().slider({
      value: value,
      orientation: "horizontal",
      min: 1,
      max: 20,
      range: "min",
      animate: true,
      step: 1,
      slide: updateParams
    });
  });
  updateParams();
});
