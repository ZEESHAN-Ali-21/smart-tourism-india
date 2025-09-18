// Google Maps Integration for Smart Tourism India

let map;
let markers = [];
let infoWindow;

function initMap(lat = 20.5937, lng = 78.9629) {
    // Default to center of India
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 5,
        center: { lat: lat, lng: lng },
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.TOP_CENTER,
        },
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.RIGHT_CENTER,
        },
        scaleControl: true,
        streetViewControl: true,
        streetViewControlOptions: {
            position: google.maps.ControlPosition.RIGHT_TOP,
        },
        fullscreenControl: true,
    });

    infoWindow = new google.maps.InfoWindow();
}

function addMarker(destination) {
    if (!destination.latitude || !destination.longitude) return;

    const position = {
        lat: parseFloat(destination.latitude),
        lng: parseFloat(destination.longitude)
    };

    const marker = new google.maps.Marker({
        position: position,
        map: map,
        title: destination.name,
        animation: google.maps.Animation.DROP,
        icon: {
            url: getMarkerIcon(destination.categories),
            scaledSize: new google.maps.Size(40, 40),
        }
    });

    const infoContent = `
        <div class="map-info-window">
            <h6 class="fw-bold text-primary mb-2">${destination.name}</h6>
            <p class="mb-2">
                <i class="fas fa-map-marker-alt me-1 text-danger"></i>
                ${destination.city}, ${destination.state}
            </p>
            <div class="mb-2">
                <div class="rating-display">
                    ${'★'.repeat(Math.floor(destination.rating))}${'☆'.repeat(5-Math.floor(destination.rating))}
                    <span class="ms-1 text-muted">(${destination.rating}/5.0)</span>
                </div>
            </div>
            <p class="small text-muted mb-2">${destination.description}</p>
            <div class="d-flex gap-2">
                <a href="/destinations/${destination.slug}/" class="btn btn-primary btn-sm">
                    <i class="fas fa-info-circle me-1"></i> Details
                </a>
                <button onclick="getDirections(${position.lat}, ${position.lng})" class="btn btn-outline-primary btn-sm">
                    <i class="fas fa-directions me-1"></i> Directions
                </button>
            </div>
        </div>
    `;

    marker.addListener("click", () => {
        infoWindow.setContent(infoContent);
        infoWindow.open(map, marker);
    });

    markers.push(marker);
    return marker;
}

function getMarkerIcon(categories) {
    // Return different marker icons based on destination category
    const categoryIcons = {
        'eco': 'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
        'cultural': 'https://maps.google.com/mapfiles/ms/icons/purple-dot.png',
        'religious': 'https://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
        'adventure': 'https://maps.google.com/mapfiles/ms/icons/orange-dot.png',
        'historical': 'https://maps.google.com/mapfiles/ms/icons/brown-dot.png',
        'wildlife': 'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
        'beach': 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
        'mountain': 'https://maps.google.com/mapfiles/ms/icons/ltblue-dot.png'
    };

    // Return icon based on first category, or default red
    const firstCategory = categories && categories.length > 0 ? categories[0] : null;
    return categoryIcons[firstCategory] || 'https://maps.google.com/mapfiles/ms/icons/red-dot.png';
}

function clearMarkers() {
    markers.forEach(marker => marker.setMap(null));
    markers = [];
}

function showDestinationsOnMap(destinations) {
    clearMarkers();
    
    if (destinations.length === 0) return;
    
    const bounds = new google.maps.LatLngBounds();
    
    destinations.forEach(destination => {
        const marker = addMarker(destination);
        if (marker) {
            bounds.extend(marker.getPosition());
        }
    });
    
    // Fit map to show all markers
    if (destinations.length > 1) {
        map.fitBounds(bounds);
    } else if (destinations.length === 1) {
        map.setCenter({
            lat: parseFloat(destinations[0].latitude),
            lng: parseFloat(destinations[0].longitude)
        });
        map.setZoom(10);
    }
}

function focusOnDestination(destination) {
    if (!destination.latitude || !destination.longitude) return;
    
    const position = {
        lat: parseFloat(destination.latitude),
        lng: parseFloat(destination.longitude)
    };
    
    map.setCenter(position);
    map.setZoom(12);
    
    // Find and trigger the marker for this destination
    const marker = markers.find(m => 
        m.getPosition().lat() === position.lat && 
        m.getPosition().lng() === position.lng
    );
    
    if (marker) {
        google.maps.event.trigger(marker, 'click');
    }
}

function getDirections(lat, lng) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLat = position.coords.latitude;
                const userLng = position.coords.longitude;
                
                const directionsUrl = `https://www.google.com/maps/dir/${userLat},${userLng}/${lat},${lng}`;
                window.open(directionsUrl, '_blank');
            },
            () => {
                // Fallback if geolocation fails
                const directionsUrl = `https://www.google.com/maps/dir//${lat},${lng}`;
                window.open(directionsUrl, '_blank');
            }
        );
    } else {
        // Fallback if geolocation not supported
        const directionsUrl = `https://www.google.com/maps/dir//${lat},${lng}`;
        window.open(directionsUrl, '_blank');
    }
}

function searchNearby(category, lat, lng) {
    const service = new google.maps.places.PlacesService(map);
    
    const request = {
        location: { lat: lat, lng: lng },
        radius: 10000, // 10km radius
        type: [category]
    };
    
    service.nearbySearch(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            results.forEach(place => {
                const marker = new google.maps.Marker({
                    position: place.geometry.location,
                    map: map,
                    title: place.name,
                    icon: {
                        url: 'https://maps.google.com/mapfiles/ms/icons/pink-dot.png',
                        scaledSize: new google.maps.Size(30, 30),
                    }
                });
                
                marker.addListener('click', () => {
                    infoWindow.setContent(`
                        <div class="map-info-window">
                            <h6 class="fw-bold mb-2">${place.name}</h6>
                            <p class="mb-2">
                                <i class="fas fa-map-marker-alt me-1 text-danger"></i>
                                ${place.vicinity}
                            </p>
                            <div class="mb-2">
                                <div class="rating-display">
                                    ${'★'.repeat(Math.floor(place.rating || 0))}${'☆'.repeat(5-Math.floor(place.rating || 0))}
                                    <span class="ms-1 text-muted">(${place.rating || 'N/A'}/5.0)</span>
                                </div>
                            </div>
                            <button onclick="getDirections(${place.geometry.location.lat()}, ${place.geometry.location.lng()})" class="btn btn-outline-primary btn-sm">
                                <i class="fas fa-directions me-1"></i> Directions
                            </button>
                        </div>
                    `);
                    infoWindow.open(map, marker);
                });
                
                markers.push(marker);
            });
        }
    });
}

// Initialize map when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if map element exists
    if (document.getElementById('map')) {
        // Map will be initialized by Google Maps callback
    }
});

// Export functions for global use
window.initMap = initMap;
window.addMarker = addMarker;
window.showDestinationsOnMap = showDestinationsOnMap;
window.focusOnDestination = focusOnDestination;
window.getDirections = getDirections;
window.searchNearby = searchNearby;