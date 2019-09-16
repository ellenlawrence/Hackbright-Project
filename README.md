# DayMap

## Summary

**DayMap** is a vacation day-planning site that allows users to search for and select sights they would like to visit in various cities across the U.S., and then creates and displays the most efficient route from the user’s location passing through each sight and ending back at the user's original location. This lets users figure out the order in which they should visit each sight they had planned for a day on vacation, and also provides them with step by step directions for each leg of their customized route.


## About the Developer

DayMap was created by Ellen Lawrence. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/ellen-lawrence-1a9837a9/).


## Technologies

**Tech Stack:**

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Jinja2
- JavaScript
- jQuery
- Fuse.js
- JSON
- AJAX
- HTML
- CSS
- Bootstrap
- Python unittest module
- Google Maps Directions API
- Google Maps JavaScript API

DayMap is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM. The front end templating uses Jinja2, the HTML was built using mainly CSS with a little Bootstrap, and the JavaScript uses jQuery and AJAX to interact with the backend. The map is built using the Google Maps Directions API and displayed using the Google Maps JavaScript API. Server routes are tested using the Python unittest module.


## Features

![alt text](https://github.com/ellenlawrence/DayMap/blob/master/static/images/signup-page.png "DayMap Signup")

The signup and login pages both feature a video of the Golden Gate Bridge as the background. The password field
includes a toggle button that allows the user to either view or hide their password. There is also a *very* 
important Terms of Service that must be viewed and agreed to before a user account can be created.


![alt text](https://github.com/ellenlawrence/DayMap/blob/master/static/images/prof-page.png "DayMap Profile Page")

The user profile includes a profile picture that, when hovered over by the mouse, displays a modal that can be
clicked on to update the user's profile picture. To the right of the profile picture and username are the user's
destinations they have already added to their Destination List, sorted by city and arranged by alphabetical order
within each city.


![alt text](https://github.com/ellenlawrence/DayMap/blob/master/static/images/dest-added.png "DayMap Destination Search and Addition")

When a user searches for a destination using the search bar in the upper right hand corner, a list of destinations 
matching their selected city and roughly matching their text input appear on the search results page. When a 
destination is selected and the "Add to Destination List" button is clicked, an alert is shown letting the user
know that their selection has been added to their Destination List.


![alt text](https://github.com/ellenlawrence/DayMap/blob/master/static/images/map-init.png "DayMap Map Init")

When the Map page initially loads, it geolocates the user and displays a window showing the user their current
location. On the right there is a destination list panel where the user can select the destinations they'd like
to route to and their mode of travel.


![alt text](https://github.com/ellenlawrence/DayMap/blob/master/static/images/route.png "DayMap Route")

The route is displayed when the user clicks "Route". A directions panel pops up after a route has been created, 
which contains the destination name, distance to destination, and time to destination for each route segment, along 
with numbered directions steps. Each red marker with a letter in it represents a destination and the end of one route 
segment, and each blue marker designates where a directions step is happening. Clicking on a blue marker will display 
a window containing the corresponding directions step. Clicking on a red marker will display the address of the 
destination.




















