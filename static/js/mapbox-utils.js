/**
 * Mapbox GL JS Utilities for Smart Tourism India
 * Provides centralized map functionality with 3D features
 */

class MapboxUtils {
    constructor() {
        this.map = null;
        this.markers = [];
        this.popups = [];
        this.currentStyle = 'mapbox://styles/mapbox/outdoors-v12';
        this.is3DEnabled = true;
    }

    /**
     * Initialize a new Mapbox GL JS map
     * @param {string} containerId - ID of the container element
     * @param {Object} options - Map configuration options
     */
    initMap(containerId, options = {}) {
        const defaultOptions = {
            container: containerId,
            style: this.currentStyle,
            center: options.center || window.MAPBOX_CONFIG.center,
            zoom: options.zoom || window.MAPBOX_CONFIG.zoom,
            pitch: options.pitch || (this.is3DEnabled ? 45 : 0),
            bearing: options.bearing || 0,
            antialias: true,
            ...options
        };

        this.map = new mapboxgl.Map(defaultOptions);

        // Add navigation controls
        this.map.addControl(new mapboxgl.NavigationControl(), 'top-right');

        // Add fullscreen control
        this.map.addControl(new mapboxgl.FullscreenControl(), 'top-right');

        // Add geolocate control
        this.map.addControl(
            new mapboxgl.GeolocateControl({
                positionOptions: {
                    enableHighAccuracy: true
                },
                trackUserLocation: true,
                showUserHeading: true
            }),
            'top-right'
        );

        // Add scale control
        this.map.addControl(new mapboxgl.ScaleControl({
            maxWidth: 80,
            unit: 'metric'
        }), 'bottom-left');

        // Wait for map to load before adding 3D features
        this.map.on('load', () => {
            this.add3DTerrain();
            this.add3DBuildings();
            this.addSkyLayer();
            this.addCustomControls();
        });

        return this.map;
    }

    /**
     * Add 3D terrain to the map
     */
    add3DTerrain() {
        if (!this.is3DEnabled) return;

        // Add terrain source
        this.map.addSource('mapbox-dem', {
            'type': 'raster-dem',
            'url': 'mapbox://mapbox.mapbox-terrain-dem-v1',
            'tileSize': 512,
            'maxzoom': 14
        });

        // Add terrain layer
        this.map.setTerrain({ 'source': 'mapbox-dem', 'exaggeration': 1.5 });
    }

    /**
     * Add 3D buildings to the map
     */
    add3DBuildings() {
        if (!this.is3DEnabled) return;

        // Add 3D building layer
        const layers = this.map.getStyle().layers;
        const labelLayerId = layers.find(
            (layer) => layer.type === 'symbol' && layer.layout['text-field']
        ).id;

        this.map.addLayer(
            {
                'id': '3d-buildings',
                'source': 'composite',
                'source-layer': 'building',
                'filter': ['==', 'extrude', 'true'],
                'type': 'fill-extrusion',
                'minzoom': 12,
                'paint': {
                    'fill-extrusion-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'height'],
                        0, '#FF6B6B',
                        50, '#4ECDC4',
                        100, '#45B7D1',
                        200, '#96CEB4',
                        300, '#FFEAA7'
                    ],
                    'fill-extrusion-height': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        12, 0,
                        12.05, ['get', 'height']
                    ],
                    'fill-extrusion-base': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        12, 0,
                        12.05, ['get', 'min_height']
                    ],
                    'fill-extrusion-opacity': 0.8
                }
            },
            labelLayerId
        );
    }

    /**
     * Add atmospheric sky layer
     */
    addSkyLayer() {
        if (!this.is3DEnabled) return;

        this.map.addLayer({
            'id': 'sky',
            'type': 'sky',
            'paint': {
                'sky-type': 'atmosphere',
                'sky-atmosphere-sun': [0.0, 0.0],
                'sky-atmosphere-sun-intensity': 15
            }
        });
    }

    /**
     * Add custom controls
     */
    addCustomControls() {
        // 3D Toggle Control
        const toggle3DControl = {
            onAdd: (map) => {
                const div = document.createElement('div');
                div.className = 'mapboxgl-ctrl mapboxgl-ctrl-group';
                div.innerHTML = `
                    <button type="button" class="mapboxgl-ctrl-icon" id="toggle-3d" 
                            title="${this.is3DEnabled ? 'Disable' : 'Enable'} 3D View">
                        <i class="fas fa-cube"></i>
                    </button>
                `;

                div.querySelector('#toggle-3d').addEventListener('click', () => {
                    this.toggle3D();
                });

                return div;
            },
            onRemove: () => {}
        };

        this.map.addControl(toggle3DControl, 'top-right');

        // Style Switcher Control
        const styleSwitcherControl = {
            onAdd: (map) => {
                const div = document.createElement('div');
                div.className = 'mapboxgl-ctrl mapboxgl-ctrl-group';
                div.innerHTML = `
                    <select class="mapbox-style-switcher" title="Change Map Style">
                        <option value="mapbox://styles/mapbox/outdoors-v12">Outdoors</option>
                        <option value="mapbox://styles/mapbox/satellite-streets-v12">Satellite</option>
                        <option value="mapbox://styles/mapbox/streets-v12">Streets</option>
                        <option value="mapbox://styles/mapbox/light-v11">Light</option>
                        <option value="mapbox://styles/mapbox/dark-v11">Dark</option>
                    </select>
                `;

                const select = div.querySelector('select');
                select.value = this.currentStyle;
                select.addEventListener('change', (e) => {
                    this.changeStyle(e.target.value);
                });

                return div;
            },
            onRemove: () => {}
        };

        this.map.addControl(styleSwitcherControl, 'top-left');
    }

    /**
     * Toggle 3D view
     */
    toggle3D() {
        this.is3DEnabled = !this.is3DEnabled;
        
        if (this.is3DEnabled) {
            this.map.easeTo({ pitch: 45, duration: 1000 });
            this.add3DTerrain();
            this.add3DBuildings();
            this.addSkyLayer();
        } else {
            this.map.easeTo({ pitch: 0, duration: 1000 });
            if (this.map.getSource('mapbox-dem')) {
                this.map.setTerrain(null);
            }
            if (this.map.getLayer('3d-buildings')) {
                this.map.removeLayer('3d-buildings');
            }
            if (this.map.getLayer('sky')) {
                this.map.removeLayer('sky');
            }
        }

        // Update button title
        const toggle3DBtn = document.getElementById('toggle-3d');
        if (toggle3DBtn) {
            toggle3DBtn.title = `${this.is3DEnabled ? 'Disable' : 'Enable'} 3D View`;
        }
    }

    /**
     * Change map style
     */
    changeStyle(styleUrl) {
        this.currentStyle = styleUrl;
        this.map.setStyle(styleUrl);
        
        // Re-add custom layers after style change
        this.map.once('style.load', () => {
            if (this.is3DEnabled) {
                this.add3DTerrain();
                this.add3DBuildings();
                this.addSkyLayer();
            }
        });
    }

    /**
     * Add a marker with custom popup
     * @param {Object} destination - Destination data
     * @param {Object} options - Marker options
     */
    addMarker(destination, options = {}) {
        if (!destination.latitude || !destination.longitude) return null;

        const coordinates = [parseFloat(destination.longitude), parseFloat(destination.latitude)];

        // Create custom marker element
        const markerEl = document.createElement('div');
        markerEl.className = 'custom-marker';
        markerEl.style.cssText = `
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            border: 3px solid white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: white;
            font-weight: bold;
            transition: transform 0.3s;
        `;
        markerEl.innerHTML = '📍';

        // Add hover effect
        markerEl.addEventListener('mouseenter', () => {
            markerEl.style.transform = 'scale(1.2)';
        });
        markerEl.addEventListener('mouseleave', () => {
            markerEl.style.transform = 'scale(1)';
        });

        // Create marker
        const marker = new mapboxgl.Marker(markerEl)
            .setLngLat(coordinates)
            .addTo(this.map);

        // Create popup
        const popupContent = this.createPopupContent(destination);
        const popup = new mapboxgl.Popup({
            offset: 25,
            closeButton: true,
            closeOnClick: false,
            className: 'custom-popup'
        }).setHTML(popupContent);

        marker.setPopup(popup);

        // Store marker reference
        this.markers.push({ marker, destination, popup });

        return marker;
    }

    /**
     * Create popup content for destinations
     */
    createPopupContent(destination) {
        return `
            <div class="mapbox-popup-content">
                <div class="popup-header">
                    <h6 class="popup-title">${destination.name}</h6>
                    <div class="popup-rating">
                        ${'★'.repeat(Math.floor(destination.average_rating || 0))}${'☆'.repeat(5-Math.floor(destination.average_rating || 0))}
                        <span class="rating-text">(${(destination.average_rating || 0).toFixed(1)})</span>
                    </div>
                </div>
                <p class="popup-location">
                    <i class="fas fa-map-marker-alt"></i>
                    ${destination.city}, ${destination.state?.name || destination.state}
                </p>
                <p class="popup-description">${destination.short_description || destination.description}</p>
                <div class="popup-actions">
                    <a href="/destinations/${destination.slug}/" class="btn btn-primary btn-sm">
                        <i class="fas fa-info-circle"></i> Details
                    </a>
                    <button onclick="mapboxUtils.getDirections(${destination.longitude}, ${destination.latitude})" 
                            class="btn btn-outline-primary btn-sm">
                        <i class="fas fa-directions"></i> Directions
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Show multiple destinations on map
     */
    showDestinations(destinations) {
        this.clearMarkers();

        if (!destinations || destinations.length === 0) return;

        const bounds = new mapboxgl.LngLatBounds();

        destinations.forEach(destination => {
            const marker = this.addMarker(destination);
            if (marker) {
                bounds.extend([destination.longitude, destination.latitude]);
            }
        });

        // Fit map to show all markers
        if (destinations.length > 1) {
            this.map.fitBounds(bounds, {
                padding: { top: 50, bottom: 50, left: 50, right: 50 },
                maxZoom: 12
            });
        } else if (destinations.length === 1) {
            this.map.flyTo({
                center: [destinations[0].longitude, destinations[0].latitude],
                zoom: 12,
                pitch: this.is3DEnabled ? 45 : 0
            });
        }
    }

    /**
     * Focus on a specific destination
     */
    focusOnDestination(destination) {
        if (!destination.latitude || !destination.longitude) return;

        this.map.flyTo({
            center: [parseFloat(destination.longitude), parseFloat(destination.latitude)],
            zoom: 14,
            pitch: this.is3DEnabled ? 60 : 0,
            duration: 2000
        });

        // Find and open popup
        const markerData = this.markers.find(m => 
            Math.abs(m.destination.latitude - destination.latitude) < 0.0001 &&
            Math.abs(m.destination.longitude - destination.longitude) < 0.0001
        );

        if (markerData) {
            markerData.marker.togglePopup();
        }
    }

    /**
     * Clear all markers
     */
    clearMarkers() {
        this.markers.forEach(({ marker, popup }) => {
            marker.remove();
        });
        this.markers = [];
    }

    /**
     * Get directions to a location
     */
    getDirections(lng, lat) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const userLng = position.coords.longitude;
                    const userLat = position.coords.latitude;
                    
                    // Use Google Maps for directions (fallback)
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

    /**
     * Add route visualization (for trip planning)
     */
    async addRoute(coordinates, options = {}) {
        if (!coordinates || coordinates.length < 2) return;

        const directionsRequest = {
            coordinates: coordinates,
            profile: options.profile || 'driving',
            geometries: 'geojson'
        };

        try {
            const response = await fetch(`https://api.mapbox.com/directions/v5/mapbox/${directionsRequest.profile}/${coordinates.map(c => c.join(',')).join(';')}?geometries=geojson&access_token=${mapboxgl.accessToken}`);
            const data = await response.json();

            if (data.routes && data.routes[0]) {
                const route = data.routes[0];

                // Add route source
                if (this.map.getSource('route')) {
                    this.map.removeLayer('route');
                    this.map.removeSource('route');
                }

                this.map.addSource('route', {
                    'type': 'geojson',
                    'data': {
                        'type': 'Feature',
                        'properties': {},
                        'geometry': route.geometry
                    }
                });

                // Add route layer
                this.map.addLayer({
                    'id': 'route',
                    'type': 'line',
                    'source': 'route',
                    'layout': {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    'paint': {
                        'line-color': '#3887be',
                        'line-width': 5,
                        'line-opacity': 0.75
                    }
                });

                // Fit map to route
                const bounds = new mapboxgl.LngLatBounds();
                route.geometry.coordinates.forEach(coord => bounds.extend(coord));
                this.map.fitBounds(bounds, { padding: 50 });
            }
        } catch (error) {
            console.error('Error getting route:', error);
        }
    }

    /**
     * Remove route visualization
     */
    removeRoute() {
        if (this.map.getSource('route')) {
            this.map.removeLayer('route');
            this.map.removeSource('route');
        }
    }
}

// Create global instance
window.mapboxUtils = new MapboxUtils();

// Add custom CSS for map components
const mapboxCSS = `
<style>
.mapbox-popup-content {
    max-width: 300px;
    font-family: 'Inter', sans-serif;
}

.popup-header {
    margin-bottom: 10px;
}

.popup-title {
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 5px;
    font-size: 16px;
}

.popup-rating {
    color: #f39c12;
    font-size: 14px;
}

.rating-text {
    color: #7f8c8d;
    margin-left: 5px;
}

.popup-location {
    color: #e74c3c;
    font-size: 14px;
    margin-bottom: 8px;
}

.popup-description {
    font-size: 13px;
    color: #34495e;
    margin-bottom: 10px;
    line-height: 1.4;
}

.popup-actions {
    display: flex;
    gap: 8px;
}

.popup-actions .btn {
    font-size: 12px;
    padding: 6px 12px;
    border-radius: 4px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.popup-actions .btn-primary {
    background-color: #3498db;
    border-color: #3498db;
    color: white;
}

.popup-actions .btn-outline-primary {
    border: 1px solid #3498db;
    color: #3498db;
    background: white;
}

.popup-actions .btn:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

.mapbox-style-switcher {
    background: white;
    border: none;
    padding: 8px;
    border-radius: 4px;
    font-size: 12px;
    cursor: pointer;
}

.custom-marker {
    animation: markerBounce 2s infinite;
}

@keyframes markerBounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-10px);
    }
    60% {
        transform: translateY(-5px);
    }
}
</style>
`;

// Inject CSS
document.head.insertAdjacentHTML('beforeend', mapboxCSS);