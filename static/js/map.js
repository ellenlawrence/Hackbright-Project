function initMap() {

  // Create a map and center it on Manhattan.
  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 17,
    center: {lat: 37.7749, lng: -122.4194}
  });

  const infoWindow = new google.maps.InfoWindow;

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      const pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      $('#submit').on('click', () => {
        initRoute(pos, map);
      });

      infoWindow.setPosition(pos);
      infoWindow.setContent('Your Location');
      infoWindow.open(map);
      map.setCenter(pos);
    }, function() {
      handleLocationError(true, infoWindow, map.getCenter());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
  }
}

// function getEnd(pos, map) {
//   // Choose the destination from the selected destinations that is closes to
//   // the user's current location.

//   const origin = pos;

//   const destinations = []; 
//   $(':checkbox[name=destination]:checked').each(function() { 
//     destinations.push($(this).next('label').text());
//   });

//   const mode = $('select#mode option:checked').val();

//   const service = new google.maps.DistanceMatrixService;

//   service.getDistanceMatrix({
//     origins: [origin],
//     destinations: destinations,
//     travelMode: mode,
//   }, function(response, status) {
//     if (status !== 'OK') {
//       alert('Error was: ' + status);
//     } else {



// }

function initRoute(pos, map) {
  // Initializes the route.

  // Instantiate a directions service.
  const directionsService = new google.maps.DirectionsService;

  // Create a renderer for directions and bind it to the map.
  const directionsDisplay = new google.maps.DirectionsRenderer({map: map});

  // Instantiate an info window to hold step text.
  const stepDisplay = new google.maps.InfoWindow;

  const markerArray = [];

  // Display the route between the initial start and end selections.
  calculateAndDisplayRoute(
      directionsDisplay, directionsService, markerArray, stepDisplay, map, pos);
  // Listen to change events from the start and end lists.
  // const onChangeHandler = function() {
  //   calculateAndDisplayRoute(
  //       directionsDisplay, directionsService, markerArray, stepDisplay, map, pos);
  // };
  // // recalculate and display new route when user checks different destinations
  // // and hits 'route' again
  // document.getElementById('destination').addEventListener('change', onChangeHandler);
}
  

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}

function calculateAndDisplayRoute(directionsDisplay, directionsService,
    markerArray, stepDisplay, map, pos) {
  // First, remove any existing markers from the map.
  for (let i = 0; i < markerArray.length; i++) {
    markerArray[i].setMap(null);
  }

  markerArray = []
  
  const mode = $('select#mode option:checked').val();
  
  const w = [];
  $.each($(':checkbox[name=destination]:checked'), function(){
    w.push($(this).val());
  });
  
  // const waypoints = [];
  // w.forEach(addWaypoint);
  // function addWaypoint(s) {
  //   const waypoint = {};
  //   waypoint[location] = s;
  //   waypoints.push(waypoint);
  // }
  // console.log(waypoints);

  const waypts = [];
  
  for (let i = 0; i < w.length; i++) {
    waypts.push({
        location: w[i],
        stopover: true
      });
  }

  directionsService.route({
    origin: pos,
    destination: pos,
    travelMode: mode,
    waypoints: waypts,
    optimizeWaypoints: true
  }, function(response, status) {
    // Route the directions and pass the response to a function to create
    // markers for each step.
    if (status === 'OK') {
      console.log('success');
      directionsDisplay.setDirections(response);
      showSteps(response, markerArray, stepDisplay, map);
    } else {
      console.log('failed');
      window.alert('Directions request failed due to ' + status);
    }
  });
}

function showSteps(directionResult, markerArray, stepDisplay, map) {
  // For each step, place a marker, and add the text to the marker's infowindow.
  // Also attach the marker to an array so we can keep track of it and remove it
  // when calculating new routes.
  const myRoute = directionResult.routes[0].legs[0];
  for (let i = 0; i < myRoute.steps.length; i++) {
    const marker = markerArray[i] = markerArray[i] || new google.maps.Marker;
    marker.setMap(map);
    marker.setPosition(myRoute.steps[i].start_location);
    attachInstructionText(
        stepDisplay, marker, myRoute.steps[i].instructions, map);
  }
}

function attachInstructionText(stepDisplay, marker, text, map) {
  google.maps.event.addListener(marker, 'click', function() {
    // Open an info window when the marker is clicked on, containing the text
    // of the step.
    stepDisplay.setContent(text);
    stepDisplay.open(map, marker);
  });
}







