// DOM Elements
const sidebar = document.getElementById('sidebar');
const sidebarItems = document.querySelectorAll('#sidebarUl li');
let currentTab = document.getElementById('tab-dashboard');

// Sidebar hover functionality
sidebar.addEventListener('mouseenter', () => {
    sidebar.classList.add('expanded');
});

sidebar.addEventListener('mouseleave', () => {
    sidebar.classList.remove('expanded');
});

// Tab navigation
function loadPage(tabId) {
    // Hide current tab
    if (currentTab) {
        currentTab.classList.add('tab-content-hidden');
    }

    // Show new tab
    const newTab = document.getElementById(`tab-${tabId}`);
    if (newTab) {
        newTab.classList.remove('tab-content-hidden');
        currentTab = newTab;
    }

    // Update active state in sidebar
    sidebarItems.forEach(item => item.classList.remove('active'));
    const activeItem = document.querySelector(`[data-tab="${tabId}"]`).parentElement;
    if (activeItem) {
        activeItem.classList.add('active');
    }
}

// Add click listeners to sidebar items
sidebarItems.forEach(item => {
    const link = item.querySelector('a');
    if (link) {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const tabId = link.dataset.tab;
            if (tabId) {
                loadPage(tabId);
            }
        });
    }
});

// Optional: Handle browser back/forward buttons with URL hash
window.addEventListener('hashchange', () => {
    const hash = window.location.hash.slice(1);
    if (hash) {
        loadPage(hash);
    }
});

// Update URL when tab changes
sidebarItems.forEach(item => {
    const link = item.querySelector('a');
    if (link) {
        link.addEventListener('click', () => {
            const tabId = link.dataset.tab;
            window.location.hash = tabId;
        });
    }
});

// Load initial tab from URL hash if present
if (window.location.hash) {
    const initialTab = window.location.hash.slice(1);
    loadPage(initialTab);
}