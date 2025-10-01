// Smart Tourism India - Main JavaScript

// Handle background image loading fallbacks
document.addEventListener('DOMContentLoaded', function() {
    // Function to check if background image loads
    function checkBackgroundImage(element, fallbackClass) {
        if (!element) return;
        
        const style = window.getComputedStyle(element);
        const backgroundImage = style.backgroundImage;
        
        if (backgroundImage && backgroundImage !== 'none') {
            const imageUrl = backgroundImage.replace(/url\(["']?([^"']+)["']?\)/g, '$1');
            const img = new Image();
            
            img.onload = function() {
                // Image loaded successfully
                console.log('Background image loaded:', imageUrl);
            };
            
            img.onerror = function() {
                // Image failed to load, add fallback class
                console.log('Background image failed to load:', imageUrl);
                element.classList.add('no-image');
            };
            
            img.src = imageUrl;
        } else {
            // No background image set, add fallback class
            element.classList.add('no-image');
        }
    }
    
    // Handle video backgrounds for page hero sections
    const videoSections = [
        { id: 'destinations-hero', videoClass: 'destinations-video' },
        { id: 'categories-hero', videoClass: 'categories-video' },
        { id: 'maps-hero', videoClass: 'maps-video' },
        { id: 'trips-hero', videoClass: 'trips-video' }
    ];
    
    videoSections.forEach(function(section) {
        const element = document.getElementById(section.id);
        const video = element ? element.querySelector('.' + section.videoClass) : null;
        
        if (element && video) {
            // Handle video loading errors
            video.addEventListener('error', function() {
                console.log('Video failed to load, using image fallback');
                video.style.display = 'none';
            });
            
            // Handle video loading success
            video.addEventListener('loadeddata', function() {
                console.log('Video loaded successfully for', section.id);
            });
            
            // For mobile optimization, pause video if not in viewport
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        if (video.paused) video.play();
                    } else {
                        if (!video.paused) video.pause();
                    }
                });
            });
            
            observer.observe(element);
        } else if (element) {
            // No video found, check for background images
            checkBackgroundImage(element, 'no-image');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.style.animationDelay = (index * 0.1) + 's';
        card.classList.add('fade-in');
    });
    
    // Enhanced search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            searchTimeout = setTimeout(function() {
                if (query.length >= 2) {
                    // You can implement live search suggestions here
                    console.log('Searching for:', query);
                }
            }, 300);
        });
    }
    
    // Wishlist functionality
    window.toggleWishlist = function(destinationId, button) {
        if (!button) return;
        
        const icon = button.querySelector('i');
        const originalClass = icon.className;
        
        // Show loading state
        icon.className = 'fas fa-spinner fa-spin';
        button.disabled = true;
        
        fetch('/toggle_wishlist/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                destination_id: destinationId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.added) {
                    icon.className = 'fas fa-heart';
                    button.classList.add('active');
                    showNotification(data.message, 'success');
                } else {
                    icon.className = 'far fa-heart';
                    button.classList.remove('active');
                    showNotification(data.message, 'info');
                }
            } else {
                icon.className = originalClass;
                showNotification(data.message || 'Error updating wishlist', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            icon.className = originalClass;
            showNotification('Network error. Please try again.', 'error');
        })
        .finally(() => {
            button.disabled = false;
        });
    };
    
    // Utility function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Simple notification system
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
        `;
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

console.log('Smart Tourism India - Main JS loaded successfully!');