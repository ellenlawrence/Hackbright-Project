window.markerArray = [];

function initMap() {
  // Create a map and center it on San Francisco.
  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 14,
    center: {lat: 37.7749, lng: -122.4194}
  });

  function addStyles(map) {
  const styles = [
    {
        "featureType": "administrative.land_parcel",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            },
            {
                "color": "#332727"
            }
        ]
    },
    {
        "featureType": "landscape.man_made",
        "elementType": "all",
        "stylers": [
            {
                "color": "#a5b7c2"
            },
            {
                "lightness": "78"
            }
        ]
    },
    {
        "featureType": "landscape.natural",
        "elementType": "all",
        "stylers": [
            {
                "color": "#64b590"
            },
            {
                "visibility": "on"
            },
            {
                "lightness": "81"
            }
        ]
    },
    {
        "featureType": "poi.attraction",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "simplified"
            },
            {
                "color": "#8989cc"
            }
        ]
    },
    {
        "featureType": "poi.attraction",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#8990cc"
            },
            {
                "lightness": "70"
            }
        ]
    },
    {
        "featureType": "poi.attraction",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "visibility": "simplified"
            },
            {
                "hue": "#0900ff"
            }
        ]
    },
    {
        "featureType": "poi.attraction",
        "elementType": "labels",
        "stylers": [
            {
                "color": "#8990cc"
            }
        ]
    },
    {
        "featureType": "poi.business",
        "elementType": "all",
        "stylers": [
            {
                "color": "#8989cc"
            },
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "poi.government",
        "elementType": "all",
        "stylers": [
            {
                "color": "#cc9f6b"
            },
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "poi.medical",
        "elementType": "all",
        "stylers": [
            {
                "color": "#b86b6b"
            },
            {
                "visibility": "simplified"
            },
            {
                "lightness": "61"
            }
        ]
    },
    {
        "featureType": "poi.medical",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#ca9191"
            },
            {
                "lightness": "68"
            }
        ]
    },
    {
        "featureType": "poi.medical",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "##000000"
            }
        ]
    },
    {
        "featureType": "poi.medical",
        "elementType": "labels.text",
        "stylers": [
            {
                "color": "#ca9191"
            },
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "poi.park",
        "elementType": "all",
        "stylers": [
            {
                "color": "#84c09b"
            },
            {
                "visibility": "simplified"
            },
            {
                "lightness": "54"
            }
        ]
    },
    {
        "featureType": "poi.park",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#84c09b"
            },
            {
                "lightness": "61"
            }
        ]
    },
    {
        "featureType": "poi.park",
        "elementType": "labels",
        "stylers": [
            {
                "color": "#84c09b"
            }
        ]
    },
    {
        "featureType": "poi.place_of_worship",
        "elementType": "all",
        "stylers": [
            {
                "color": "#8989cc"
            },
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "poi.school",
        "elementType": "all",
        "stylers": [
            {
                "color": "#8989cc"
            },
            {
                "visibility": "simplified"
            },
            {
                "lightness": "61"
            }
        ]
    },
    {
        "featureType": "poi.school",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#8986cc"
            },
            {
                "lightness": "70"
            }
        ]
    },
    {
        "featureType": "poi.school",
        "elementType": "labels",
        "stylers": [
            {
                "color": "#8986cc"
            }
        ]
    },
    {
        "featureType": "poi.sports_complex",
        "elementType": "all",
        "stylers": [
            {
                "color": "#8989cc"
            },
            {
                "lightness": "61"
            },
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "poi.sports_complex",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#8990cc"
            },
            {
                "lightness": "70"
            }
        ]
    },
    {
        "featureType": "poi.sports_complex",
        "elementType": "labels",
        "stylers": [
            {
                "color": "#8990cc"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "all",
        "stylers": [
            {
                "color": "#ffc894"
            },
            {
                "lightness": "27"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "all",
        "stylers": [
            {
                "color": "#394399"
            },
            {
                "lightness": "84"
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "all",
        "stylers": [
            {
                "color": "#ffffff"
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "all",
        "stylers": [
            {
                "color": "#c5eaff"
            },
            {
                "lightness": "15"
            }
        ]
    }];

  const customMapType = new google.maps.StyledMapType(
    styles,
    { name: 'Custom Style' }
  );

  map.mapTypes.set('map_style', customMapType);
  map.setMapTypeId('map_style');
  }

  addStyles(map);

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

      $('#route-submit').on('click', () => {
        console.log('clickhandler');
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

  if (waypts.length === 0) {
    alert('You must select at least one item from your Destination List in order to create a route.')
  } else {
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
  // const markerImage = '/static/images/marker_img.svg'
  
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







