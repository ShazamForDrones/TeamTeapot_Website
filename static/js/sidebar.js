// DOM Elements
const sidebar = document.getElementById('sidebar');
const sidebarItems = document.querySelectorAll('#sidebarUl li');
let currentTab = document.getElementById('tab-dashboard');

// Sidebar hover functionality
sidebar.addEventListener('mouseenter', () => sidebar.classList.add('expanded'));
sidebar.addEventListener('mouseleave', () => sidebar.classList.remove('expanded'));

// Tab navigation
function loadPage(tabId) {
    // Hide current tab
    if (currentTab) currentTab.classList.add('hidden');

    // Show new tab
    const newTab = document.getElementById(`tab-${tabId}`);
    if (newTab) {
        newTab.classList.remove('hidden');
        currentTab = newTab;
    }

    // Update active state in sidebar
    sidebarItems.forEach(item => item.classList.remove('active'));
    const activeLink = document.querySelector(`[data-tab="${tabId}"]`);
    if (activeLink) activeLink.closest('li').classList.add('active');
}

// Add click listeners to sidebar items
sidebarItems.forEach(item => {
    const link = item.querySelector('a');
    if (link) {
        link.addEventListener('click', e => {
            e.preventDefault();
            const tabId = link.getAttribute('data-tab');
            if (tabId) {
                loadPage(tabId);
                window.location.hash = tabId;
            }
        });
    }
});

// Optional: Handle browser back/forward buttons with URL hash
window.addEventListener('hashchange', () => {
    const hash = window.location.hash.slice(1);
    if (hash) loadPage(hash);
});

// Load initial tab from URL hash if present
if (window.location.hash) {
    loadPage(window.location.hash.slice(1));
}