// Smart Tourism India - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initializeAnimations();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize wishlist functionality
    initializeWishlist();
    
    // Initialize filter chips
    initializeFilters();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize smooth scrolling
    initializeSmoothScroll();
});

// Animation observers
function initializeAnimations() {
    if ('IntersectionObserver' in window) {
        const animatedElements = document.querySelectorAll('.fade-in, .slide-up, .scale-in');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        animatedElements.forEach(el => {
            el.style.animationPlayState = 'paused';
            observer.observe(el);
        });
    }
}

// Search functionality
function initializeSearch() {
    const searchForm = document.querySelector('#searchForm');
    const searchInput = document.querySelector('#searchInput');
    const searchBtn = document.querySelector('.search-btn');
    
    if (searchForm && searchInput) {
        // Add search suggestions (could be enhanced with AJAX)
        searchInput.addEventListener('input', debounce(function(e) {
            const query = e.target.value.trim();
            if (query.length > 2) {
                // Implement search suggestions here
                console.log('Searching for:', query);
            }
        }, 300));
        
        // Handle form submission
        searchForm.addEventListener('submit', function(e) {
            if (searchInput.value.trim() === '') {
                e.preventDefault();
                searchInput.focus();
                showToast('Please enter a search term', 'warning');
            }
        });
    }
}

// Wishlist functionality
function initializeWishlist() {
    const wishlistBtns = document.querySelectorAll('.wishlist-btn');
    
    wishlistBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const destinationId = this.dataset.destinationId;
            const isActive = this.classList.contains('active');
            
            // Toggle wishlist status
            toggleWishlist(destinationId, !isActive, this);
        });
    });
}

// Filter chips functionality
function initializeFilters() {
    const filterChips = document.querySelectorAll('.filter-chip');
    
    filterChips.forEach(chip => {
        chip.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Toggle active state
            this.classList.toggle('active');
            
            // Apply filters (implement based on your needs)
            const activeFilters = Array.from(document.querySelectorAll('.filter-chip.active'))
                .map(chip => chip.dataset.category);
            
            applyFilters(activeFilters);
        });
    });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Wishlist toggle function
function toggleWishlist(destinationId, add, button) {
    // Show loading state
    const originalIcon = button.innerHTML;
    button.innerHTML = '<div class="loading-spinner"></div>';
    button.disabled = true;
    
    // Simulate API call (replace with actual implementation)
    setTimeout(() => {
        if (add) {
            button.classList.add('active');
            button.innerHTML = '<i class="fas fa-heart"></i>';
            showToast('Added to wishlist!', 'success');
        } else {
            button.classList.remove('active');
            button.innerHTML = '<i class="far fa-heart"></i>';
            showToast('Removed from wishlist', 'info');
        }
        
        button.disabled = false;
    }, 500);
    
    // In a real implementation, you would make an AJAX call here:
    /*
    fetch('/api/wishlist/toggle/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            'destination_id': destinationId,
            'action': add ? 'add' : 'remove'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (add) {
                button.classList.add('active');
                button.innerHTML = '<i class="fas fa-heart"></i>';
                showToast('Added to wishlist!', 'success');
            } else {
                button.classList.remove('active');
                button.innerHTML = '<i class="far fa-heart"></i>';
                showToast('Removed from wishlist', 'info');
            }
        } else {
            showToast('Error updating wishlist', 'error');
            button.innerHTML = originalIcon;
        }
        button.disabled = false;
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error updating wishlist', 'error');
        button.innerHTML = originalIcon;
        button.disabled = false;
    });
    */
}

// Apply filters function
function applyFilters(activeFilters) {
    const cards = document.querySelectorAll('.destination-card');
    
    cards.forEach(card => {
        if (activeFilters.length === 0) {
            // Show all cards if no filters are active
            card.style.display = 'block';
        } else {
            const cardCategories = (card.dataset.categories || '').split(',');
            const hasMatchingCategory = activeFilters.some(filter => 
                cardCategories.includes(filter)
            );
            
            card.style.display = hasMatchingCategory ? 'block' : 'none';
        }
    });
    
    // Update results count
    const visibleCards = Array.from(cards).filter(card => 
        card.style.display !== 'none'
    ).length;
    
    const resultsCount = document.querySelector('#resultsCount');
    if (resultsCount) {
        resultsCount.textContent = `${visibleCards} destination${visibleCards !== 1 ? 's' : ''} found`;
    }
}

// Toast notification function
function showToast(message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${getToastIcon(type)} ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Get or create toast container
function getOrCreateToastContainer() {
    let container = document.querySelector('#toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    return container;
}

// Get toast icon based on type
function getToastIcon(type) {
    const icons = {
        success: '<i class="fas fa-check-circle me-2"></i>',
        error: '<i class="fas fa-exclamation-triangle me-2"></i>',
        warning: '<i class="fas fa-exclamation-circle me-2"></i>',
        info: '<i class="fas fa-info-circle me-2"></i>'
    };
    return icons[type] || icons.info;
}

// Get CSRF token for Django
function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Card hover effects
document.addEventListener('mouseenter', function(e) {
    if (e.target.closest('.card')) {
        e.target.closest('.card').style.transform = 'translateY(-10px)';
    }
}, true);

document.addEventListener('mouseleave', function(e) {
    if (e.target.closest('.card')) {
        e.target.closest('.card').style.transform = 'translateY(0)';
    }
}, true);

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    }
});

// Add CSS for navbar scroll effect
const style = document.createElement('style');
style.textContent = `
    .navbar-scrolled {
        background: rgba(13, 110, 253, 0.95) !important;
        backdrop-filter: blur(10px);
    }
`;
document.head.appendChild(style);

// Loading screen (optional)
window.addEventListener('load', function() {
    const loader = document.querySelector('#loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => {
            loader.style.display = 'none';
        }, 300);
    }
});

// Image lazy loading fallback for older browsers
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.src = img.dataset.src || img.src;
    });
} else {
    // Fallback for browsers that don't support lazy loading
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/lozad@1.16.0/dist/lozad.min.js';
    document.head.appendChild(script);
    
    script.onload = function() {
        const observer = lozad();
        observer.observe();
    };
}