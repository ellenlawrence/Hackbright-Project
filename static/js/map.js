window.markerArray = [];

function initMap() {

  // Create a map and center it on San Francisco.
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

      // Instantiate a directions service.
      const directionsService = new google.maps.DirectionsService;

      // Create a renderer for directions and bind it to the map.
      const directionsDisplay = new google.maps.DirectionsRenderer({map: map});

      // Instantiate an info window to hold step text.
      const stepDisplay = new google.maps.InfoWindow;

      $('#submit').on('click', () => {
        calculateAndDisplayRoute(directionsDisplay,
                                 directionsService,
                                 stepDisplay,
                                 map,
                                 pos);
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



// }

// function initRoute(pos, map) {
//   // Initializes the route.

//   // Instantiate a directions service.
//   const directionsService = new google.maps.DirectionsService;

//   // Create a renderer for directions and bind it to the map.
//   const directionsDisplay = new google.maps.DirectionsRenderer({map: map});

//   // Instantiate an info window to hold step text.
//   const stepDisplay = new google.maps.InfoWindow;

//   const markerArray = [];

//   // Display the route between the initial start and end selections.
//   calculateAndDisplayRoute(
//       directionsDisplay, directionsService, markerArray, stepDisplay, map, pos);
//   // Listen to change events from the start and end lists.
//   // const onChangeHandler = function() {
//   //   calculateAndDisplayRoute(
//   //       directionsDisplay, directionsService, markerArray, stepDisplay, map, pos);
//   // };
//   // // recalculate and display new route when user checks different destinations
//   // // and hits 'route' again
//   // document.getElementById('destination').addEventListener('change', onChangeHandler);
// }
  

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}

function calculateAndDisplayRoute(
  directionsDisplay, 
  directionsService,
  stepDisplay, 
  map, 
  pos
  ) {
  // First, remove any existing markers from the map.
  for (let i = 0; i < window.markerArray.length; i++) {
    window.markerArray[i].setMap(null);
  }

  window.markerArray = [];
  
  const mode = $('select#mode option:checked').val();

  const selectedDestinations = [];
  $.each($(':checkbox[name=destination]:checked'), function(){
    let address = $(this).val();
    let name = $(this).data('name');
    selectedDestinations.push({address: address,
            name: name});
  });

  const waypts = [];
  
  for (let i = 0; i < selectedDestinations.length; i++) {
    waypts.push({
        location: selectedDestinations[i].address,
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
      showSteps(response, stepDisplay, map, selectedDestinations);
    } else {
      console.log('failed');
      window.alert('Directions request failed due to ' + status);
    }
  });
}

function showSteps(directionResult, stepDisplay, map, selectedDestinations, pos) {
  // For each step, place a marker, and add the text to the marker's infowindow.
  // Also attach the marker to an array so we can keep track of it and remove it
  // when calculating new routes.
  
  const myRoute = directionResult.routes[0];
  const directionsPanel = document.getElementById('directions-panel');
  const upperLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
  'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

  directionsPanel.style.display = '';
  directionsPanel.innerHTML = '';

  const options = {
    tokenize: true,
    keys: [{
      name: 'address',
    }]
  };

  const fuse = new Fuse(selectedDestinations, options);
  
  for (let i = 0; i < myRoute.legs.length; i++) {
    let leg = myRoute.legs[i];

    const searchResult = fuse.search(leg.end_address);
    
    directionsPanel.innerHTML += '<b>Route Segment: ' + upperLetters[i] + ' to ' +
    upperLetters[i + 1] + '</b><br>';
    
    if (i != (myRoute.legs.length - 1)) {
      directionsPanel.innerHTML += '<b>Destination: ' + searchResult[0].name +
              '</b><br>';
    }    
    else {
      directionsPanel.innerHTML += '<b>Destination: ' + leg.end_address +
              '</b><br>';
    }

    directionsPanel.innerHTML += '<b>Distance: ' + leg.distance.text +
            '</b><br>'; 
    directionsPanel.innerHTML += '<b>Duration: ' + leg.duration.text +
            '</b><br>'; 
    directionsPanel.innerHTML += '<ol id="numbered-' + i + '-list"></ol>'
    let numberedList = document.getElementById('numbered-' + i + '-list');

    for (let i = 0; i < leg.steps.length; i++) {
      const marker = new google.maps.Marker();
      window.markerArray.push(marker);
      marker.setMap(map);
      marker.setPosition(leg.steps[i].start_location);
      attachInstructionText(stepDisplay, 
                            marker, 
                            leg.steps[i].instructions, 
                            map);
      numberedList.innerHTML += '<li>' + leg.steps[i].instructions + '</li><br>';
    }
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







